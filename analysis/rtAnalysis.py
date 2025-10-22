from pingouin import ttest

def rt_ttest(df):
    return ttest(df["rt-gazed-at"], df["rt-gazed-away"], paired = True)
