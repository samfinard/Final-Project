import pandas as pd
from scipy.stats import pearsonr, ttest_ind
from tqdm import tqdm
import numpy as np

# Assuming you have a DataFrame df
df = pd.read_csv("../data/polarity.csv")
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)
target_cols = ['DJIA_percent_change', 'DJIA', 'ICC']
source_cols = ['vader', 'textblob', 'vader_full', 'textblob_full']

results = []

for target in tqdm(target_cols):
    for source in source_cols:
        pear_corr, _ = pearsonr(df[source], df[target])
        t_stat, p_val = ttest_ind(df[source], df[target])
        
        results.append({
            'Source': source,
            'Target': target,
            'Pearson_Corr': pear_corr,
            'T_Score': t_stat,
            'P_Value': p_val
        })

results_df = pd.DataFrame(results)
results_df.to_csv('../data/results.csv', index=False)
