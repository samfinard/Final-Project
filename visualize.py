import pandas as pd
import matplotlib.pyplot as plt

# Read the average_scores_all_periods.csv file
df = pd.read_csv('average_scores_all_periods.csv')

# Convert the date (week) column to datetime type
df['date (week)'] = pd.to_datetime(df['date (week)'])

# Set the date (week) column as the index
df.set_index('date (week)', inplace=True)

# Resample the data to weekly intervals (Tuesday to Tuesday) and calculate the mean
# df_weekly = df.resample('W-TUE', closed='left', label='left').mean()

# Plot the weekly average scores
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['average_score'], marker='o', linestyle='-', color='blue', label='Vader')
plt.plot(df.index, df['average_score.1'], marker='o', linestyle='-', color='red', label='TextBlob')
plt.xlabel('Date (Week)')
plt.ylabel('Average Score')
plt.title('Weekly Average Scores - Vader vs TextBlob')
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()

# Save the plot as an image or display it directly
plt.savefig('weekly_average_scores_vader_vs_textblob.png')
plt.show()
