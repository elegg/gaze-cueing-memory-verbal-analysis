

from pingouin import mixed_anova


def rt_anova(df):
    return mixed_anova(between="cue_type", within="consistency", subject="id", data=df, dv="median_rt")

