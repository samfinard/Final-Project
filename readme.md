**Timeframe: Beginning of 2017 - End of 2021**

Need to:
- Cleanup Billboard/data
- Delete all unnecessary .csv files
- Move most updated lyrics.csv into main where master.csv is
  

Follow next steps from [presentation](https://docs.google.com/presentation/d/1H1dAenok4H4BRiA0VzbDUx20iFsqvwxgRdY73o2SWLs/edit#slide=id.p)

[Low-resource text classification](https://www.youtube.com/watch?v=jkdWzvMOPuo) (GZIP + k-NN, beats BERT in SA)





Instructions for master.csv total data file:

We are trying to predict percent_change column, which is weekly percent change for dow jones. Can also try percent_change_VTI, which is percent change for VTI index

The "date" column is the dates where the percent_change values are taken from. All our data is matched to those dates, real_dates_trends_songs are the real dates from which the google trends and songs information came though it's all matched to the nearest future percent_change date in the "date" column

Google trends data is the following columns (vader_mean, vader_sum, vader_weighted_mean, vader_weighted_sum, textblob_mean, textblob_sum, textblob_weighted_mean, textblob_weighted_sum)

NYT data is in the following columns (nyt_vader_mean, nyt_vader_sum, nyt_textblob_mean, nyt_textblob_sum)

Songs data is in the following columns (whole_song_score, mean_by_sentence_song_score, mean_without_0_by_sentence_song_score, tb_whole_song, tb_song_by_sentence, tb_song_by_sentence_without_0)
