import lyricsgenius

# Replace 'your_genius_api_key' with your actual Genius API key
api_key = "3JxP5khQzzzhp1XcBmCiBcEnrXHgX7c3xW1uKGlN3fTVGVhhhJ3zSb3XS0UMz8aP"
genius = lyricsgenius.Genius("3JxP5khQzzzhp1XcBmCiBcEnrXHgX7c3xW1uKGlN3fTVGVhhhJ3zSb3XS0UMz8aP")

def get_song_lyrics(song_title, artist):
    try:
        song = genius.search_song(song_title, artist)
        if song is not None:
            return song.lyrics
        else:
            return "Lyrics not found for the given song and artist."
    except Exception as e:
        return str(e)

def main():
    # Replace these with the song title and artist of your choice
    song_title = "Mo Bomba"
    artist = "Sheck Wes"

    lyrics = get_song_lyrics(song_title, artist)
    print("Song Title:", song_title)
    print("Artist:", artist)
    print("\nLyrics:")
    print(lyrics)

if __name__ == "__main__":
    main()
