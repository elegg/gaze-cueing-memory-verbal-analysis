
import glob
from jatosDataExtraction import extractAllParticipantData
from trialClassifier import gaze_memory_trial_classifier
from dprime.dprimeCalculations import dprime_calculator, dprime_column, d_prime_calculation
from dprime.dprimeExclusions import get_mad_outliers, MADCalculation
from rts.rtSelection import selector, only_correct_rts
from analysis.dprimeAnalysis import dprime_ttest
from analysis.rtAnalysis import rt_ttest
from utilities.mad_calculator import mad_exclusion
from utilities.filters import exclude_ids
from graph.generate_graph import generate_graph

folder ="/Users/ed/Documents/jatos_results_20250520180509"
template = "/**/**/*/experiment-log.json"

files = glob.glob(folder+template)

# extract from json and classifies trial types
df = extractAllParticipantData(files)\
        .pipe(gaze_memory_trial_classifier)
