# Script to process Rhythm task output files
# VERSION 1.1
# Written by Joseph Thibodeau in 2016
# on behalf of
# Penhune Laboratory for Motor Learning and Neural Plasticity
# Concordia University, Montreal, Quebec, Canada

#--------------------------------------CONFIGURATION ETC--------------------------------------

# IMPORTS ETC
import Tkinter, tkFileDialog
import os
import csv
import string
from datetime import datetime
import numpy as np
from numpy import int32
from matplotlib import pyplot as plt

# Input file naming convention
# ex., "010B - Tapping-Testing - Timing_v2 (2014-08-02 17.16).txt"
in_delim1 = ' - ' # filename information delimiter
in_delim2 = '_' # filename information delimiter, second iteration
# explanation of above: some files start with <subjectID> - <other stuff>
# and other files start with <subjectID>_-_<other stuff>
subj_ID = 0 # first position is subject ID
# everything else in the filename is unimportant

# Input file data format
# Every three rows represents a listen trial and then either a tap- or no-tap response
data_row_seq = ['target_onset','tap_onset','tap_release']
# Data columns:
trial_num_col = 0
rhythm_ID_col = 1
tap_or_not_col = 2
start_time_col = 3
row_seq_counter_col = 4
time_series_start_col = 5 # there will be one or more items in subsequent columns

# Rhythm complexity labels:
RHYTHM_COMPLEXITY = ['metric-simple',
                     'metric-complex',
                     '',
                     'metric-simple',
                     'metric-complex',
                     '',
                     'easy',
                     'easy']

# Output file format
outFile_headers = ['SubjectID',
               'RhythmID',
               'Metric Complexity',
               'Asynchrony(ms)',
               '% Correct',
               'Abs. % ITI dev']
outFile_delim = '-' # Delimiter for output filename

#--------------------------------------HELPER FUNCTIONS--------------------------------------

######################################
#       FIND NEAREST                 #
######################################
# from stackoverflow:
# http://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
def findNearestValue(array,value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]

def findNearestIndex(array,value):
    idx = (np.abs(np.asarray(array)-value)).argmin()
    return idx

##################################
#   CALCULATING RHYTHM RESULTS   #
##################################
def calcRhythmResults(targets, onsets, sID, rhythm_ID):

    # Prepare output measures
    mean_async = []
    mean_perc_correct = []
    mean_abs_perc_iti_dev = []

    # For each series of taps (should be 3 total)
    for series in onsets:
        
        # Make some empty space for scoring
        chosen_taps = np.zeros(len(targets)) * np.NaN # array of NaNs (Not a Number)
        num_responses = np.zeros(len(targets)) # array of '0's

        # Associate each tap with a target
        # round each tap to the closest target, then choose the 'best' tap
        for tap in series:
            closest_target = findNearestIndex(targets, tap) # find closest target
            diff_to_target = tap - targets[closest_target] # get difference in times between tap and target
            num_responses[closest_target] += 1 # increment the # of responses for this target
            if not np.isnan(chosen_taps[closest_target]): # if there is already an entry for this target
                if abs(diff_to_target) < abs(chosen_taps[closest_target]): # and if the new entry is closer than the existing one
                    chosen_taps[closest_target] = diff_to_target # replace the old value
            else:
                chosen_taps[closest_target] = diff_to_target # simply replace the old value
                
        
        # flush out the NaNs
        chosen_taps_notnan = chosen_taps[np.isnan(chosen_taps) == False]

        # Calculate % correct for this tap series
        correct_taps = num_responses != 0 # correct if not empty
        num_taps = len(targets) # number of taps in the target rhythm
        num_correct = sum(correct_taps) # number of correct taps
        perc_correct = float(num_correct) / float(num_taps) # percent correct taps

        # Now determine "ITI" according to the method used in the previous study:
        # First let us apply the 'tap vs target' differences to the corresponding target times
        chosen_tap_times = targets + chosen_taps
        # Now, calculate ITIs for any 2 adjacent 'real' (not NaN) taps
        itis = np.diff(chosen_tap_times)
        itis_notnan = itis[np.isnan(itis) == False]

        # Calculate percent ITI deviation
        target_intervals = np.diff(targets) # distances (ms) between targets)
        perc_async = 1 - (itis / target_intervals) # perc. async relative to interval between THIS and NEXT target
        perc_async_notnan = perc_async[np.isnan(perc_async) == False]

        # Append all the relevant values to the output lists for later mean()ing
        mean_async.append(np.mean(chosen_taps_notnan)) # mean asynchrony (ms)
        mean_perc_correct.append(perc_correct) # percent correct (single measure)
        mean_abs_perc_iti_dev.append(np.mean(np.abs(perc_async_notnan))) # mean absolute percent iti deviation

    # After processing each series of taps
    # Calculate final measures (mean across series)
    mean_async = np.mean(mean_async)
    mean_perc_correct = np.mean(mean_perc_correct)
    mean_abs_perc_iti_dev = np.mean(mean_abs_perc_iti_dev)
    
    check_validity = [mean_async, mean_perc_correct, mean_abs_perc_iti_dev]
    if (np.sum(np.isnan(check_validity)) > 0): # the sum will be > 0 if there are any 'nan' values
        return -1 # error code
    else:
        rhythm_label = RHYTHM_COMPLEXITY[rhythm_ID - 1]
        return [sID,
                rhythm_ID,
                rhythm_label,
                mean_async,
                mean_perc_correct,
                mean_abs_perc_iti_dev]

