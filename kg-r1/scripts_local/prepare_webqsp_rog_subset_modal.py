"""Build the approved 300-train / 100-test WebQSP subset from public RoG data.

The output is deliberately compatible with ``kg_r1.search.KnowledgeGraph``:
``entities*.txt``, ``relations.txt``, and JSONL ``*_simple.json`` files.
It uses only a Modal CPU function and persists the small converted subset, not a
full Freebase dump, in the ``kgr1-webqsp-subset`` Volume.

Run:
    py -3.10 -m modal run scripts_local/prepare_webqsp_rog_subset_modal.py
"""

import json
from datetime import date
from pathlib import Path

import modal


APP_NAME = "kgr1-prepare-webqsp-subset"
VOLUME_NAME = "kgr1-webqsp-subset"
MOUNT_PATH = "/data"
TRAIN_LIMIT = 300
TEST_LIMIT = 100
SOURCE_DATASET = "rmanluo/RoG-webqsp"

app = modal.App(APP_NAME)
volume = modal.Volume.from_name(VOLUME_NAME, create_if_missing=True)
image = modal.Image.debian_slim(python_version="3.10").pip_install("datasets==4.5.0")


def _take_split(split: str, limit: int) -> list[dict]:
    from datasets import load_dataset

    stream = load_dataset(SOURCE_DATASET, split=split, streaming=True)
    rows = list(stream.take(limit))
    if len(rows) != limit:
        raise RuntimeError(f"Expected {limit} rows from {split}, received {len(rows)}")
    return rows


def _answer_records(row: dict) -> list[dict]:
    answers = list(row["answer"])
    answer_entities = list(row["a_entity"])
    return [
        {
            "text": answer,
            "kb_id": answer_entities[index] if index < len(answer_entities) else answer,
        }
        for index, answer in enumerate(answers)
    ]


def _convert(rows: list[dict], entity_to_index: dict[str, int], relation_to_index: dict[str, int]) -> list[dict]:
    converted: list[dict] = []
    for row in rows:
        triples: list[list[int]] = []
        entities: set[int] = set()
        for triple in row["graph"]:
            if len(triple) != 3 or not all(isinstance(item, str) and item for item in triple):
                raise ValueError(f"Invalid triple for {row['id']}: {triple!r}")
            head, relation, tail = triple
            head_index = entity_to_index[head]
            relation_index = relation_to_index[relation]
            tail_index = entity_to_index[tail]
            triples.append([head_index, relation_index, tail_index])
            entities.update((head_index, tail_index))

        initial_entities = [entity_to_index[entity] for entity in row["q_entity"]]
        converted.append(
            {
                "question": row["question"],
                "answers": _answer_records(row),
                "id": row["id"],
                "entities": initial_entities,
                "subgraph": {"entities": sorted(entities), "tuples": triples},
            }
        )
    return converted


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


@app.function(image=image, volumes={MOUNT_PATH: volume}, timeout=3600)
def prepare() -> dict:
    train_rows = _take_split("train", TRAIN_LIMIT)
    test_rows = _take_split("test", TEST_LIMIT)
    all_rows = train_rows + test_rows

    entity_names = sorted(
        {
            item
            for row in all_rows
            for triple in row["graph"]
            for item in (triple[0], triple[2])
        }
        | {entity for row in all_rows for entity in row["q_entity"]}
        | {entity for row in all_rows for entity in row["a_entity"]}
    )
    relation_names = sorted({triple[1] for row in all_rows for triple in row["graph"]})
    entity_to_index = {entity: index for index, entity in enumerate(entity_names)}
    relation_to_index = {relation: index for index, relation in enumerate(relation_names)}

    output_dir = Path(MOUNT_PATH) / "data_kg" / "webqsp"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "entities.txt").write_text("\n".join(entity_names) + "\n", encoding="utf-8")
    (output_dir / "entities_text.txt").write_text("\n".join(entity_names) + "\n", encoding="utf-8")
    (output_dir / "relations.txt").write_text("\n".join(relation_names) + "\n", encoding="utf-8")

    converted_train = _convert(train_rows, entity_to_index, relation_to_index)
    converted_test = _convert(test_rows, entity_to_index, relation_to_index)
    _write_jsonl(output_dir / "train_simple.json", converted_train)
    _write_jsonl(output_dir / "test_simple.json", converted_test)

    manifest = {
        "source_dataset": SOURCE_DATASET,
        "source_url": "https://huggingface.co/datasets/rmanluo/RoG-webqsp",
        "prepared_on": date.today().isoformat(),
        "selection": "first rows in Hugging Face streaming order; deterministic IDs recorded below",
        "train_limit": TRAIN_LIMIT,
        "test_limit": TEST_LIMIT,
        "train_ids": [row["id"] for row in train_rows],
        "test_ids": [row["id"] for row in test_rows],
        "entity_count": len(entity_names),
        "relation_count": len(relation_names),
        "train_triple_count": sum(len(row["graph"]) for row in train_rows),
        "test_triple_count": sum(len(row["graph"]) for row in test_rows),
    }
    (output_dir / "provenance.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    volume.commit()
    return manifest


@app.local_entrypoint()
def main() -> None:
    print(json.dumps(prepare.remote(), ensure_ascii=False, indent=2))

