"""Create and score a blinded, no-LLM audit of Figure 4's source label.

Figure 4 calls an edit a source/evidence check when its added text matches a
keyword regex.  This tool draws a deterministic stratified sample of the exact
OECD answer uses on which that field is computed.  The blind file intentionally
does not contain the regex label.  Two human raters can code it independently,
then ``score`` reports agreement and the regex's precision/recall.

    python lab/source_label_audit.py make
    python lab/source_label_audit.py score audits/rater_1.csv audits/rater_2.csv
"""
import argparse
import csv
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parent / 'src'))
import answers_oecd as ao  # noqa: E402
import conventions as cv  # noqa: E402
from common import Dataset, T  # noqa: E402

ALERT = T('2026-06-20T03:41:17').timestamp()
SRC = (r'xlsx|workbook|power ?bi|\bPBI\b|tooltip|querydata|sdmx|\braw\b|parsed|extracted|intercept|verified|aria|render'
       r'|9\.9124|16\.376|14\.587|9\.694|23\.130')
OUT = ROOT / 'audits'


def population():
    """The same edited-answer population and regex label used by Fig. 4."""
    ds = Dataset()
    idx, forms = cv.sequence(ds.revs, ao.NAME)
    per_page = {}
    rows = []
    for ordinal, (i, form) in enumerate(zip(idx, forms), 1):
        revision = ds.revs[i]
        prior_wrong, prior_right = per_page.get(revision['page_id'], (0, 0))
        added = revision.get('added') or ''
        rows.append(dict(
            audit_id=f'OECD-{ordinal:03d}', rev_id=revision['rev_id'], page_id=revision['page_id'],
            time=revision['time'], period='before_first_correction' if T(revision['time']).timestamp() < ALERT else 'after_first_correction',
            prior_notes=prior_wrong + prior_right, answer_form='wrong_padded' if form == 0 else 'right_raw',
            regex_source_label=int(bool(re.search(SRC, added, re.I))), added_text=added,
        ))
        per_page[revision['page_id']] = (prior_wrong + (form == 0), prior_right + (form == 1))
    return rows


def sample_rows(rows, per_stratum, seed):
    """Balanced across period × regex label; retain all items if a stratum is smaller."""
    rng = random.Random(seed)
    buckets = {}
    for row in rows:
        buckets.setdefault((row['period'], row['regex_source_label']), []).append(row)
    chosen = []
    for key, group in sorted(buckets.items()):
        chosen.extend(rng.sample(group, min(per_stratum, len(group))))
    rng.shuffle(chosen)
    return chosen, {f'{period}|regex={label}': len(group) for (period, label), group in buckets.items()}


def make(args):
    rows = population()
    chosen, counts = sample_rows(rows, args.per_stratum, args.seed)
    OUT.mkdir(exist_ok=True)
    blind = OUT / 'source_label_audit_blind.csv'
    key = OUT / 'source_label_audit_key.csv'
    instructions = OUT / 'source_label_audit_instructions.md'
    with blind.open('w', newline='', encoding='utf-8') as f:
        fields = ['audit_id', 'period', 'prior_notes', 'answer_form', 'added_text', 'rater_label', 'rater_comment']
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in chosen:
            writer.writerow({k: row.get(k, '') for k in fields})
    with key.open('w', newline='', encoding='utf-8') as f:
        fields = ['audit_id', 'rev_id', 'page_id', 'time', 'period', 'prior_notes', 'answer_form', 'regex_source_label']
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in chosen:
            writer.writerow({k: row[k] for k in fields})
    instructions.write_text("""# Blinded source-label audit

Code each `added_text` without trying to infer the original regex label.

* `0` — no source, evidence, extraction, or verification statement.
* `1` — claims a source was checked, but gives no identifiable source or evidence.
* `2` — names an identifiable source, dataset, URL, tool output, or extraction route, but does not make the numeric support traceable.
* `3` — gives traceable evidence for the answer: e.g. a source plus the relevant value/row, a reproducible query, or an explicit extraction.
* `9` — cannot determine from the text.

For the primary validation, labels `2` and `3` count as a positive manual source/evidence label; `0` and `1` count as negative.  Preserve the audit ID and enter one label per row.  Two raters must work independently.  Do not open `source_label_audit_key.csv` until both completed files are saved.
""", encoding='utf-8')
    print(json.dumps(dict(population=len(rows), available_strata=counts, sampled=len(chosen),
                          blind=str(blind), key=str(key), instructions=str(instructions)), indent=2))


def read_ratings(path):
    with Path(path).open(newline='', encoding='utf-8-sig') as f:
        out = {}
        for row in csv.DictReader(f):
            if row.get('audit_id') and str(row.get('rater_label', '')).strip():
                out[row['audit_id']] = int(row['rater_label'])
    return out


def binary(label):
    return None if label == 9 else int(label >= 2)


def cohen_kappa(a, b):
    pairs = [(a[k], b[k]) for k in a.keys() & b.keys() if a[k] != 9 and b[k] != 9]
    if not pairs:
        return float('nan'), 0
    observed = sum(x == y for x, y in pairs) / len(pairs)
    ca, cb = Counter(x for x, _ in pairs), Counter(y for _, y in pairs)
    expected = sum(ca[v] / len(pairs) * cb[v] / len(pairs) for v in set(ca) | set(cb))
    return (observed - expected) / (1 - expected) if expected < 1 else float('nan'), len(pairs)


def score(paths):
    if len(paths) != 2:
        raise SystemExit('Provide exactly two completed rater CSV files.')
    key_path = OUT / 'source_label_audit_key.csv'
    if not key_path.exists():
        raise SystemExit('Run make first.')
    with key_path.open(newline='', encoding='utf-8') as f:
        key = {r['audit_id']: r for r in csv.DictReader(f)}
    r1, r2 = map(read_ratings, paths)
    kappa, n_agree = cohen_kappa(r1, r2)
    consensus = {}
    for audit_id in key:
        a, b = r1.get(audit_id), r2.get(audit_id)
        if a is not None and b is not None and a == b and binary(a) is not None:
            consensus[audit_id] = binary(a)
    tp = fp = fn = tn = 0
    for audit_id, manual in consensus.items():
        regex = int(key[audit_id]['regex_source_label'])
        if regex and manual: tp += 1
        elif regex: fp += 1
        elif manual: fn += 1
        else: tn += 1
    precision = tp / (tp + fp) if tp + fp else float('nan')
    recall = tp / (tp + fn) if tp + fn else float('nan')
    print(json.dumps(dict(rater_1_completed=len(r1), rater_2_completed=len(r2), exact_agreement_n=n_agree,
                          cohen_kappa=round(kappa, 3), consensus_n=len(consensus), confusion_matrix=dict(tp=tp, fp=fp, fn=fn, tn=tn),
                          regex_precision=round(precision, 3), regex_recall=round(recall, 3)), indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p_make = sub.add_parser('make')
    p_make.add_argument('--per-stratum', type=int, default=20)
    p_make.add_argument('--seed', type=int, default=20261106)
    p_score = sub.add_parser('score')
    p_score.add_argument('ratings', nargs='+')
    args = parser.parse_args()
    make(args) if args.command == 'make' else score(args.ratings)


if __name__ == '__main__':
    main()
