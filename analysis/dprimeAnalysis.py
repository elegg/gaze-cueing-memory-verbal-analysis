from scipy.stats import ttest_rel
from pingouin import ttest


def dprime_ttest(df):
    return ttest(df["dprime-gazed-at"], df["dprime-gazed-away"], paired=True)