import pandas as pd
import re

def process_lyrics(lyrics):
    # Find the first occurrence of "[" or "Lyrics", whichever comes first
    first_occurrence = min([lyrics.find('['), lyrics.find('Lyrics')])
    
    # If any of them are not found, set to the maximum value
    if first_occurrence == -1:
        first_occurrence = max(len(lyrics), 0)
    
    # Remove everything before the first occurrence
    processed_lyrics = lyrics[first_occurrence:]

    return processed_lyrics

def process_lyrics_column(input_file, output_file):
    # Read data from uniqueSongs_lyrics.csv
    df = pd.read_csv(input_file)

    # Apply the processing function to the 'lyrics' column
    df['processed_lyrics'] = df['lyrics'].apply(process_lyrics)

    # Drop the original 'lyrics' column
    df.drop('lyrics', axis=1, inplace=True)

    # Save the processed DataFrame to uniqueSongs_lyrics_processed.csv
    df.to_csv(output_file, index=False)
    print(f"Processed lyrics saved to {output_file}")
# Replace 'uniqueSongs_lyrics.csv' and 'uniqueSongs_lyrics_processed.csv'
# with the actual file paths
input_file_path = 'uniqueSongs_lyrics.csv'
output_file_path = 'uniqueSongs_lyrics_processed.csv'
process_lyrics_column(input_file_path, output_file_path)
