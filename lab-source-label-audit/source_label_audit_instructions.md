# Blinded source-label audit

Code each `added_text` without trying to infer the original regex label.

* `0` — no source, evidence, extraction, or verification statement.
* `1` — claims a source was checked, but gives no identifiable source or evidence.
* `2` — names an identifiable source, dataset, URL, tool output, or extraction route, but does not make the numeric support traceable.
* `3` — gives traceable evidence for the answer: e.g. a source plus the relevant value/row, a reproducible query, or an explicit extraction.
* `9` — cannot determine from the text.

For the primary validation, labels `2` and `3` count as a positive manual source/evidence label; `0` and `1` count as negative.  Preserve the audit ID and enter one label per row.  Two raters must work independently.  Do not open `source_label_audit_key.csv` until both completed files are saved.
