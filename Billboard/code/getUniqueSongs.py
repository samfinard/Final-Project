import pandas as pd

# Assuming the file "charts_post2017.csv" is in the same directory as this script
input_file_path = "charts/charts_post2017.csv"

# Read the CSV file into a DataFrame
df = pd.read_csv(input_file_path)

# Create a new DataFrame to store the unique songs and their appearance dates
unique_songs_df = pd.DataFrame(columns=['dates', 'song', 'artist'])

# Group the original DataFrame by the 'song' and 'artist' columns and aggregate the dates as lists
grouped = df.groupby(['song', 'artist'])['date'].agg(list).reset_index()

# Iterate through the groups and fill the new DataFrame with unique songs and their dates
for _, row in grouped.iterrows():
    dates_appeared_in = ', '.join(row['date'])
    unique_songs_df = pd.concat([unique_songs_df, pd.DataFrame([[dates_appeared_in, row['song'], row['artist']]], columns=['dates', 'song', 'artist'])], ignore_index=True)

# Save the new DataFrame to a CSV file named "uniqueSongs.csv"
output_file_path = "uniqueSongs.csv"
unique_songs_df.to_csv(output_file_path, index=False)

print(f"File '{output_file_path}' with unique songs and their appearance dates has been created.")
