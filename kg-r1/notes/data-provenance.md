# Provenance dữ liệu WebQSP subset

## Nguồn đã dùng

- Dataset công khai: [`rmanluo/RoG-webqsp`](https://huggingface.co/datasets/rmanluo/RoG-webqsp).
- Mô tả nguồn: WebQSP có per-question Freebase subgraph; dataset card công bố 2.826 train và 1.628 test (tổng khoảng 1,66 GB).
- Không tải Freebase RDF dump đầy đủ.

## Subset tái hiện thu nhỏ

| Hạng mục | Giá trị |
| --- | ---: |
| Train | 300 mẫu, ID bắt đầu `WebQTrn-0` |
| Test | 100 mẫu, ID bắt đầu `WebQTest-0` |
| Entity duy nhất | 327.850 |
| Relation duy nhất | 4.284 |
| Triple train | 1.316.122 |
| Triple test | 455.077 |

Selection là 300/100 dòng đầu theo thứ tự streaming của Hugging Face. Toàn bộ danh sách ID, số triple và URL nguồn được ghi trong `provenance.json` ở Modal Volume `kgr1-webqsp-subset`, đường dẫn `/data/data_kg/webqsp/provenance.json`.

## Chuyển đổi

Script [prepare_webqsp_rog_subset_modal.py](../scripts_local/prepare_webqsp_rog_subset_modal.py) chuyển triple chuỗi từ RoG thành các chỉ số toàn cục mà `kg_r1.search.KnowledgeGraph` yêu cầu, rồi ghi:

```text
data_kg/webqsp/entities.txt
data_kg/webqsp/entities_text.txt
data_kg/webqsp/relations.txt
data_kg/webqsp/train_simple.json
data_kg/webqsp/test_simple.json
```

Script [build_webqsp_parquet_modal.py](../scripts_local/build_webqsp_parquet_modal.py) tạo `train.parquet` (300 dòng, 413.289 bytes) và `test.parquet` (100 dòng, 58.381 bytes). Prompt dùng `<search>`/`<information>`/`<answer>` theo repo thực thi, không dùng `<kg-query>` của paper.

