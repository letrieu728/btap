# KG-R1 — tóm tắt đã đối chiếu (Phase 0)

## Phạm vi và nguồn

- Paper: *Efficient and Transferable Agentic Knowledge Graph RAG via Reinforcement Learning*, arXiv:2509.26383v5, 22-05-2026 (preprint).
- Mã thực thi: `junhongmit/KG-R1`, commit `a3c02facbb3f4a905c9cf24707867d1df0746595`.
- Quyết định triển khai của nhóm: **repo là chuẩn thực thi**. Các kết quả chạy sẽ dùng giao thức và reward có thật trong repo; mọi khác biệt với paper được ghi rõ, không che giấu.

## Vấn đề trong một câu

KG-R1 thay pipeline KG-RAG nhiều module bằng một LLM agent tương tác nhiều turn với KG server, rồi huấn luyện policy đó end-to-end bằng RL để giảm chi phí sinh token và chuyển sang KG khác mà không fine-tune lại.

## Framework (diễn giải Figure 1 và Figure 3)

Hệ gồm một LLM agent và KG server. Agent nhận prompt chứa câu hỏi, suy luận trong `<think>`, phát hành truy vấn KG, nhận observation trong `<information>`, rồi tiếp tục cho tới khi trả lời trong `<answer>`. Server thực hiện truy vấn trên subgraph theo từng câu; paper mô tả bốn phép 1-hop (quan hệ/đỉnh theo hai chiều), nên một path dài `l` có thể thực hiện trong không quá `l + 1` action.

## Ba phương trình reward/training chính của paper

1. Turn reward: `r_turn_t = w_fmt v_fmt(m_t) + w_kg v_kg(a_t, o_(t+1)) + w_ans v_ans(m_T)`.
2. Global reward (Eq. 2): `R_global = w_H1 H1(A_hat_q, A_q) + w_ret v_ret`, trong đó `H1` là câu trả lời dự đoán có nằm trong gold hay không, còn `v_ret` kiểm tra gold entity có từng xuất hiện trong evidence retrieve hay không.
3. Return/advantage: `G_t^(n) = r_turn_t^(n) + lambda R_global^(n)` và `A_t^(n) = (G_t^(n) - mean(G)) / (std(G) + epsilon)` trên toàn bộ turn của nhóm rollout.

Paper Appendix E.3 lại ghi global reward theo F1, không phải H1. Đây là bất nhất nội bộ của paper. Khi chạy repo, script có `answer_score_mode=f1` và năm thành phần reward đều có trọng số `0.5`; số này là cấu hình repo, không được trình bày như công thức Eq. 2 của paper.

## Hai bảng kết quả paper cần trích dẫn

### Table 1 — kết quả in-domain (Hits@1, %, H=5)

| Dataset | KG-R1 Qwen2.5-3B | Điểm so sánh đáng chú ý | Gen tokens KG-R1 |
| --- | ---: | --- | ---: |
| WebQSP | 82.75 | RoG 7B: 79.89; RoG 72B: 81.63; ToG: 65.00 | 308.67 |
| CWQ | 65.31 | RoG 7B: 46.32; RoG 72B: 45.05; ToG: 32.25 | 311.14 |

Paper báo latency trung bình 6.4 ± 1.5 giây/câu và throughput 3.7 samples/s trên một H100, batch 64. Đây là số của paper, **không phải** mục tiêu cần đạt ở tái hiện thu nhỏ.

### Table 2 — transfer zero-shot (Hits@1 AVG, %)

| Train policy | AVG | T-REx | QALD-10en |
| --- | ---: | ---: | ---: |
| WebQSP | 77.50 | 83.38 | 41.96 |
| CWQ | 72.82 | 80.10 | 34.74 |

## Hai hạn chế cần nêu

1. KG phải có cấu trúc và query được; chất lượng, độ nhiễu và sai khác schema ảnh hưởng trực tiếp đến hiệu năng/transfer.
2. RL training vẫn tốn compute hơn supervised fine-tuning dù inference gọn hơn.

## Sai khác paper–repo phải giữ trong báo cáo

| Hạng mục | Paper v5 | Repo tại commit cố định | Cách xử lý của nhóm |
| --- | --- | --- | --- |
| Tag action | `<kg-query>` | README/generation parser dùng `<search>` và observation `<information>` | Dùng `<search>`/`<information>` khi chạy repo; ghi rõ khác paper. |
| Action server | 4 action 1-hop | Có thêm `get_conditional_relations`; action names nội bộ còn có alias `get_relations_in/out`, `get_entities_in/out` | Giữ 5 action của repo, log action thực tế trong trace. |
| Reward answer | Eq. 2 dùng H1; E.3 dùng F1 | Script set `answer_score_mode=f1`, reward weights 0.5 | Dùng F1/exact match không cần GPT judge; nêu tách biệt với paper. |
| Script tái hiện | Paper H=5, N=16, 4×H100, 400 steps | README tham chiếu file turn-5 không có; repo chỉ có script CWQ turn-7/4 GPU | Tạo script WebQSP/300/H=5/50-step riêng trước khi train; không chạy script gốc nguyên trạng. |

## Nguồn

- Paper: https://arxiv.org/html/2509.26383v5 (Section 3, Tables 1–3, Appendix A, E).
- Repo: https://github.com/junhongmit/KG-R1/tree/a3c02facbb3f4a905c9cf24707867d1df0746595

