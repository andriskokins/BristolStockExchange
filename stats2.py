import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    "font.family": "serif",
    "axes.titlesize": 18,
    "axes.labelsize": 15,
    "xtick.labelsize": 13,
    "ytick.labelsize": 13,
    "legend.fontsize": 13
})

agents = ['GVWY', 'SHVR', 'SNPR', 'ZIC', 'ZIP']

# Mean profit for each agent, in order:
# [run 6, ratio 20:80], [run 6, ratio 80:20], [run 7, ratio 20:80], [run 7, ratio 80:20]
means = {
    'GVWY': [467.55, 485.58, 406.26, 487.04],
    'SHVR': [460.16, 448.24, 559.88, 441.15],
    'SNPR': [23.43, 23.52, 22.00, 24.24],
    'ZIC': [255.29, 167.37, 229.47, 201.24],
    'ZIP': [402.35, 414.54, 948.40, 416.72]}

stds = {
    'GVWY': [262.63, 279.07, 234.21, 274.98],
    'SHVR': [259.77, 253.25, 312.41, 243.01],
    'SNPR': [48.01, 48.89, 46.41, 49.67],
    'ZIC': [146.54, 96.13, 147.78, 107.26],
    'ZIP': [228.22, 229.53, 539.52, 235.52]}

mins = {
    'GVWY': [0.00, 1.93, 0.04, 0.47],
    'SHVR': [0.00, 0.00, 0.00, 0.00],
    'SNPR': [0.00, 0.00, 0.00, 0.00],
    'ZIC': [0.38, 0.00, 0.00, 0.00],
    'ZIP': [0.00, 0.00, 0.53, 0.00]}

q1s = {
    'GVWY': [236.47, 244.53, 199.16, 247.70],
    'SHVR': [229.55, 228.10, 288.40, 227.40],
    'SNPR': [0.00, 0.00, 0.00, 0.00],
    'ZIC': [128.97, 79.22, 102.60, 114.60],
    'ZIP': [206.20, 224.00, 478.58, 210.36]}

medians = {
    'GVWY': [477.53, 486.13, 405.76, 496.49],
    'SHVR': [471.21, 451.47, 579.40, 450.60],
    'SNPR': [0.00, 0.00, 0.00, 0.00],
    'ZIC': [253.45, 169.89, 206.60, 202.60],
    'ZIP': [410.00, 423.00, 958.88, 421.22]}

q3s = {
    'GVWY': [719.07, 746.27, 616.21, 741.93],
    'SHVR': [697.26, 681.96, 844.00, 657.40],
    'SNPR': [6.02, 0.00, 0.00, 6.50],
    'ZIC': [389.36, 260.32, 361.60, 309.20],
    'ZIP': [610.00, 618.60, 1428.11, 634.52]}

maxs = {
    'GVWY': [879.00, 939.60, 796.22, 928.16],
    'SHVR': [876.75, 859.50, 1063.80, 843.40],
    'SNPR': [182.44, 188.62, 176.46, 191.08],
    'ZIC': [497.26, 317.82, 492.60, 356.00],
    'ZIP': [771.20, 787.00, 1856.81, 798.88]}

# Calculate averages for plotting
avg_means = [np.mean(means[agent]) for agent in agents]
avg_stds = [np.mean(stds[agent]) for agent in agents]
avg_mins = [np.mean(mins[agent]) for agent in agents]
avg_q1s = [np.mean(q1s[agent]) for agent in agents]
avg_medians = [np.mean(medians[agent]) for agent in agents]
avg_q3s = [np.mean(q3s[agent]) for agent in agents]
avg_maxs = [np.mean(maxs[agent]) for agent in agents]

# Calculate 95% confidence intervals for means
n_runs = 5  # Number of runs
confidence_intervals = [1.96 * (np.std(means[agent], ddof=1) / np.sqrt(n_runs)) for agent in agents]

# Print calculated values for verification
print("Average statistics across all runs:")
for i, agent in enumerate(agents):
    print(
        f"{agent}: Mean={avg_means[i]:.2f}, Median={avg_medians[i]:.2f}, Min={avg_mins[i]:.2f}, Max={avg_maxs[i]:.2f}")

# Plotting
positions = np.arange(len(agents))
fig, ax = plt.subplots(figsize=(12, 9))

