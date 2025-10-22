
from scipy import stats
import pandas as pd

## note our columns are proportion of correct answers so miss is calculated as 1-invalid
d_prime_calculation = lambda a: stats.norm.ppf(a["valid"]) - stats.norm.ppf(1-a["invalid"])

# generates column with calculation of dprime
def dprime_column(df):
        hits_and_misses = df.groupby(["target_type", "id"])["correct"].agg(["mean", "std"]).reset_index()
        dprime = hits_and_misses.pivot(index=["id"], columns=["target_type"], values="mean").reset_index()
        dprime["dprime"] = d_prime_calculation(dprime)

        return dprime


## function returning a df with a column of dprime for all trial types a column for valid trials and a column for invalid trials

def dprime_calculator(complete_df):

    hits_and_misses = complete_df.groupby(["consistency", "target_type", "id"])["correct"].agg(["mean", "std"]).reset_index()

    #hits_and_misses.pivot(index=["id", "consistency"], columns=["target_type"], values=["mean"])
    #  pivots so that there is a column for valid and column for invalid types of trials
    dprime = hits_and_misses.pivot(index="id", columns=["consistency", "target_type"], values="mean")

    ## note that the df has an index based on consistency (which is a boolean value) so consistent trials can be selected by indexing df[True]
    gaze_at = dprime[True]
    gaze_away = dprime[False]
    gaze_at["dprime_gazed_at"] = d_prime_calculation(gaze_at)
    gaze_away["dprime_gazed_away"] = d_prime_calculation(gaze_away)


    overall_score = complete_df.groupby(["target_type", "id"])["correct"].agg(["mean", "std"]).reset_index()
    overall_res = overall_score.pivot(index="id", columns=["target_type"], values="mean")
    overall_res["dprime_full"] = d_prime_calculation(overall_res)


    return pd.concat([gaze_at, gaze_away, overall_res], axis = 1).reset_index()








