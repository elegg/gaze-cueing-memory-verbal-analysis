import numpy as np


"""
Calculation of Mean Absolute Deviation for excluding extreme values. See:

https://psycnet.apa.org/doi/10.1016/j.jesp.2013.03.013

Concretely, calculating the MAD implies the following steps:
(a) the series in which the median is subtracted of each observation
becomes the series of absolute values of (1–7), (3–7), (3–7), (6–7),
(8–7), (10–7), (10–7), and (1000–7), that is, 6, 4, 4, 1, 1, 3, 3, and
993; (b) when ranked, we obtain: 1, 1, 3, 3, 4, 4, 6, and 993; (c) and
(d) the median equals 3.5 and will be multiplied by 1.4826 to find a
MAD of 5.1891.
"""


def MADCalculation(df, column):
    # note b is a constant assuming underlying data is normally distributed
    b =  1.4826
    median = df[column].median()
    diff = abs(df[column]-median)
    print(diff, "DIFF")
    return diff.median()*b



def mad_exclusion(df, column, output_column, deviation=2.5 ):
    median_dprime = df[column].median()
    mad_limit = MADCalculation(df, column)*deviation 
    [min_deviation, max_deviation] = [median_dprime-mad_limit, median_dprime+mad_limit]

    df[output_column] = np.where((min_deviation < df[column]) & (max_deviation> df[column])  , True, False)

    return df

def get_mad_outliers(df, column):
    mad = MADCalculation(df, column)
    median = df[column].median()
    max = median+ (2.5* mad)
    min = median - (2.5* mad)

    df = df[(df[column] <  min) | (df[column] > max)  ]

    return df["id"]