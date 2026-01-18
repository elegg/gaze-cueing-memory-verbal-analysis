from pingouin import mixed_anova


def dprime_anova(df):
    return mixed_anova(between="cue_type", within="consistency", subject="id", data=df, dv="dprime")