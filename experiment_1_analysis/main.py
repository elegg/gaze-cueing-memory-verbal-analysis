
import glob

from jatosDataExtraction import extractAllParticipantData
from trialClassifier import gaze_memory_trial_classifier
from dprime.dprimeCalculations import dprime_column, d_prime_calculation
from rts.rtExclusion import only_correct_rts
from analysis.dprimeAnalysis import dprime_ttest
from analysis.rtAnalysis import rt_ttest
from utilities.filters import exclude_ids
from utilities.mad_calculator import get_mad_outliers
from graph.generate_graph import generate_graph
from os import makedirs
import shutil

## folder and folder containing raw experiment results in json files 
folder = "/Users/ed/Documents/jatos_results_20251230222414"
template = "/**/**/*/experiment-log.json"

files = glob.glob(folder+template)

print(files)

"""
for f in files:
        id = f.split("/")[-4]
        makedirs(f"data/{id}")
        shutil.copyfile(f, f"data/{id}/experiment-log.json")

"""
# extract from json and classifies trial types
# classify trial types and whether responses are correct
df = extractAllParticipantData(files)\
        .pipe(gaze_memory_trial_classifier)

# calculate dprime for each participant across all trial types and returns the ids of participants that are outliers
dprime_outliers = df.pipe(dprime_column ).pipe(get_mad_outliers, "dprime")
df = df.pipe(exclude_ids, dprime_outliers)

# extracts rts from correct trials, calculates median rt per participant and returns the ids of participants that are outliers
rt_outliers = df.pipe(only_correct_rts)\
                 .pipe(lambda d: d.groupby("id")["rt"].agg(["median", "std"]).reset_index())\
                        .pipe(get_mad_outliers, "median")

# remove outliers
df = df.pipe(exclude_ids, rt_outliers)


# calculate median rt per participant 
rts = df.groupby(["id", "consistency"])["rt"].agg(["median", "std"]).reset_index()

# widen df on consistency column
rts = rts.pivot(index="id", columns = ["consistency"], values="median").reset_index()
rts =rts.rename(columns={"Gazed-At":"rt-gazed-at", "Gazed-Away":"rt-gazed-away"})

hits_and_misses = df.groupby(["consistency", "target_type", "id"])["correct"].agg(["mean"]).reset_index()

dprime = hits_and_misses.pivot(index="id", columns=["consistency", "target_type"], values="mean").reset_index()
dprime["dprime-gazed-at"] = d_prime_calculation(dprime["Gazed-At"])
dprime["dprime-gazed-away"] = d_prime_calculation(dprime["Gazed-Away"])


d1 = dprime[["id", "dprime-gazed-at", "dprime-gazed-away"]]

d1.columns = d1.columns.get_level_values(0)

final_df = d1.merge(rts, on = "id")


# summary statistics
print(final_df[["dprime-gazed-at", "dprime-gazed-away", "rt-gazed-at", "rt-gazed-away"]].agg(["mean", "std"]))

# print results of t-tests for each data type
print(rt_ttest(final_df))
print(dprime_ttest(final_df))

# draw graphs
generate_graph(final_df)