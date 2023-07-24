import pandas as pd
import lyricsgenius
import time

# Replace 'YOUR_GENIUS_API_KEY' with your actual Genius API key
genius = lyricsgenius.Genius('3JxP5khQzzzhp1XcBmCiBcEnrXHgX7c3xW1uKGlN3fTVGVhhhJ3zSb3XS0UMz8aP')

# Function to get the song lyrics or return -1 if not found
def get_lyrics_or_default(song, artist):
    try:
        song_lyrics = genius.search_song(song, artist)
        if song_lyrics:
            return song_lyrics.lyrics
        else:
            return -1
    except Exception as e:
        print(f"An error occurred while fetching lyrics for '{song}': {e}")
        return -1

# Main function to process the CSV file and get lyrics
def main():
    # Assuming the file "uniqueSongs.csv" is in the same directory as this script
    input_file_path = "uniqueSongs.csv"

    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file_path)

    # Create lists to store lyrics and lyrics status for each song
    lyrics_list = []
    lyrics_status_list = []

    num_songs = df.shape[0]
    processed_songs = 0
    songs_without_lyrics = 0

    print("Processing...")

    while processed_songs < num_songs:
        start_time = time.time()

        for index, row in df.iterrows():
            song = row['song']
            artist = row['artist']

            lyrics = get_lyrics_or_default(song, artist)

            if lyrics == -1:
                songs_without_lyrics += 1

            lyrics_list.append(lyrics)
            lyrics_status_list.append(lyrics != -1)

            processed_songs += 1

        # Add the lyrics and lyrics_status to the DataFrame
        df['lyrics'] = lyrics_list
        df['lyrics_status'] = lyrics_status_list

        # Save the DataFrame to a new CSV file with the additional 'lyrics' column
        output_file_path = "uniqueSongs_lyrics.csv"
        df.to_csv(output_file_path, index=False)

        elapsed_time = time.time() - start_time
        print(f"Songs processed: {processed_songs} | Elapsed Time: {elapsed_time:.2f} seconds")
        print(f"Total Songs without lyrics: {songs_without_lyrics}")

        # Wait for 60 seconds before processing the next batch
        time.sleep(60)

if __name__ == "__main__":
    main()
