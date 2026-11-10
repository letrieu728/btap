# Môi trường — Phase 1 (trạng thái hiện tại)

## Điều khiển Modal trên máy local

Các lệnh dưới đây đã chạy thành công trên Windows vào 2026-11-10:

```powershell
winget install --id Python.Python.3.10 --exact --accept-source-agreements --accept-package-agreements
py -3.10 -m pip install --user --disable-pip-version-check --no-cache-dir modal -q
py -3.10 -m modal --version
py -3.10 -m modal profile current
```

Phiên bản đã xác nhận:

| Thành phần | Phiên bản/trạng thái |
| --- | --- |
| Python (local control plane) | 3.10.11 |
| pip | 23.0.1 |
| Modal CLI | 1.6.3 |
| Modal profile | `letrieu728` |

Ở thời điểm kiểm tra ban đầu, Modal chỉ có `hf-cache-helix` và `helix-adapters`
Volume; không có Secret hay Modal app nào. Sau đó đã tạo Volume
`kgr1-webqsp-subset` và dựng subset WebQSP đã ghi trong
[provenance](./data-provenance.md).

## Chưa hoàn tất — không được coi là đã cài

Chưa có image Linux GPU `kgr1` hoặc `kg_server`; do đó các phiên bản GPU của
`torch`, `vLLM`, `veRL`, `flash-attn`… **chưa được cài hay xác nhận**. Image
CPU tạm thời đã xác nhận `fastapi` cho smoke test server.

## Điều kiện để tiếp tục

Subset WebQSP 2-hop/provenance hợp lệ đã sẵn sàng. Bước còn lại cần image GPU
và cấu hình baseline; không tải Freebase RDF đầy đủ.

