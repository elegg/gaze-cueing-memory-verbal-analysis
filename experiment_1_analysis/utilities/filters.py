

# removes a list of ids from a df
def exclude_ids(df, ids):
    return df[~df["id"].isin(ids)]
