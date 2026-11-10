# Artifact KG-R1

Thư mục này là bản ghi có thể kiểm tra của các bước đã hoàn thành cho kế hoạch
tái lập thu nhỏ KG-R1. Mã nguồn chuẩn là repository chính thức
[junhongmit/KG-R1](https://github.com/junhongmit/KG-R1), commit
`a3c02facbb3f4a905c9cf24707867d1df0746595`.

## Nội dung

- [notes/](./notes/): môi trường, provenance dữ liệu, tóm tắt bài báo và kiểm
  tra server.
- [scripts_local/](./scripts_local/): script Modal dùng để quan sát dữ liệu,
  dựng subset/parquet, xác minh và smoke-test FastAPI.

Các script không nhúng token hay secret. Chúng tham chiếu Modal Volume
`kgr1-webqsp-subset`; dữ liệu được tạo trên volume này không được commit vì
kích thước lớn.

## Phạm vi dữ liệu đã tạo

Nguồn công khai: `rmanluo/RoG-webqsp` trên Hugging Face. Subset được lấy theo
thứ tự streaming đầu nguồn: 300 train và 100 test, với 1,316,122 triple train,
455,077 triple test, 327,850 entity và 4,284 relation. Xem
[provenance](./notes/data-provenance.md) để có lệnh và đường dẫn đầu ra chính
xác.
