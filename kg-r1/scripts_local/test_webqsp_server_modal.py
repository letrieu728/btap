"""Exercise the KG-R1 FastAPI retrieval endpoint against the prepared subset."""

import json
from pathlib import Path

import modal


app = modal.App("kgr1-test-webqsp-server")
volume = modal.Volume.from_name("kgr1-webqsp-subset")
MOUNT_PATH = "/data"
image = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install("fastapi==0.115.12", "uvicorn==0.34.2", "httpx==0.28.1", "psutil==7.0.0")
    .env({"PYTHONPATH": "/root"})
    .add_local_dir("kg_r1", remote_path="/root/kg_r1")
)


def _content(response: dict) -> str:
    choices = response.get("choices", [])
    if not choices:
        return ""
    return choices[0].get("message", {}).get("content", "")


@app.function(image=image, volumes={MOUNT_PATH: volume}, timeout=900)
def test_server() -> dict:
    from fastapi.testclient import TestClient

    from kg_r1.search import server

    volume.reload()
    kg_path = Path(MOUNT_PATH) / "data_kg" / "webqsp"
    first_row = json.loads((kg_path / "train_simple.json").read_text(encoding="utf-8").splitlines()[0])
    head_idx, relation_idx, tail_idx = first_row["subgraph"]["tuples"][0]
    entities = (kg_path / "entities_text.txt").read_text(encoding="utf-8").splitlines()
    relations = (kg_path / "relations.txt").read_text(encoding="utf-8").splitlines()
    head, relation, tail = entities[head_idx], relations[relation_idx], entities[tail_idx]

    server.initialize_server(
        str(Path(MOUNT_PATH) / "data_kg"),
        supported_kgs=["webqsp"],
        enabled_actions=[
            "get_tail_relations",
            "get_head_relations",
            "get_tail_entities",
            "get_head_entities",
            "get_conditional_relations",
        ],
        use_entities_text=True,
    )
    client = TestClient(server.app)
    request_base = {"dataset_name": "webqsp", "sample_id": first_row["id"]}
    request_cases = {
        "get_relations_out": {**request_base, "action_type": "get_relations_out", "entity_id": head},
        "get_relations_in": {**request_base, "action_type": "get_relations_in", "entity_id": tail},
        "get_entities_out": {
            **request_base,
            "action_type": "get_entities_out",
            "entity_id": head,
            "relation": relation,
        },
        "get_entities_in": {
            **request_base,
            "action_type": "get_entities_in",
            "entity_id": tail,
            "relation": relation,
        },
    }
    results = {}
    for name, request in request_cases.items():
        http_response = client.post("/retrieve", json=[request])
        body = http_response.json()
        result = body[0] if body else {}
        results[name] = {
            "http_status": http_response.status_code,
            "is_error": result.get("is_error"),
            "error_type": result.get("error_type"),
            "response_excerpt": _content(result)[:300],
        }
    result = {
        "health_status": client.get("/health").status_code,
        "sample_id": first_row["id"],
        "selected_triple": [head, relation, tail],
        "results": results,
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


@app.local_entrypoint()
def main() -> None:
    print(test_server.remote())