###############################
#   PARSING THE LOG FILE      #
###############################
def parseLogFile(root_dir, file_name, outputDir, sID):

    # Allocate output data structure
    final_results = []

    # put together file names
    filepath = os.path.join(root_dir, file_name)
    inFile = open(filepath, 'rb') # opens the file
    
    try:
        # Create a CSV reader
        reader = csv.reader(inFile, delimiter=',')
        # Prepare a dummy values for the current rhythm
        last_rhythm = 0
        lineCtr = 0
        tstamp = [] # reset timestamps
        label = [] # reset the labels
        args = [] # event arguments
        
        # \ Process each line individually as strings
        for line in reader:
            
            # \ determine timestamp
            
            # get the timestamp information from the first column
            ts = line[0]
            # convert timestamp from "10:26:15.978" format into something more useable
            # firstly, get the numbers to be integers in a list
            ts = ts.split(":") # split by colon
            ts = ts[0:2] + ts[2].split(".") # split the last element by '.'
            ts = np.asarray(ts,np.uint32) # convert to numpy unsigned integer array
            ts = ts[3] + 1000*(ts[2] + 60*(ts[1] + 60*ts[0])) # collapse into milliseconds
            tstamp.append(ts) # append to list of timestamps
            
            # / timestamp is done
            
            # \ split label into event type and arguments
            l = line[1].split(" ")[1] # remove leading space
            l = l.split("_") # split into event name and arguments using underscore
            if len(l) > 1: # if there are any arguments
                a = l[1:] # arguments come after the event name
            else:
                a = None # (no arguments found)
            l = l[0] # label is only the event name
            label.append(l) # store the event name
            args.append(a) # store arguments
            # \
                # based on the label, add information to a different variable
                # if l == 'EXPECTED_ONSET':
                #    expected_times.append([ts,a[0]])
            # /
            # / done processing label
            
        # / line processing is done          
    finally:
        
        # \ prep some variables for plotting
        tstamp = np.asarray(tstamp)
        label = np.asarray(label)
        # strange code but it takes all timestamps that are associated with Metronome events:
        metronomes = tstamp[np.nonzero(np.where(label=='Metronome', 1, 0))[0]]
        expects = tstamp[np.nonzero(np.where(label=='ExpectedTimeKeypress', 1, 0))[0]]
        extracts = tstamp[np.nonzero(np.where(label=='Extract', 1, 0))[0]]
        # / done prepping variables
        
        # \ find closest metronome to each expected keypress
        timediffs = []
        for e in expects:
            closest = findNearestValue(metronomes,e)
            timediffs.append(e - closest)
        # / done matching metronomes and keypresses
        
        # \ plot some stuff for fun (development)
        plt.figure(1)
        plt.stem(metronomes,metronomes*0+1,'r--x')
        plt.stem(expects,expects*0+2,'b-o')
        plt.plot(expects,timediffs,'k:^')
        plt.show()
        # / plotting done
        
        # Calculate the results for the final rhythm
        results = [];
        # Only save the results if all results are valid
        if results != -1: # only save results if they are valid
            final_results.append(results)
        
        inFile.close()
        return final_results

#--------------------------------------MAIN SCRIPT BELOW--------------------------------------

#############################
#      MAIN SCRIPT          #
#############################
root = Tkinter.Tk()
datadir = tkFileDialog.askdirectory(parent=root,initialdir=".",title='Select Data Directory for Processing')
outputdir = tkFileDialog.askdirectory(parent=root,initialdir=".",title='Select Output Directory')
# If the directory is valid, go ahead
if len(datadir) > 0 and len(outputdir) > 0:
    # Open an output file and CSV writer object
    time_now = datetime.now()
    time_str=str(time_now.year)+outFile_delim+str(time_now.month)+outFile_delim+str(time_now.day)+outFile_delim+str(time_now.hour)+outFile_delim+str(time_now.minute)
    outFileName = outputdir + '/' + 'Log_analysis_' + time_str + '.txt'
    outFID = open(outFileName,'wb')
    writer = csv.writer(outFID, delimiter = '\t')
    writer.writerow(outFile_headers)
    
    # Get any rhythm files from this directory and subdirectories
    for rootdir, dirs, files in os.walk(datadir):
        for f in files:
            if f.endswith(".txt") and (f.find("playback") > 0):
                # Report operation
                print 'Processing input file: ' + f
                
                # Split filename info
                # f_split1 = string.split(f,in_delim1) #first pass, splits by ' - '
                # f_split2 = string.split(f_split1[0],in_delim2) #second pass, splits by '_'
                # sID = f_split2[0]
                sID = 'test'
                
                # Begin the parsing process
                results = parseLogFile(rootdir,f,outputdir, sID)
                
                # Write the result to the output file
                writer.writerows(results)
                
    outFID.close()
    
    print 'Processing complete.'
    
# invalid directory
else:
    print "Operation Cancelled."
