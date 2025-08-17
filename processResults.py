import sys
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

plt.rcParams.update({
    "font.family": "serif",
    "axes.titlesize": 18,
    "axes.labelsize": 15,
    "xtick.labelsize": 13,
    "ytick.labelsize": 13,
    "legend.fontsize": 12,
    "figure.titlesize": 20
})
# --- End Style Application ---

# Create folder for graphs
if not os.path.exists("output/figures"):
    os.makedirs("output/figures")

# Get file path from command line
if len(sys.argv) == 1:
    print("ProcessResults ERROR: No filepath provided in command line argument")
    sys.exit(-1)
elif len(sys.argv) > 2:
    print("ProcessResults ERROR: Provided more than 1 filepath")
    sys.exit(-1)
else:
    path = sys.argv[1]
    print(f"ProcessResults SUCCESS: Parsed {path}")

# Read all columns from the CSV
avgBalance = pd.read_csv(path, header=None, index_col=False)

print("Initial DataFrame head:")
print(avgBalance.head(2))
print(f"Number of columns read: {avgBalance.shape[1]}")

fixed_cols_map = {
    0: 'FileID',
    1: 'Time',
    2: 'Bid',
    3: 'Ask'
}
avgBalance.rename(columns=fixed_cols_map, inplace=True)

agent_avg_balance_cols_to_plot = []
dynamic_rename_map = {}
num_total_cols = avgBalance.shape[1]
first_agent_col_index = 4

if (num_total_cols - first_agent_col_index) < 0:
    print(f"ProcessResults WARNING: Not enough columns for any agent data. Expected at least {first_agent_col_index + 4} columns, got {num_total_cols}.")
elif (num_total_cols - first_agent_col_index) % 4 != 0:
    print(f"ProcessResults WARNING: Number of columns for agent data ({num_total_cols - first_agent_col_index}) is not a multiple of 4. Check CSV structure.")

num_agent_blocks = (num_total_cols - first_agent_col_index) // 4

for i in range(num_agent_blocks):
    agent_name_source_col_idx = first_agent_col_index + i * 4
    agent_avg_balance_data_col_idx = agent_name_source_col_idx + 3

    if agent_avg_balance_data_col_idx < num_total_cols:
        agent_name = avgBalance.iloc[0, agent_name_source_col_idx]
        if pd.isna(agent_name) or str(agent_name).strip() == "":
            print(f"ProcessResults WARNING: Agent name at original column index {agent_name_source_col_idx} is empty or NaN. Skipping this agent.")
            continue
        agent_name_str = str(agent_name).strip()
        dynamic_rename_map[agent_avg_balance_data_col_idx] = agent_name_str
        if agent_name_str not in agent_avg_balance_cols_to_plot:
            agent_avg_balance_cols_to_plot.append(agent_name_str)
    else:
        print(f"ProcessResults WARNING: Column index out of bounds when trying to identify agent block {i + 1}.")
        break

avgBalance.rename(columns=dynamic_rename_map, inplace=True)

print("\nDataFrame columns after dynamic renaming:")
print(avgBalance.columns)
print("Identified agent average balance columns to plot:", agent_avg_balance_cols_to_plot)

for col in ['Time', 'Bid', 'Ask']:
    if col in avgBalance.columns:
        avgBalance[col] = pd.to_numeric(avgBalance[col], errors='coerce').astype('Int32')

for agent_col_name in agent_avg_balance_cols_to_plot:
    if agent_col_name in avgBalance.columns:
        avgBalance[agent_col_name] = pd.to_numeric(avgBalance[agent_col_name], errors='coerce')
    else:
        print(f"ProcessResults WARNING: Column '{agent_col_name}' not found for numeric conversion. It might have been skipped.")

print("\nDataFrame dtypes after numeric conversion:")
print(avgBalance.dtypes)
print("\nNaN values before fillna:")
nan_counts = avgBalance.isnull().sum()
print(nan_counts[nan_counts > 0])
print("Filling NaN values with 0")
avgBalance.fillna(0, inplace=True)
print("\nNumber of NaN values after fillna:")
nan_counts_after = avgBalance.isnull().sum()
print(nan_counts_after[nan_counts_after > 0])

