import pandas as pd
# Per day


# # Read the combined_headlines.csv file
# df = pd.read_csv('combined_headlines.csv')

# # Group by year-month and calculate the average compound score
# average_scores_per_day = df.groupby('date')['compound_score'].mean().reset_index()

# # Save the results to a new CSV file
# average_scores_per_day.to_csv('average_scores_per_day.csv', index=False)

# print("Average scores per day saved to 'average_scores_per_day.csv'.")


# Per week

import pandas as pd

# Read the combined_headlines.csv file
df = pd.read_csv('combined_headlines.csv')

# Convert the 'date' column to datetime type
df['date'] = pd.to_datetime(df['date'])

# Set the 'date' column as the index
df.set_index('date', inplace=True)

# Calculate average scores per day
average_scores_per_day = df.resample('D')['compound_score'].mean().reset_index()
average_scores_per_day.rename(columns={'date': 'date (day)', 'compound_score': 'average_score'}, inplace=True)

# Calculate average scores per week (starting on Tuesday)
average_scores_per_week = df.resample('W-TUE')['compound_score'].mean().reset_index()
average_scores_per_week.rename(columns={'date': 'date (week)', 'compound_score': 'average_score'}, inplace=True)

# Calculate average scores per month
average_scores_per_month = df.resample('M')['compound_score'].mean().reset_index()
average_scores_per_month.rename(columns={'date': 'date (month)', 'compound_score': 'average_score'}, inplace=True)

# Calculate average scores per year
average_scores_per_year = df.resample('Y')['compound_score'].mean().reset_index()
average_scores_per_year.rename(columns={'date': 'date (year)', 'compound_score': 'average_score'}, inplace=True)

# Combine all results into a single DataFrame
combined_results = pd.concat([average_scores_per_day, average_scores_per_week, average_scores_per_month, average_scores_per_year], axis=1)

# Save the results to a new CSV file
combined_results.to_csv('average_scores_all_periods.csv', index=False)

print("Average scores per day, per week, per month, and per year saved to 'average_scores_all_periods.csv'.")


