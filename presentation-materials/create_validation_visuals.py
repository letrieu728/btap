"""Draw a presentation-ready overview of the two zero/new-cost validation extensions."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'figures' / 'proposed_validation_overview.png'

INK, SLATE, TEAL, AMBER, ROSE, PALE = '#172033', '#52606d', '#087e8b', '#e89b25', '#b94a63', '#edf4f6'


def box(ax, xy, w, h, text, color=PALE, edge=TEAL, size=10, weight='normal'):
    patch = FancyBboxPatch(xy, w, h, boxstyle='round,pad=0.012,rounding_size=0.025',
                           facecolor=color, edgecolor=edge, linewidth=1.2)
    ax.add_patch(patch)
    ax.text(xy[0] + w / 2, xy[1] + h / 2, text, ha='center', va='center', fontsize=size,
            color=INK, fontweight=weight, wrap=True)


def arrow(ax, start, end, color=SLATE):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle='-|>', mutation_scale=13, linewidth=1.25, color=color))


def main():
    fig = plt.figure(figsize=(16, 9), facecolor='white')
    fig.text(0.5, 0.955, 'Hai kiểm định đề xuất cho “Copying explains the collective behavior of AI agents”',
             ha='center', va='center', fontsize=19, fontweight='bold', color=INK)
    fig.text(0.5, 0.918, 'Mục tiêu: tách cơ chế nhân quả và kiểm tra độ tin cậy của phép đo trong Figure 4',
             ha='center', va='center', fontsize=11.5, color=SLATE)

    left = fig.add_axes((0.05, 0.15, 0.43, 0.71)); left.set_axis_off(); left.set(xlim=(0, 1), ylim=(0, 1))
    right = fig.add_axes((0.52, 0.15, 0.43, 0.71)); right.set_axis_off(); right.set(xlim=(0, 1), ylim=(0, 1))
    for ax, number, title, subtitle in (
        (left, '1', 'Tách “đồng thuận” khỏi “đã kiểm chứng nguồn”', 'Mở rộng trực tiếp cơ chế được gợi ý bởi Figure 4'),
        (right, '2', 'Audit mù nhãn “đã kiểm tra nguồn”', 'Kiểm định cách Figure 4 đo hành vi kiểm chứng trong dữ liệu thực'),
    ):
        ax.text(0.01, 0.97, number, ha='center', va='center', fontsize=18, color='white', fontweight='bold',
                bbox=dict(boxstyle='circle,pad=0.25', fc=TEAL, ec='none'))
        ax.text(0.07, 0.975, title, ha='left', va='center', fontsize=14, color=INK, fontweight='bold')
        ax.text(0.07, 0.925, subtitle, ha='left', va='center', fontsize=9.5, color=SLATE)

    # Left: 2x2 factor matrix
    left.text(0.43, 0.835, 'Nội dung ghi chú sai', ha='center', fontsize=10, color=SLATE)
    left.text(0.40, 0.785, 'Không nêu nguồn', ha='center', fontsize=10, color=INK, fontweight='bold')
    left.text(0.72, 0.785, 'Tuyên bố “đã kiểm chứng”', ha='center', fontsize=10, color=INK, fontweight='bold')
    left.text(0.055, 0.615, '2 ghi chú\n(đồng thuận ít)', ha='center', va='center', fontsize=9.2, color=INK)
    left.text(0.055, 0.405, '12 ghi chú\n(đồng thuận nhiều)', ha='center', va='center', fontsize=9.2, color=INK)
    cells = [
        (0.18, 0.54, '2× “Hungary 9.90%”\nKhông nêu nguồn'),
        (0.53, 0.54, '2× “Hungary 9.90%”\n“Nguồn đã kiểm chứng”'),
        (0.18, 0.33, '12× “Hungary 9.90%”\nKhông nêu nguồn'),
        (0.53, 0.33, '12× “Hungary 9.90%”\n“Nguồn đã kiểm chứng”'),
    ]
    for x, y, label in cells:
        box(left, (x, y), 0.28, 0.14, label, color='#fff7e8' if x > .5 else PALE,
            edge=AMBER if x > .5 else TEAL, size=9)
    box(left, (0.27, 0.12), 0.50, 0.105, 'Đo chính: agent có mở workbook nguồn trước khi trả lời?',
        color='#e9f6f5', edge=TEAL, size=10, weight='bold')
    arrow(left, (0.48, 0.52), (0.49, 0.24))
    left.text(0.52, 0.05, 'Hiệu ứng tương tác ⇒ số đông hay tín hiệu nguồn là cơ chế chính?',
              ha='center', fontsize=9.3, color=SLATE, style='italic')

    # Right: audit pipeline
    box(right, (0.08, 0.68), 0.22, 0.13, '325 lượt trả lời OECD\nđúng tập Figure 4', size=10, weight='bold')
    box(right, (0.39, 0.68), 0.25, 0.13, 'Phân tầng theo\ntrước/sau sửa sai × regex', color='#fff7e8', edge=AMBER, size=10)
    box(right, (0.73, 0.68), 0.19, 0.13, '77 mẫu mù\nkhông lộ nhãn regex', color='#f9edf0', edge=ROSE, size=10, weight='bold')
    arrow(right, (0.30, .745), (.385, .745)); arrow(right, (.64, .745), (.725, .745))
    box(right, (0.18, 0.41), 0.23, 0.12, 'Người chấm 1\n0 / 1 / 2 / 3 / 9', size=10)
    box(right, (0.59, 0.41), 0.23, 0.12, 'Người chấm 2\n0 / 1 / 2 / 3 / 9', size=10)
    arrow(right, (.80, .68), (.32, .54)); arrow(right, (.84, .68), (.70, .54))
    box(right, (0.26, 0.17), 0.48, 0.13, 'Cohen’s κ: hai người có đồng ý?\nPrecision / recall: regex có đo đúng\n“nguồn/evidence” không?',
        color='#e9f6f5', edge=TEAL, size=9.2, weight='bold')
    arrow(right, (.30, .41), (.43, .30)); arrow(right, (.70, .41), (.57, .30))
    right.text(0.50, 0.055, 'Kết quả tốt ⇒ củng cố Figure 4  •  Kết quả kém ⇒ giới hạn diễn giải',
               ha='center', fontsize=9.2, color=SLATE, style='italic')
    fig.text(0.5, 0.055, 'Thiết kế và bộ audit đã được tạo; chưa có kết quả LLM hoặc kết quả chấm thủ công mới.',
             ha='center', fontsize=9, color=SLATE)
    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT, dpi=200, bbox_inches='tight')
    print('wrote proposed_validation_overview.png')


if __name__ == '__main__':
    main()
