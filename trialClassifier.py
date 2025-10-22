import numpy as np


# function that classifies trials and responses to trials
# Adds "correct" column to df (boolean). Value is True if partipant indicated up when probe letter was in array or down when probe not in array
# adds consistency column to df (boolean) True if grid was in direction of gaze

def gaze_memory_trial_classifier(complete_df):

    complete_df["correct"]= ((complete_df["target_type"] =="valid") & (complete_df["response"] =="ArrowUp")) | ((complete_df["target_type"] =="invalid") & (complete_df["response"] =="ArrowDown"))

    complete_df["consistency"] = np.where(complete_df["grid_position"]==complete_df["gaze_direction"], "Gazed-At", "Gazed-Away")

    return complete_df
