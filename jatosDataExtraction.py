
import pandas as pd
import json

# takes a file and an index or id to create a dataframe from the data stored in the files from the jatos server
def singlePtcptDataFrame(file, i):

    with open(file, ) as f:
        json_data=  json.load(f)
        matching = []

        for row in json_data:

            if row.get("block") and row["block"] != "practice":

                row.update({'id':i})
                matching.append(row)

        return  pd.DataFrame(matching)


# takes an array of file locations provides and provides each location (which corresponds to an individual participant) with an id and \n
# extracts data for each individual and creates a dataframe containing all participants data

def extractAllParticipantData(files):
    complete_df = pd.DataFrame()

    for  f in files:

        id = f.split("/")[-4].split("_")[-1]

        df = singlePtcptDataFrame(f, id)

        if len(complete_df):

            complete_df = pd.concat([complete_df, df], join="inner")
        else:
            complete_df = df


    return complete_df

