"""Inspect the public RoG WebQSP dataset without downloading all splits locally.

Run with:
    py -3.10 -m modal run scripts_local/inspect_rog_webqsp.py
"""

import json

import modal


app = modal.App("kgr1-inspect-rog-webqsp")
image = modal.Image.debian_slim(python_version="3.10").pip_install("datasets==4.5.0")


@app.function(image=image, timeout=600)
def inspect() -> dict:
    from datasets import load_dataset

    dataset = load_dataset("rmanluo/RoG-webqsp", split="train", streaming=True)
    row = next(iter(dataset))
    graph = row["graph"]
    return {
        "keys": sorted(row.keys()),
        "id": row["id"],
        "question": row["question"],
        "answer": row["answer"],
        "q_entity": row["q_entity"],
        "a_entity": row["a_entity"],
        "answer_count": len(row["answer"]),
        "q_entity_count": len(row["q_entity"]),
        "a_entity_count": len(row["a_entity"]),
        "graph_triple_count": len(graph),
        "first_triple": graph[0] if graph else None,
        "first_triple_item_types": [type(item).__name__ for item in graph[0]] if graph else [],
    }


@app.local_entrypoint()
def main() -> None:
    print(json.dumps(inspect.remote(), ensure_ascii=False, indent=2))

