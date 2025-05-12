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

# Agent summary statistics (raw data from all runs)
agents = ['GVWY', 'SHVR', 'SNPR', 'ZIC', 'ZIP']
means = {
    'GVWY': [757.15, 674.80, 672.28, 672.09, 676.85],
    'SHVR': [831.66, 807.20, 780.75, 781.58, 765.36],
    'SNPR': [43.93, 33.33, 33.72, 29.70, 28.41],
    'ZIC': [259.26, 241.26, 270.01, 249.76, 232.04],
    'ZIP': [782.88, 759.32, 723.56, 723.70, 403.90]
}

stds = {
    'GVWY': [415.27, 387.09, 387.70, 389.15, 388.11],
    'SHVR': [452.53, 458.14, 448.31, 448.83, 440.50],
    'SNPR': [79.13, 72.73, 72.98, 68.14, 65.57],
    'ZIC': [144.84, 141.68, 162.80, 145.04, 141.54],
    'ZIP': [426.94, 426.42, 412.47, 421.23, 403.90]
}

mins = {
    'GVWY': [0.00, 0.37, 0.73, 0.09, 0.35],
    'SHVR': [0.00, 0.00, 0.00, 0.00, 0.00],
    'SNPR': [0.00, 0.00, 0.00, 0.00, 0.00],
    'ZIC': [0.00, 0.00, 0.00, 0.00, 0.00],
    'ZIP': [0.07, 0.00, 0.11, 0.00, 0.00]
}

q1s = {
    'GVWY': [389.80, 338.99, 332.03, 335.96, 338.69],
    'SHVR': [437.96, 409.59, 391.53, 392.02, 384.98],
    'SNPR': [0.00, 0.00, 0.00, 0.00, 0.00],
    'ZIC': [132.63, 118.16, 124.70, 122.62, 123.20],
    'ZIP': [408.92, 399.34, 365.36, 357.46, 355.40]
}

medians = {
    'GVWY': [784.17, 676.83, 682.13, 670.84, 680.73],
    'SHVR': [866.75, 814.59, 778.83, 787.19, 767.41],
    'SNPR': [0.00, 0.00, 0.00, 0.00, 0.00],
    'ZIC': [263.37, 239.92, 267.20, 251.67, 230.00],
    'ZIP': [815.09, 762.20, 726.59, 722.57, 705.83]
}

q3s = {
    'GVWY': [1155.20, 1023.32, 1024.70, 1012.45, 1018.67],
    'SHVR': [1250.29, 1216.23, 1179.87, 1170.92, 1154.11],
    'SNPR': [55.54, 0.00, 0.00, 0.00, 0.00],
    'ZIC': [400.73, 365.11, 413.00, 375.46, 340.00],
    'ZIP': [1179.74, 1144.00, 1089.96, 1089.17, 1054.83]
}

maxs = {
    'GVWY': [1363.07, 1316.55, 1319.00, 1341.18, 1335.65],
    'SHVR': [1513.49, 1566.76, 1545.03, 1552.57, 1524.22],
    'SNPR': [272.84, 280.90, 279.70, 283.10, 267.60],
    'ZIC': [474.57, 484.09, 534.90, 505.07, 480.20],
    'ZIP': [1417.46, 1457.70, 1411.99, 1446.62, 1390.67]
}

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
plt.savefig('agent_profit_summary.png', dpi=500, bbox_inches='tight')
plt.show()