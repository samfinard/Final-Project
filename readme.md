Beginning of 2017 - End of 2021

Check Lyrics of uniqueSongs_lyrics_processed.csv

1. 2914 songs total - lyrics should be scanned over and briefly checked

To check if a song is valid
  - lyrics are in the correct language
  - lyrics look like song lyrics = no strange numbers or formating

common patterns to watch out for 
  - English song/artist with Russian lyrics (ex. line 189)
  - Instead of lyrics, a list of other songs (ex. 193)

quick way to check is look at 0 values for the isEnglish column - however this isn't enough.
  
  songs with no lyrics already have 0 in the correct_lyrics column - can ignore

**incorrect lyrics should be flagged 0 in the correct_lyrics column - not necessary to copy paste lyrics yourself**

Tip : open in google sheets, make the zoom %50, and navigate using arrow keys
  - update this file and uniqueSongs_lyrics_processed.csv as you go
  - Takes roughly 3 min to do 100 songs
  
Progress
**Sam**
- 1-200
- 201-400
- 401-600
- 601-800
- 801-1000
**Jay**
- 1001-1200
- 1201-1400
- 1401-1600
- 1601-1800
- 1801-2000
**Sam**
- 2001-2200
- 2201-2400
- 2401-2600
- 2601-2800
- 2800-2914


2. continue processing lyrics

  - remove "Embed" and any numbers touching "Embed" from the end of all lyrics]
  - fill in missing lyrics
3. Finally, ready for Sentiment Analysis (need to find more tools, especially for Emotion Classification)
  - Vader
  - TextBlob
  - Polyglot (for non english)
  
