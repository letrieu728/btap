# Tóm tắt hai kiểm định đề xuất

| Phần mở rộng | Liên quan đến bài báo | Cách nhìn nhanh | Trạng thái / chi phí |
| --- | --- | --- | --- |
| Consensus × claimed-source provenance | Tách cơ chế đằng sau Figure 4: agent có ngừng kiểm tra vì số đông, hay vì lời khẳng định “đã kiểm chứng nguồn”? | Thí nghiệm 2×2: 2/12 ghi chú sai × có/không tuyên bố nguồn; đo tỷ lệ mở workbook và trả lời đúng. | Runner đã sẵn sàng; không chạy LLM khi chưa có `--execute`; có chặn ngân sách. |
| Blinded source-label audit | Kiểm định biến `src` trong Figure 4, hiện được gán bằng regex từ khóa. | 325 quan sát Figure 4 → 77 mẫu mù phân tầng → 2 người chấm → Cohen’s kappa, precision, recall. | Bộ chấm đã tạo; không tốn API/GPU. Cần hai người chấm độc lập để có kết quả. |

## Cách diễn giải khi báo cáo

* Nếu tương tác ở thí nghiệm 2×2 âm: lời khẳng định nguồn sai làm hiệu ứng số đông mạnh hơn; rủi ro không chỉ là conformity mà còn là “provenance laundering”.
* Nếu audit có kappa cao và precision/recall cao: phép đo nguồn ở Figure 4 đáng tin hơn.
* Nếu audit kém: phần dữ liệu thực của Figure 4 cần được diễn giải là một proxy văn bản, không phải bằng chứng trực tiếp về hành vi mở nguồn.
