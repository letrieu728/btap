from pathlib import Path
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'figures' / 'final_reproduction_summary.png'

fig, axes = plt.subplots(1, 2, figsize=(11, 5.7))
fig.patch.set_facecolor('#f8fafc')

ax = axes[0]
ax.set_facecolor('#f8fafc')
labels = ['β = 1.68', 'β = 3.9']
form = [0.141, 0.242]
name = [0.193, 0.438]
x = [0, 1]
ax.bar([v - .18 for v in x], form, .36, label='Form', color='#2f6f9f')
ax.bar([v + .18 for v in x], name, .36, label='Name', color='#e38b3a')
ax.set_xticks(x, labels)
ax.set_ylim(0, .52)
ax.set_ylabel('Median distance from prior at s = 0.10')
ax.set_title('1. Beta rerun: stronger copying\ncreates larger deviation when prior is weak', loc='left', weight='bold')
ax.legend(frameon=False)
ax.text(0, .49, '50 seeds per β • local CPU • no LLM/API', fontsize=9, color='#475569')
for series, offset in ((form, -.18), (name, .18)):
    for i, value in enumerate(series):
        ax.text(i + offset, value + .014, f'{value:.3f}', ha='center', fontsize=9)

ax = axes[1]
ax.set_facecolor('#f8fafc')
vals = [33, 3, 0, 40]
cols = ['#25846a', '#d97706', '#dc2626', '#64748b']
bars = ax.bar(['TP', 'FP', 'FN', 'TN'], vals, color=cols)
ax.set_ylim(0, 45)
ax.set_ylabel('Number of consensus items (n = 76)')
ax.set_title('2. Source-label audit: regex is sensitive,\nbut has a few false positives', loc='left', weight='bold')
for bar, value in zip(bars, vals):
    ax.text(bar.get_x() + bar.get_width()/2, value + .8, str(value), ha='center', weight='bold')
ax.text(-.48, 42, 'Precision 0.917   •   Recall 1.000\n1 human rater + AI rater; not two-human reliability', fontsize=9, color='#475569')

for ax in axes:
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis='y', alpha=.18)
fig.suptitle('Reproduction & validation summary', x=.08, ha='left', fontsize=16, weight='bold')
fig.tight_layout(rect=(0, 0, 1, .93))
fig.savefig(OUT, dpi=220, bbox_inches='tight')
print(OUT)
