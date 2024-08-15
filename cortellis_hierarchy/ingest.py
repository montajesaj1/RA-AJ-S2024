import pandas as pd

# Read the original CSV file
df = pd.read_csv('Cortellis_hierarchy_all_1_split.csv')

# Function to sanitize the data
def sanitize(data):
    # Remove all rows with any missing values
    data_cleaned = data.dropna()
    # Convert the first column to integer
    data_cleaned[data_cleaned.columns[0]] = data_cleaned[data_cleaned.columns[0]].astype(int)
    return data_cleaned

# Extract pairs of columns, sanitize, and write them to separate CSV files
for i in range(0, df.shape[1], 2):
    pair_df = df.iloc[:, [i, i + 1]]
    pair_df = sanitize(pair_df)
    pair_df.to_csv(f'output_pair_{i // 2 + 1}.csv', index=False, header=False)

# Read back the newly created CSV files to verify their content
for i in range(0, df.shape[1], 2):
    output_df = pd.read_csv(f'output_pair_{i // 2 + 1}.csv', header=None)
    print(f'output_pair_{i // 2 + 1}.csv:')
    print(output_df)
    print(i)
