import sys
import pandas as pd
import os


def calculate_and_print_stats(filepath):
    """
    Reads a CSV file, identifies agent average balance columns,
    and prints descriptive statistics for each agent.
    """
    try:
        # Read all columns from the CSV
        # Pandas will assign default integer column names (0, 1, 2, ...)
        data_df = pd.read_csv(filepath, header=None, index_col=False)
    except FileNotFoundError:
        print(f"ERROR: File not found at {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Could not read CSV file {filepath}. Reason: {e}")
        sys.exit(1)

    print("Initial DataFrame head:")
    print(data_df.head(2))
    print(f"Number of columns read: {data_df.shape[1]}")

    # Define fixed column names for the initial part of the data
    fixed_cols_map = {
        0: 'FileID',
        1: 'Time',
        2: 'Bid',
        3: 'Ask'
    }
    data_df.rename(columns=fixed_cols_map, inplace=True)

    # Identify agent columns and their average balance columns
    agent_avg_balance_cols_for_stats = []
    dynamic_rename_map = {}  # Maps original integer column indices to new agent names for avg balance

    num_total_cols = data_df.shape[1]
    first_agent_col_index = 4  # Starting index of the first agent's data block

    if (num_total_cols - first_agent_col_index) < 0:
        print(
            f"WARNING: Not enough columns for any agent data. Expected at least {first_agent_col_index + 4} columns, got {num_total_cols}.")
    elif (num_total_cols - first_agent_col_index) % 4 != 0:
        # This warning might appear if there's a trailing comma in the CSV,
        # leading to an extra empty column. The logic should still correctly
        # identify complete agent blocks.
        print(
            f"WARNING: Number of columns for agent data ({num_total_cols - first_agent_col_index}) is not a multiple of 4. This might be due to a trailing comma or malformed CSV. Proceeding with complete blocks.")

    num_agent_blocks = (num_total_cols - first_agent_col_index) // 4

    for i in range(num_agent_blocks):
        agent_name_source_col_idx = first_agent_col_index + i * 4
        agent_avg_balance_data_col_idx = agent_name_source_col_idx + 3

        if agent_avg_balance_data_col_idx < num_total_cols:
            agent_name = data_df.iloc[0, agent_name_source_col_idx]

            if pd.isna(agent_name) or str(agent_name).strip() == "":
                print(
                    f"WARNING: Agent name at original column index {agent_name_source_col_idx} is empty or NaN. Skipping this agent.")
                continue

            agent_name_str = str(agent_name).strip()

            # Map the original integer index of the average balance column to the agent's name
            dynamic_rename_map[agent_avg_balance_data_col_idx] = agent_name_str
            if agent_name_str not in agent_avg_balance_cols_for_stats:
                agent_avg_balance_cols_for_stats.append(agent_name_str)
        else:
            print(f"WARNING: Column index out of bounds when trying to identify agent block {i + 1}.")
            break

    # Rename the identified agent average balance columns
    data_df.rename(columns=dynamic_rename_map, inplace=True)

    print("\nDataFrame columns after dynamic renaming:")
    print(data_df.columns)
    print("Identified agent average balance columns for statistics:", agent_avg_balance_cols_for_stats)

    # Convert agent average balance columns to numeric (float)
    for agent_col_name in agent_avg_balance_cols_for_stats:
        if agent_col_name in data_df.columns:
            data_df[agent_col_name] = pd.to_numeric(data_df[agent_col_name], errors='coerce')
        else:
            print(
                f"WARNING: Column '{agent_col_name}' not found for numeric conversion. It might have been skipped or misidentified.")

    print("\nDataFrame dtypes after numeric conversion (showing relevant columns):")
    relevant_dtypes = {col: data_df[col].dtype for col in agent_avg_balance_cols_for_stats if col in data_df.columns}
    print(pd.Series(relevant_dtypes))

    if not agent_avg_balance_cols_for_stats:
        print("\nERROR: No agent average balance columns identified for statistics.")
        return

    # Calculate descriptive statistics for each agent's average balance
    all_agent_stats = {}
    for agent_name in agent_avg_balance_cols_for_stats:
        if agent_name in data_df.columns:
            # .describe() handles NaNs by excluding them from calculations by default
            stats = data_df[agent_name].describe()
            all_agent_stats[agent_name] = stats
        else:
            print(f"WARNING: Column '{agent_name}' was expected but not found in DataFrame for statistics calculation.")

    if not all_agent_stats:
        print("\nERROR: Could not calculate statistics for any agent.")
        return

    # Convert the dictionary of Series to a DataFrame for nice printing
    # Each agent will be a column, and stats (mean, std, etc.) will be rows.
    stats_df = pd.DataFrame(all_agent_stats)

    print("\nDescriptive Statistics for Agent Average Balances:")
    print(stats_df)

    # Save the DataFrame to a CSV file
    try:
        output_filename = "agent_stats_summary.csv"
        if not os.path.exists("output/raw"):
            os.makedirs("output/raw")
        stats_df.to_csv("output/raw/"+output_filename)
        print(f"\nSuccessfully saved agent statistics to {output_filename}")
    except Exception as e:
        print(f"\nERROR: Could not save statistics to CSV. Reason: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERROR: No filepath provided.")
        print("Usage: python calculate_agent_stats.py <path_to_csv_file>")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("ERROR: Too many arguments provided.")
        print("Usage: python calculate_agent_stats.py <path_to_csv_file>")
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"ERROR: The file '{filepath}' does not exist.")
        sys.exit(1)

    print(f"Processing file: {filepath}")
    calculate_and_print_stats(filepath)