# Draw box (IQR: Q1 to Q3)
for i in range(len(agents)):
    ax.add_patch(plt.Rectangle(
        (positions[i] - 0.18, avg_q1s[i]), 0.36, avg_q3s[i] - avg_q1s[i],
        color='#5BA4CF', alpha=0.6, zorder=1, label='_nolegend_'
    ))

# Whiskers: Min to Q1, Q3 to Max
for i in range(len(agents)):
    # Lower whisker
    ax.plot([positions[i], positions[i]], [avg_mins[i], avg_q1s[i]], color='black', lw=2, zorder=2)
    # Upper whisker
    ax.plot([positions[i], positions[i]], [avg_q3s[i], avg_maxs[i]], color='black', lw=2, zorder=2)
    # Whisker end caps
    ax.plot([positions[i] - 0.07, positions[i] + 0.07], [avg_mins[i], avg_mins[i]], color='black', lw=2, zorder=2)
    ax.plot([positions[i] - 0.07, positions[i] + 0.07], [avg_maxs[i], avg_maxs[i]], color='black', lw=2, zorder=2)

# Median line
for i in range(len(agents)):
    ax.plot([positions[i] - 0.18, positions[i] + 0.18], [avg_medians[i], avg_medians[i]], color='red', lw=3, zorder=3,
            label='_nolegend_')

# Mean marker and annotation with 95% confidence intervals
for i in range(len(agents)):
    ax.plot(positions[i], avg_means[i], marker='o', color='navy', markersize=10, zorder=4, label='_nolegend_')

    # Error bars for 95% confidence interval
    ax.errorbar(positions[i], avg_means[i], yerr=confidence_intervals[i],
                fmt='none', ecolor='navy', capsize=5, zorder=3)

    # Mean value annotation
    ax.annotate(f"{avg_means[i]:.1f}", (positions[i], avg_means[i]),
                textcoords="offset points", xytext=(0, 8),
                ha='center', fontsize=11, fontweight='bold', color='navy')

# Annotate min, Q1, median, Q3, max
for i in range(len(agents)):
    # Min
    ax.annotate(f"min\n{avg_mins[i]:.1f}", (positions[i] + 0.22, avg_mins[i]), va='center', ha='left', fontsize=9,
                color='gray')
    # Q1
    ax.annotate(f"Q1\n{avg_q1s[i]:.1f}", (positions[i] + 0.22, avg_q1s[i]), va='center', ha='left', fontsize=9,
                color='#5BA4CF')
    # Median
    ax.annotate(f"median\n{avg_medians[i]:.1f}", (positions[i] + 0.22, avg_medians[i]), va='center', ha='left',
                fontsize=9, color='red')
    # Q3
    ax.annotate(f"Q3\n{avg_q3s[i]:.1f}", (positions[i] + 0.22, avg_q3s[i]), va='center', ha='left', fontsize=9,
                color='#5BA4CF')
    # Max
    ax.annotate(f"max\n{avg_maxs[i]:.1f}", (positions[i] + 0.22, avg_maxs[i]), va='center', ha='left', fontsize=9,
                color='gray')

# Axes and title
ax.set_xticks(positions)
ax.set_xticklabels(agents, fontsize=14)
ax.set_ylabel('Profit', fontsize=16)
ax.set_xlabel('Agent Type', fontsize=16)
ax.set_title('Agent Profit Distribution Across All Experimental Runs', fontsize=18, pad=16)
ax.grid(axis='y', linestyle='--', alpha=0.7)
ax.set_axisbelow(True)

# Custom legend
import matplotlib.patches as mpatches

legend_elements = [
    mpatches.Patch(color='#5BA4CF', label='IQR (Q1–Q3)'),
    plt.Line2D([0], [0], color='red', lw=3, label='Median'),
    plt.Line2D([0], [0], color='navy', marker='o', linestyle='None', markersize=10, label='Mean w/ 95% CI')
]
ax.legend(handles=legend_elements, loc='upper left', frameon=True)

ax.set_xlim(-0.5, len(agents) - 0.5)
plt.tight_layout()
# plt.savefig('agent_profit_summary.pdf', dpi=500, bbox_inches='tight')
plt.savefig('agent_profit_summary.png', dpi=2000, bbox_inches='tight')
plt.show()