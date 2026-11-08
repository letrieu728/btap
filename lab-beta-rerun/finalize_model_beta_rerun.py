"""Finish the Windows-safe beta rerun after its simulation cache is available."""
import pickle
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / 'cache' / 'model_beta_rerun_50seed.pkl'
REPORT = ROOT / 'reports' / 'model_beta_rerun_50seed.md'


def main():
    deadline = time.monotonic() + 7200
    while not CACHE.exists():
        if time.monotonic() >= deadline:
            raise TimeoutError(f'Cache was not created within two hours: {CACHE}')
        time.sleep(20)
    with CACHE.open('rb') as handle:
        sims = pickle.load(handle)
    counts = {}
    for beta in (1.68, 3.9):
        if beta not in sims:
            raise ValueError(f'Missing beta={beta}')
        form = next(values for key, values in sims[beta].items() if key[0] == 'form')
        counts[beta] = len(form['final'])
        if counts[beta] != 50:
            raise ValueError(f'beta={beta} has {counts[beta]} runs, expected 50')
    subprocess.run([
        sys.executable, str(ROOT / 'lab' / 'ed_model_beta.py'),
        '--input', CACHE.name,
        '--output', 'ed_model_beta_rerun_50seed.png',
        '--pdf-output', 'ed_model_beta_rerun_50seed.pdf',
    ], cwd=ROOT, check=True)
    REPORT.write_text(
        '# Tái chạy beta: kiểm định hoàn tất\n\n'
        'Mô phỏng S-shaped copying chạy tuần tự trên Windows, không dùng LLM/API. '
        'Cache và biểu đồ được đặt tên `*_rerun_50seed` để không thay thế kết quả tác giả.\n\n'
        f'- β = 1.68: {counts[1.68]} seed hợp lệ\n'
        f'- β = 3.9: {counts[3.9]} seed hợp lệ\n'
        '- Kết luận: tái chạy hoàn tất về mặt cấu trúc; đối chiếu định lượng dùng ảnh mới cùng ảnh tác giả.\n',
        encoding='utf-8')
    print('finalized beta rerun')


if __name__ == '__main__':
    main()
