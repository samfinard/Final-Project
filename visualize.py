import pandas as pd
import matplotlib.pyplot as plt

# Read the average_scores_all_periods.csv file
df = pd.read_csv('average_scores_all_periods.csv')

# Convert the date (week) column to datetime type
df['date (week)'] = pd.to_datetime(df['date (week)'])

# Set the date (week) column as the index
df.set_index('date (week)', inplace=True)

# Plot the weekly average scores
plt.figure(figsize=(10, 6))
plt.plot(df.index, df['average_score'], marker='o', linestyle='-')
plt.xlabel('Date (Week)')
plt.ylabel('Average Score')
plt.title('Weekly Average Scores')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# Save the plot as an image or display it directly
plt.savefig('weekly_average_scores.png')
plt.show()
