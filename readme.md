Check Lyrics of uniqueSongs_lyrics_processed.csv
2914 songs total - lyrics should be scanned over and briefly checked

To check if a song is valid
  - lyrics are in the correct language
  - lyrics look like song lyrics = no strange numbers or formating

quick way to check is look at 0 values for the isEnglish column - however this isn't enough because some songs may have near-empty values

songs with no lyrics already have 0 in the correct_lyrics column - can ignore

example of incorrect lyrics: line 70 - lyrics for ASAP rocky song are in Russian

incorrect lyrics should be flagged 0 in the correct_lyrics column - not necessary to copy paste lyrics yourself


1 - 1000
1001 - 2000
2000 - 2914

