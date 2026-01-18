

from trialClassifier import gaze_memory_trial_classifier
from dprime.dprimeCalculations import dprime_column, d_prime_calculation, d_prime_corrected_calc
from rts.rtExclusion import only_correct_rts
from analysis.dprimeAnalysis import dprime_anova
from analysis.rtAnalysis import rt_anova
from utilities.filters import exclude_ids
from utilities.mad_calculator import get_mad_outliers
from graph.generate_graph import generate_graph

import pandas as pd

from analysis.planned_ttests import planned_ttests

file = "gaze-working-memory2.csv"

# extract from json and classifies trial types
# classify trial types and whether responses are correct
df = pd.read_csv(file)\
        .pipe(gaze_memory_trial_classifier)


# calculate dprime for each participant across all trial types and returns the ids of participants that are outliers
dprime_outliers = df.pipe(dprime_column ).pipe(get_mad_outliers, "dprime")
print(f"Number of outliers removed because of deviaion in dprime {len(dprime_outliers)}")
df = df.pipe(exclude_ids, dprime_outliers)


# extracts rts from correct trials, calculates median rt per participant and returns the ids of participants that are outliers
rt_outliers = df.pipe(only_correct_rts)\
                 .pipe(lambda d: d.groupby("id")["rt"].agg(["median", "std"]).reset_index())\
                        .pipe(get_mad_outliers, "median")

# remove outliers
print(f"Number of outliers removed because of deviation in RT {len(rt_outliers)}")

df = df.pipe(exclude_ids, rt_outliers)

# calculate median rt per participant 
rts = df.groupby(["id", "consistency"])["rt"].agg(["median"]).reset_index()
rts.rename(columns={"median":"median_rt"}, inplace=True)


dprime = d_prime_corrected_calc(df)
# change properly
dprime.columns = dprime.columns.get_level_values(0)
final_df = dprime.merge(rts, on = ["id", "consistency"], suffixes=("_", "")).merge(df[["id", "cue_type"]], on="id", how="left").groupby(["id", "consistency"]).first().reset_index()
# summary statistics
print(final_df.groupby(["cue_type", "consistency"])[["dprime", "median_rt"]].agg(["mean", "std"]))



# print results of t-tests for each data type

print(rt_anova(final_df).round(3))
print(dprime_anova(final_df.dropna()).round(3))

print("ARROW Planned TTest")
print(planned_ttests(final_df[final_df["cue_type"]=="ARROW"]))

print("Face Planned TTest")

print(planned_ttests(final_df[final_df["cue_type"]=="FACE"]))

# draw graphs
generate_graph(final_df)