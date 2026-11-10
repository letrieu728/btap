"""Verify the converted public WebQSP subset stored in Modal Volume."""

import json
from pathlib import Path

import modal


app = modal.App("kgr1-verify-webqsp-subset")
volume = modal.Volume.from_name("kgr1-webqsp-subset")
MOUNT_PATH = "/data"


@app.function(volumes={MOUNT_PATH: volume})
def verify() -> dict:
    volume.reload()
    base = Path(MOUNT_PATH) / "data_kg" / "webqsp"
    manifest_path = base / "provenance.json"
    required = [
        "entities.txt",
        "entities_text.txt",
        "relations.txt",
        "train_simple.json",
        "test_simple.json",
        "provenance.json",
    ]
    missing = [name for name in required if not (base / name).is_file()]
    result = {"missing": missing, "base": str(base)}
    if not missing:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        result.update(
            {
                "train_lines": sum(1 for _ in (base / "train_simple.json").open(encoding="utf-8")),
                "test_lines": sum(1 for _ in (base / "test_simple.json").open(encoding="utf-8")),
                "entity_count": manifest["entity_count"],
                "relation_count": manifest["relation_count"],
                "train_triple_count": manifest["train_triple_count"],
                "test_triple_count": manifest["test_triple_count"],
                "first_train_id": manifest["train_ids"][0],
                "first_test_id": manifest["test_ids"][0],
            }
        )
    return result


@app.local_entrypoint()
def main() -> None:
    print(json.dumps(verify.remote(), ensure_ascii=False, indent=2))

