# KG server test — WebQSP subset

## Cấu hình

- Ngày chạy: 2026-11-10.
- Runtime: Modal CPU; FastAPI `0.115.12`, Uvicorn `0.34.2`, HTTPX `0.28.1`.
- Dữ liệu: Modal Volume `kgr1-webqsp-subset`, `/data/data_kg/webqsp`.
- Script: [test_webqsp_server_modal.py](../scripts_local/test_webqsp_server_modal.py).
- Test gửi HTTP request bằng `FastAPI TestClient` vào endpoint thật `POST /retrieve`; không dùng mock.

## Kết quả

`GET /health` trả **HTTP 200**. Bốn request sau đều trả **HTTP 200** trên sample `WebQTrn-0`, với triple được chọn:

```text
P!nk --freebase.valuenotation.is_reviewed--> Gender
```

| Action request | Kết quả trả về (rút gọn) |
| --- | --- |
| `get_relations_out(P!nk)` | Có `freebase.valuenotation.is_reviewed`, cùng các relation khác. |
| `get_relations_in(Gender)` | Có `freebase.valuenotation.is_reviewed`, cùng các relation khác. |
| `get_entities_out(P!nk, freebase.valuenotation.is_reviewed)` | Trả về entity gồm `Gender`, `Profession`, `Place of birth`, … |
| `get_entities_in(Gender, freebase.valuenotation.is_reviewed)` | Trả về entity gồm `50 Cent`, `Aaliyah`, `P!nk`, … |

## Lưu ý giao thức repo

Payload HTTP dùng action name canonical `get_relations_out`, `get_relations_in`, `get_entities_out`, `get_entities_in`. Repo ánh xạ các tên legacy `get_tail_*`/`get_head_*` sang các action canonical này trong `ACTION_NAME_MAPPING`. Đây là một khác biệt thực thi cần được giữ trong trace/cấu hình.

