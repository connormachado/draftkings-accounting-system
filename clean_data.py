import pandas as pd

# Load the CSV file
data = pd.read_csv('all_nba_games.csv')

# View the first few rows
print(data.head())

# View column names
print(data.columns)

# Summary of the dataset
print(data.info())

# Check for missing values
print(data.isnull().sum())

# Display basic statistics
print(data.describe())
