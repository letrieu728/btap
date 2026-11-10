# KG-R1: tái lập thu nhỏ có kiểm chứng

Kho này lưu bằng chứng thực thi cho quá trình tái lập thu nhỏ và mở rộng
[KG-R1](https://github.com/junhongmit/KG-R1), dựa trên mã nguồn chính thức tại
commit `a3c02facbb3f4a905c9cf24707867d1df0746595`.

## Trạng thái hiện tại

- Đã xác minh môi trường Modal và nguồn dữ liệu công khai RoG-WebQSP.
- Đã tạo tập đồ thị thu nhỏ: 300 mẫu train, 100 mẫu test; dữ liệu nằm trên
  Modal Volume `kgr1-webqsp-subset`, không đưa dữ liệu lớn vào Git.
- Đã tạo parquet prompt và kiểm tra bốn thao tác đồ thị qua FastAPI; tất cả
  trả HTTP 200.
- Chưa chạy baseline GPU, GRPO, hay báo cáo metric. Không có kết quả nào được
  suy diễn hoặc điền giả.

Chi tiết, provenance và script tái tạo nằm trong [kg-r1/](./kg-r1/).

## Quy ước thực thi

Mã nguồn chính thức là chuẩn khi có khác biệt với bài báo. Đặc biệt, parser
trong repo dùng các thẻ `<search>`, `<information>`, `<answer>` và hỗ trợ một
hành động điều kiện thứ năm; khác biệt với mô tả bốn hành động / `<kg-query>`
trong bài báo được ghi rõ ở [tóm tắt](./kg-r1/notes/paper-summary.md).

## Bước kế tiếp

Chạy baseline Qwen2.5-3B trên 100 mẫu test bằng GPU Modal, lưu log và metric
thật, sau đó mới tiến hành huấn luyện GRPO thu nhỏ nếu baseline ổn định.
