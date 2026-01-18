from pingouin import ttest


def planned_ttests(df):

    a = df.pivot(index="id", columns=["consistency"], values="dprime").reset_index()

    return ttest(a["Gazed-At"], a["Gazed-Away"], paired=True, ).round(5)