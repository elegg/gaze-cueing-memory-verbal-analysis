import json
import pandas as pd
import numpy as np
import glob
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from dprime.dprimeCalculations import dprime_calculator

from dprime.dprimeExclusions import exclude_outliers
from rts.rtSelection import selector
from analysis.dprimeAnalysis import dprime_ttest
from analysis.rtAnalysis import rt_ttest


LINE_BREAK = "\n _____________________ \n"

folder ="/Users/ed/Documents/jatos_results_20250520180509"
template = "/**/**/*/experiment-log.json"

files = glob.glob(folder+template)

def singlePtcptDataFrame(file, i):

    with open(file, ) as f:
        json_data=  json.load(f)
        matching = []

        for row in json_data:

            if row.get("block") and row["block"] != "practice":

                row.update({'id':i})
                matching.append(row)

        return  pd.DataFrame(matching)


complete_df = pd.DataFrame()

for i, f in enumerate(files):

    df = singlePtcptDataFrame(f, i)

    if len(complete_df):

        complete_df = pd.concat([complete_df, df], join="inner")
    else:
        complete_df = df


# hit :: prob of correct responses in valid trials

# miss :: prob of mistake (saying present) on invalid trials

complete_df["correct"]= ((complete_df["target_type"] =="valid") & (complete_df["response"] =="ArrowUp")) | ((complete_df["target_type"] =="invalid") & (complete_df["response"] =="ArrowDown"))

complete_df["consistency"] = complete_df["grid_position"]==complete_df["gaze_direction"]

print(complete_df["id"].agg(["mean", "std"]), complete_df.groupby("id").agg(["mean", "std"]))

grouped_df = complete_df.groupby(["consistency", "id"])["correct"].agg(["mean", "std"]).reset_index()
grouped_df["consistency"]= grouped_df["consistency"].apply(lambda x: "Gazed-At" if x else "Gazed-Away")


#sns.barplot(grouped_df, x="consistency", y="mean")
#plt.show()

df_two_columns = grouped_df.pivot(index='id', columns='consistency', values='mean')

#### D-PRIME

hits_and_misses = complete_df.groupby(["consistency", "target_type", "id"])["correct"].agg(["mean", "std"]).reset_index()

#hits_and_misses.pivot(index=["id", "consistency"], columns=["target_type"], values=["mean"])

dprime = hits_and_misses.pivot(index="id", columns=["consistency", "target_type"], values="mean")
gaze_at = dprime[True]
gaze_away = dprime[False]

dp = dprime_calculator(complete_df)

#rt_df = exclude_outliers(dp, "dprime_full")

#print("dprime df", dprime_calculator(complete_df))

rt_df = selector(complete_df)
print(rt_df)
print(rt_ttest(rt_df))
## note our columns are proportion of correct answers so miss is calculated as 1-invalid
d_prime_calculation = lambda a: stats.norm.ppf(a["valid"]) - stats.norm.ppf(1-a["invalid"])

gaze_at["dprime_gazed_at"] = d_prime_calculation(gaze_at)
gaze_away["dprime_gazed_away"] = d_prime_calculation(gaze_away)

df = pd.concat([gaze_at, gaze_away], axis=1).reset_index()


print(df)
print(dprime_ttest(df))

"""
https://psycnet.apa.org/doi/10.1016/j.jesp.2013.03.013

Concretely, calculating the MAD implies the following steps:
(a) the series in which the median is subtracted of each observation
becomes the series of absolute values of (1–7), (3–7), (3–7), (6–7),
(8–7), (10–7), (10–7), and (1000–7), that is, 6, 4, 4, 1, 1, 3, 3, and
993; (b) when ranked, we obtain: 1, 1, 3, 3, 4, 4, 6, and 993; (c) and
(d) the median equals 3.5 and will be multiplied by 1.4826 to find a
MAD of 5.1891.
"""

df1 = pd.DataFrame.from_dict({"val":[ 1, 3, 3, 6, 8, 10, 10, 1000]})


def MADCalculation(df, column):
    # note b is a constant assuming underlying data is normally distributed
    b =  1.4826
    median = df[column].median()
    diff = abs(df[column]-median)
    print(diff.median())
    return diff.median()*b
    
#print(MADCalculation(grouped_df, ''))


print("mean d' for gazed away: ")
print(gaze_away["dprime"].agg(["median", "std"]))
print(LINE_BREAK)
print("mean d' for gazed at: ")
print(gaze_at["dprime"].agg(["median", "std"]))
print(LINE_BREAK)

print("d' analysis")
print(stats.ttest_rel(gaze_at["dprime"], gaze_away["dprime"]))
print(LINE_BREAK)

# 

grouped_df = complete_df.groupby(["consistency", "id"])["rt"].agg(["mean", "std"]).reset_index()
grouped_df["consistency"]= grouped_df["consistency"].apply(lambda x: "Gazed-At" if x else "Gazed-Away")


gazed_at = grouped_df[grouped_df["consistency"] == "Gazed-At"]
gazed_away = grouped_df[grouped_df["consistency"] == "Gazed-Away"]

print("mean rt for gazed away: ")
print(gazed_at["mean"].agg(["median", "std"]))
print(LINE_BREAK)

print("mean rt for gazed at: ")
print(gazed_away["mean"].agg(["median", "std"]))
print(LINE_BREAK)

print("rt' analysis")

print(stats.ttest_rel(gazed_at["mean"], gazed_away["mean"]))


gaze_at["condition"]="gazed_at"
gaze_away["condition"]="gazed_away"
full_dprime = pd.concat([gaze_at, gaze_away])

def mad_exclusion():
    median_dprime = full_dprime["dprime"].median()
    mad_limit = MADCalculation(full_dprime, "dprime")*2.5 
    [min_deviation, max_deviation] = [median_dprime-mad_limit, median_dprime+mad_limit]

    return np.where((min_deviation < full_dprime["dprime"]) & (max_deviation> full_dprime["dprime"])  , True, False)

    
print(mad_exclusion())


print(
    full_dprime["dprime"].agg(["mean", "std"]),
    full_dprime.groupby("id")["dprime"].agg(["mean", "std"]))
Palette = sns.color_palette("Set1")
 #define your preference
sns.set(font_scale = 2)
sns.set_style("whitegrid")
sns.set_palette(Palette)
#sns.set_style(rc = {'axes.facecolor': "#F5ED90",'figure.facecolor': "#F5ED90"})


sns.barplot(full_dprime, x="condition", y="dprime", errorbar="se")
plt.show()

#sns.barplot()
#plt.show()