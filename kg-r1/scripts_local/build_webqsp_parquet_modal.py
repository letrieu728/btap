"""Build KG-R1 Parquet files from the verified Modal WebQSP subset.

This deliberately uses the repo's executable tag convention, ``<search>``,
rather than the paper's ``<kg-query>`` convention.
"""

import json
from pathlib import Path

import modal


app = modal.App("kgr1-build-webqsp-parquet")
volume = modal.Volume.from_name("kgr1-webqsp-subset")
MOUNT_PATH = "/data"
image = modal.Image.debian_slim(python_version="3.10").pip_install(
    "pandas==2.3.3", "pyarrow==25.0.1"
)


def _read_jsonl(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _to_parquet_rows(rows: list[dict], entity_texts: list[str], split: str) -> list[dict]:
    output: list[dict] = []
    for row in rows:
        initial_entity_ids = row["entities"]
        initial_entities = [entity_texts[index] for index in initial_entity_ids]
        entities_suffix = ", ".join(f'"{entity}"' for entity in initial_entities)
        augmented_question = f'{row["question"]}? (Initial entities: {entities_suffix})'
        prompt = (
            "Answer the given question. You must conduct reasoning inside <think> and </think> "
            "first every time you get new information. After reasoning, if you lack knowledge, "
            "query the knowledge graph with <search> function_name(arguments) </search>. "
            "The result appears between <information> and </information>. You can query as many "
            "times as needed. If no external knowledge is needed, provide the final answer inside "
            "<answer> and </answer> without detailed illustrations. "
            "For example, <answer> Beijing </answer>.\n\n"
            f"Question: {augmented_question}"
        )
        output.append(
            {
                "data_source": "RoG-webqsp-public-subset-for-KG-R1",
                "prompt": [{"role": "user", "content": prompt}],
                "ability": "kg-reasoning",
                "reward_model": {
                    "style": "rule",
                    "ground_truth": {
                        "target_text": [answer.get("text", "") for answer in row["answers"]],
                        "target_kb_id": [answer.get("kb_id", "") for answer in row["answers"]],
                    },
                },
                "extra_info": {
                    "split": split,
                    "sample_id": row["id"],
                    "dataset_name": "webqsp",
                    "initial_entities": initial_entities,
                    "initial_entity_ids": initial_entity_ids,
                },
            }
        )
    return output


@app.function(image=image, volumes={MOUNT_PATH: volume}, timeout=900)
def build() -> dict:
    import pandas as pd

    raw_dir = Path(MOUNT_PATH) / "data_kg" / "webqsp"
    output_dir = Path(MOUNT_PATH) / "data_kg" / "webqsp_search_augmented_initial_entities"
    output_dir.mkdir(parents=True, exist_ok=True)
    entity_texts = (raw_dir / "entities_text.txt").read_text(encoding="utf-8").splitlines()
    train_rows = _to_parquet_rows(_read_jsonl(raw_dir / "train_simple.json"), entity_texts, "train")
    test_rows = _to_parquet_rows(_read_jsonl(raw_dir / "test_simple.json"), entity_texts, "test")
    train_path = output_dir / "train.parquet"
    test_path = output_dir / "test.parquet"
    pd.DataFrame(train_rows).to_parquet(train_path, index=False)
    pd.DataFrame(test_rows).to_parquet(test_path, index=False)
    volume.commit()
    return {
        "train_rows": len(train_rows),
        "test_rows": len(test_rows),
        "train_bytes": train_path.stat().st_size,
        "test_bytes": test_path.stat().st_size,
        "tag_convention": "<search>/<information>/<answer>",
    }


@app.local_entrypoint()
def main() -> None:
    print(json.dumps(build.remote(), ensure_ascii=False, indent=2))

