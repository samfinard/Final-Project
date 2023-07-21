import pandas as pd

# Read the combined.csv file
df_combined = pd.read_csv('combined.csv')

# Convert the "date" column to datetime type
df_combined['date'] = pd.to_datetime(df_combined['date'])

# Drop rows with empty values
df_combined.dropna(how='any', inplace=True)

# Set the "date" column as the index
df_combined.set_index('date', inplace=True)

# Resample the data to weekly intervals (Tuesday to Tuesday) and calculate the mean
df_weekly = df_combined.resample('W-TUE').mean()

# Create a weekly date range with increment of 7 days
weekly_dates = pd.date_range(start=df_weekly.index.min(), end=df_weekly.index.max(), freq='7D')

# Format the dates to "Dec 1, Dec 8, ..."
formatted_dates = weekly_dates.strftime('%b %-d')

# Print the formatted dates
print(formatted_dates)
