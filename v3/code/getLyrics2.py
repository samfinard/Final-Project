from lyrics_extractor import SongLyrics

el = SongLyrics("AIzaSyCaGOJrYc4yhdkk2Aw_G3kMvyznNKMqms8","73453abec62454bae")

lyrics = el.get_lyrics("Shape of You")

print(lyrics)