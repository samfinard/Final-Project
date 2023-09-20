import pandas as pd
from scipy.stats import pearsonr
import numpy as np

df = pd.read_csv("../data/polarity.csv")
x = df['DJIA']
y = df['ICC']
# Calculate Pearson correlation
finite_x = x[np.isfinite(x)]
finite_y = y[np.isfinite(y)]

# Check that vectors have the same length after cleaning
if len(finite_x) == len(finite_y):
    correlation_coefficient, p_value = pearsonr(finite_x, finite_y)
    print("Pearson Correlation Coefficient:", correlation_coefficient)
    print("P-value:", p_value)
else:
    print("Vectors do not have the same length after cleaning.")
