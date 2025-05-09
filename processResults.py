import pandas as pd
import string
import matplotlib.pyplot as plt
import os

# Create folder for graphs
if not os.path.exists("graphs"):
    os.makedirs("graphs")

print(list(string.ascii_uppercase)[0:22])

avgBalance = pd.read_csv("bse_d000_i05_0001_avg_balance.csv", header=None,\
                         names=list(string.ascii_uppercase)[0:22],\
                         index_col=False)

print(avgBalance.head())

# Use the original working column mapping
newNames = { "H":"GVWY", "L":"SHVR", "P":"ZIC", "T":"ZIP"}
avgBalance.rename(columns=newNames,inplace=True)

print(avgBalance.columns)  # See all column names
print(avgBalance.dtypes)   # Check data types for each column

# Data cleaning
# Convert to int32 types
for col in ['B', 'C', 'D']:
    avgBalance[col] = pd.to_numeric(avgBalance[col], errors='coerce').astype('Int32')

# Print NaN values
print("NaN values")
print((avgBalance.isnull().sum())[avgBalance.isnull().sum() > 0])
# Delete NaN values
print("Deleting NaN values")
avgBalance.fillna(0, inplace=True)
# Print number of null / None values
print("Number of NaN values")
print((avgBalance.isnull().sum())[avgBalance.isnull().sum() > 0])

fig1 = avgBalance.plot(x="B",y=["GVWY", "SHVR","ZIC","ZIP"], kind="line")
plt.title("Trading Bots Performance")
plt.xlabel("Time (seconds)")
plt.ylabel("Average Balance")
plt.savefig("graphs/bots_performance.png", dpi=500)
plt.show(block=True)

avgBalance.plot(x="B", y=["C", "D"])
plt.xlabel("Time (seconds)")
plt.legend(["Bid Price", "Ask Price"])
plt.show(block=True)