
import pandas as pd
import json
import glob
# takes a file and an index or id to create a dataframe from the data stored in the files from the jatos server
def singlePtcptDataFrame(file, i):

    with open(file, ) as f:
        json_data=  json.load(f)
        matching = []

        for row in json_data:

            # don't add practice trials to the df
            if row.get("block") and row["block"] != "practice":

                row.update({'id':i})
                matching.append(row)

        return  pd.DataFrame(matching)


# takes an array of file locations provides and provides each location (which corresponds to an individual participant) with an id and \n
# extracts data for each individual and creates a dataframe containing all participants data

def extractAllParticipantData(files, output_dir):
    complete_df = pd.DataFrame()

    for  f in files:

        id = f.split("/")[-4].split("_")[-1]

        df = singlePtcptDataFrame(f, id)

        if len(complete_df):

            complete_df = pd.concat([complete_df, df], join="inner")
        else:
            complete_df = df

    
    complete_df.to_csv(output_dir)


    return complete_df


## folder and folder containing raw experiment results in json files 
folder ="/Users/ed/Documents/jatos_results_20251231065623"
template = "/**/**/*/experiment-log.json"
output_file = "gaze-working-memory2.csv"
files = glob.glob(folder+template)

extractAllParticipantData(files, output_file)