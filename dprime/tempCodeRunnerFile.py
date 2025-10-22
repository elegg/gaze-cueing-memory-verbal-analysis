
from scipy import stats
import pandas as pd
import numpy as np
## note our columns are proportion of correct answers so miss is calculated as 1-invalid
d_prime_calculation = lambda a: stats.norm.ppf(a["valid"]) - stats.norm.ppf(1-a["invalid"])


def dprime_column(df):
        hits_and_misses = df.groupby(["target_type", "id"])["correct"].agg(["mean", "std"]).reset_index()

        dprime = hits_and_misses.pivot(index=["id"], columns=["target_type"], values="mean").reset_index()

        dprime["dprime"] = d_prime_calculation(dprime)

        df["dprime_exclusions"] = np.where(df["id"].isin([0]), True, False)
        return df
