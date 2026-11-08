# Tái chạy beta: kiểm định hoàn tất

Mô phỏng S-shaped copying được chạy tuần tự trên Windows, không dùng LLM/API. Tệp tái chạy có hậu tố `*_rerun_50seed`; vì vậy không ghi đè cache hoặc ảnh của tác giả.

## Kiểm tra tái lập

| Điều kiện | Số seed hợp lệ | Trạng thái |
| --- | ---: | --- |
| β = 1.68 | 50 | đạt |
| β = 3.9 | 50 | đạt |

Ảnh tái chạy có cùng kích thước hiển thị và cùng cấu trúc bốn ô với ảnh tác giả. Cache mới được lưu riêng trong `cache/model_beta_rerun_50seed.pkl`.

## Kết quả cần trình bày

- Khi β tăng từ 1.68 lên 3.9, khoảng cách với prior tại prior-strength thấp tăng rõ rệt. Ví dụ, với **form** ở `s=0.10`, median distance lần lượt là khoảng 0.141 và 0.242; với **name**, lần lượt là khoảng 0.193 và 0.438.
- Hiệu ứng mạnh hơn ở phần `name`: tại β=3.9, median distance còn cao cho đến prior-strength trung bình, phù hợp với trực giác về đáp ứng copying hình chữ S.
- Theo đường lý thuyết trong hình, điểm cân bằng hỗn hợp trở nên bất ổn khi `s < 0.18` (β=1.68) và `s < 0.51` (β=3.9). Mô phỏng tái chạy thể hiện đúng sự chuyển dịch này.

## Kết luận

Tái chạy độc lập trên Windows tái tạo được kết quả định tính chính của supplementary experiment: copying phi tuyến mạnh hơn làm tăng phân cực/độ lệch khỏi prior khi prior yếu. Đây là một **kiểm định tái lập cấu trúc**, không phải bằng chứng về trùng khớp bit-for-bit với môi trường tác giả.
