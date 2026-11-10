# Kiểm tra môi trường — Phase 1 (2026-11-10)

## Kết quả

Máy hiện tại chưa có môi trường khả dụng để chạy KG-R1:

| Thành phần | Kết quả thực tế |
| --- | --- |
| Python | `python` trỏ tới WindowsApps alias và không khởi chạy được; Python 3.12 do `py` phát hiện cũng bị `Access is denied`. Python 3.10 chưa có. |
| Conda | Không có trên `PATH`. |
| GPU/NVIDIA | `nvidia-smi` không có trên `PATH`. |
| WSL | Có `wsl.exe`, nhưng liệt kê distro bị `Wsl/EnumerateDistros/Service/E_ACCESS_DENIED`. |
| Data | Không có `data_kg/`, `data/`, hay `verl_checkpoints/` trong repo. |

## Lệnh đã kiểm tra

```powershell
python --version
conda --version
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
py --version
py -0p
wsl --status
wsl -l -q
```

Không có dependency nào được cài đặt và không có dữ liệu nào được tải trong bước này.

## Hệ quả

Không thể chạy server, xử lý parquet hay baseline local tại thời điểm kiểm tra. Bước tiếp theo cần một Linux environment có Python 3.10 và GPU CUDA (Modal là phương án phù hợp với phạm vi/budget trong kế hoạch), hoặc người dùng cần cung cấp một môi trường local/WSL đã hoạt động.

