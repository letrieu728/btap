# Audit nhãn nguồn: người chấm 1 và AI

## Dữ liệu

- Người chấm 1: `lab/audits/rater_1_submitted_labels.csv` (77/77 mục).
- Người chấm 2: `lab/audits/rater_2_ai.csv` (77/77 mục), một lượt chấm AI theo rubric strict được tạo mù trước khi nhận nhãn người chấm 1.

## Kết quả

| Chỉ số | Giá trị |
| --- | ---: |
| Mục được cả hai cho cùng nhãn 0–3 | 36/77 |
| Cohen's kappa trên nhãn 0–3 | 0.292 |
| Mục đồng thuận nhị phân (0/1 so với 2/3) | 76/77 |
| Regex true positive | 33 |
| Regex false positive | 3 |
| Regex false negative | 0 |
| Regex true negative | 40 |
| Precision của regex trong phần đồng thuận | 0.917 |
| Recall của regex trong phần đồng thuận | 1.000 |

## Diễn giải

Hai bản chấm chỉ trùng 36/77 ở nhãn chi tiết, nhưng trùng 76/77 ở quyết định chính “có/không bằng chứng”. Regex của Figure 4 không bỏ sót trường hợp “có bằng chứng” trong 76 mục đồng thuận, nhưng có ba dương tính sai. Kappa thấp-vừa cho thấy ranh giới giữa nhãn 1, 2 và 3 còn phụ thuộc diễn giải rubric; vì vậy nên báo cáo kết quả nhị phân và nêu rõ giới hạn này.

## Giới hạn

Người chấm 2 là AI, không phải người chấm độc lập. Các số trên là kiểm tra **người chấm 1 + AI**, không được mô tả là độ tin cậy giữa hai người chấm (two-human inter-rater reliability).