# --- Plotting Trading Bots Performance ---
if not agent_avg_balance_cols_to_plot:
    print("\nProcessResults WARNING: No agent average balance columns identified for plotting.")
else:
    print(f"\nPlotting performance for agents: {agent_avg_balance_cols_to_plot}")
    try:
        plt.figure(figsize=(12, 7))  # Adjusted figure size

        # Define a color palette
        # Using a qualitative palette good for distinct categories
        palette = sns.color_palette("deep", n_colors=len(agent_avg_balance_cols_to_plot))

        ax_bots = avgBalance.plot(x="Time", y=agent_avg_balance_cols_to_plot, kind="line",
                                  color=palette, linewidth=1.5, ax=plt.gca())  # Use plt.gca() to get current axes

        ax_bots.set_title("Trading Bot Performance Over Time", fontsize=plt.rcParams["axes.titlesize"])
        ax_bots.set_xlabel("Time (Number of Trades)", fontsize=plt.rcParams["axes.labelsize"])
        ax_bots.set_ylabel("Average Balance", fontsize=plt.rcParams["axes.labelsize"])

        # Customize legend
        ax_bots.legend(title="Agent Type", loc='upper left', frameon=True, facecolor='white', edgecolor='lightgray',
                       title_fontsize='13')

        # Customize grid and spines
        ax_bots.grid(axis='y', linestyle='--', alpha=0.7, linewidth=0.7)
        ax_bots.grid(axis='x', linestyle='--', alpha=0.5, linewidth=0.5)  # Optional: x-axis grid
        ax_bots.spines['top'].set_visible(False)
        ax_bots.spines['right'].set_visible(False)
        ax_bots.set_axisbelow(True)

        plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout
        plt.savefig("output/figures/bots_performance.png", dpi=300)
        plt.show(block=True)
    except Exception as e:
        print(f"Error plotting bot performance: {e}")
        print("Available columns for plotting:", avgBalance.columns)
        print("Data for Time column (first 5 rows):", avgBalance["Time"].head())
        for agent_col in agent_avg_balance_cols_to_plot:
            if agent_col in avgBalance.columns:
                print(f"Data for {agent_col} column (first 5 rows):", avgBalance[agent_col].head())
            else:
                print(f"Column {agent_col} not found in DataFrame for plotting.")

# --- Plotting Bid and Ask Prices ---
if 'Time' in avgBalance.columns and 'Bid' in avgBalance.columns and 'Ask' in avgBalance.columns:
    try:
        plt.figure(figsize=(12, 7))  # Adjusted figure size

        # Define specific colors for Bid and Ask
        bid_color = sns.color_palette("deep")[0]  # Example: blue
        ask_color = sns.color_palette("deep")[3]  # Example: red

        ax_prices = avgBalance.plot(x="Time", y=["Bid", "Ask"], kind="line",
                                    color=[bid_color, ask_color], linewidth=1.5, ax=plt.gca())

        ax_prices.set_title("Bid and Ask Prices Over Time", fontsize=plt.rcParams["axes.titlesize"])
        ax_prices.set_xlabel("Time (Number of Trades)", fontsize=plt.rcParams["axes.labelsize"])
        ax_prices.set_ylabel("Price", fontsize=plt.rcParams["axes.labelsize"])

        # Customize legend
        ax_prices.legend(["Bid Price", "Ask Price"], loc='upper right', frameon=True, facecolor='white',
                         edgecolor='lightgray')

        # Customize grid and spines
        ax_prices.grid(axis='y', linestyle='--', alpha=0.7, linewidth=0.7)
        ax_prices.grid(axis='x', linestyle='--', alpha=0.5, linewidth=0.5)  # Optional: x-axis grid
        ax_prices.spines['top'].set_visible(False)
        ax_prices.spines['right'].set_visible(False)
        ax_prices.set_axisbelow(True)

        plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout
        plt.savefig("output/figures/bid_ask_prices.png", dpi=300)
        plt.show(block=True)
    except Exception as e:
        print(f"Error plotting bid/ask prices: {e}")
else:
    print("\nProcessResults WARNING: 'Time', 'Bid', or 'Ask' columns not available for plotting bid/ask prices.")

print("\nProcessResults: Script finished.")