import pandas as pd

# Load dataset
df = pd.read_csv("data/sample_argo.csv")

# Count unique floats
num_floats = df["PLATFORM_NUMBER"].nunique()

print("Number of floats in dataset:", num_floats)
