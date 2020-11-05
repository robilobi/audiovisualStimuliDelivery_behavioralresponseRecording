# Script to process melody learning task output files
# VERSION 1.1
# Written by Joseph Thibodeau in 2016, edited by Roberta Bianco in 2017
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
import pandas as pd


# Input file naming convention
# ex., "010B - Tapping-Testing - Timing_v2 (2014-08-02 17.16).txt"
in_delim1 = '_' # filename information delimiter
in_delim2 = '.' # filename information delimiter, second iteration
# explanation of above: some files start with <subjectID> - <other stuff>
# and other files start with <subjectID>_-_<other stuff>
subj_ID = 0 # first position is subject ID
# everything else in the filename is unimportant
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
###############################
#   WriteDic into CSV file    #
###############################
def WriteDictToCSV(outfile,outfile_columns,dict_data):
    try:
        with open(outfile, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=outfile_columns, extrasaction='ignore')
            writer.writeheader()
            for data in dict_data:
                writer.writerows(data)
    except IOError as (errno, strerror):
            print("I/O error({0}): {1}".format(errno, strerror))    
    return            
################################
#   match expected and pressed #
################################              
def matchExpectedLength(key1, key2):
    if len(key1)  != len(key2):
        Err = 1
    else:
        Err = 0
    return Err

def matchExpectedKeypress(key1, key2):
    KeyErr = []
    if len(key1) != len(key2):
        KeyErr = [1,1,1,1]
    else:
        for k in range(4):
            if key1[k] != key2[k]:
                KeyErr.append(1)
            else:
                KeyErr.append(0)
    return KeyErr

def calculateRespDiff(key1, key2):
    if len(key1)  == len(key2):  #played -expected
        RespDiff = [x - y for x, y in zip( key2, key1)]
    else:
        RespDiff = ['NaN', 'NaN', 'NaN', 'NaN']   
    return RespDiff

def calculateITI(key1):
    if len(key1)  == 4:  #4 played keys
        key1.insert(0, 3.85199546814) #add first expected onset as a 0
        iti= [y - x for x,y in zip(key1,key1[1:])] #compute onset-to-onset interval
        iti_expect = [0.428, 0.428, 0.428, 0.428]
        iti_percent= [(x - y)/y for x, y in zip( iti, iti_expect)]
    else:
        iti_percent = ['NaN', 'NaN', 'NaN', 'NaN']   
    return iti_percent

def create_dataframe(res):
    for bl in range(3):
        for line in range(len(res[bl])):
            res[bl][line].pop('played_onsets', None)
            res[bl][line].pop('played_keys', None)
            #res[bl][line].pop('enjoy', None)
            #res[bl][line].pop('expectedness', None) 
            res[bl][line].pop('expected_keys', None) 
            res[bl][line].pop('expected_onsets', None) 
            if len(res[bl][line]['velocities']) != 4:
                res[bl][line].update({'velocities':['NaN', 'NaN', 'NaN', 'NaN']}) 
            #res[bl][line].pop('velocities', None) 
    df = res[0] + res[1] + res[2]
    df = pd.DataFrame(df)
    items_as_cols = df.apply(lambda x: pd.Series(x['RespDiff']), axis=1)
    items_as_cols['orig_index'] = items_as_cols.index # Keep original df index as a column so it's retained after melt 
    melted_items = pd.melt(items_as_cols, id_vars='orig_index', var_name='key_num', value_name='respdiff')
    melted_items.set_index('orig_index', inplace=True)
    df1 = df.merge(melted_items, left_index=True, right_index=True).drop('RespDiff', axis =1)  ###done for respdiff
    df1 = df1.drop('velocities', axis =1)
    df1 = df1.drop('KeyErr', axis =1)
    df1 = df1.drop('iti_percent', axis =1)
    
    items_as_cols = df.apply(lambda x: pd.Series(x['velocities']), axis=1)
    items_as_cols['orig_index'] = items_as_cols.index # Keep original df index as a column so it's retained after melt 
    melted_items = pd.melt(items_as_cols, id_vars='orig_index', var_name='key_num', value_name='vel')
    melted_items.set_index('orig_index', inplace=True)
    df2 = df.merge(melted_items, left_index=True, right_index=True)
    df2 = df2['vel']
    
    items_as_cols = df.apply(lambda x: pd.Series(x['KeyErr']), axis=1)
    items_as_cols['orig_index'] = items_as_cols.index # Keep original df index as a column so it's retained after melt 
    melted_items = pd.melt(items_as_cols, id_vars='orig_index', var_name='key_num', value_name='Kerr')
    melted_items.set_index('orig_index', inplace=True)
    df3 = df.merge(melted_items, left_index=True, right_index=True)
    df3 = df3['Kerr']
    
    items_as_cols = df.apply(lambda x: pd.Series(x['iti_percent']), axis=1)
    items_as_cols['orig_index'] = items_as_cols.index # Keep original df index as a column so it's retained after melt 
    melted_items = pd.melt(items_as_cols, id_vars='orig_index', var_name='key_num', value_name='iti_percent')
    melted_items.set_index('orig_index', inplace=True)
    df4 = df.merge(melted_items, left_index=True, right_index=True)
    df4 = df4['iti_percent_y']
    
    res = pd.concat([df1, df2, df3, df4], axis=1)
    print 'create df'
    return res
    
###############################
#   PARSING THE LOG FILE      #
###############################
def parseLogFile(root_dir, file_name, outputDir, sID):
    
    # put together file names
    filepath = os.path.join(root_dir, file_name)
    inFile = open(filepath, 'rb') # opens the file
    
    reader = csv.reader(inFile, delimiter='\t')
        # Prepare a dummy values for the current rhythm
    tstamp = [] # reset timestamps
    label = []
    Roberta = []
    
    # \ Process each line individually as strings
    for line in reader:
                    
        # get the timestamp information from the first column
        ts = [line[0], line[1], line[2], line[3]]
        # convert timestamp from "10:26:15.978" format into something more useable
        ts = np.asarray(ts,np.uint32) # convert to numpy unsigned integer array
        ts = ts[3] + 1000*(ts[2] + 60*(ts[1] + 60*ts[0])) # collapse into milliseconds
        tstamp.append(ts) # append to list of timestamps
        l = line[4]
        label.append(l)
        
        if 'WarmupBlockStart' in line or 'PlaybackBlockStart' in line or 'PerformBlockStart' in line:
            Roberta.append([])
            if 'WarmupBlockStart' in line: 
                print("0")
                bl = 0
            elif 'PlaybackBlockStart' in line: 
                print("1")
                bl = 1
            elif 'PerformBlockStart' in line:   
                print("2")
                bl = 2 
        # [[]]                 At this point,  this is how your data structure should look like
        # [[{},{},{},{}],[]]
        if 'TrialStart' in line:
            Roberta[-1].append({})
            Roberta[-1][-1].update({'subID': int(sID), 'block': int(bl), 'trialID': int(line[5]), 'repetition': int(line[6]), 'condition': line[7]})
            Roberta[-1][-1].update({'expected_onsets': []})
            Roberta[-1][-1].update({'played_onsets': []})
            Roberta[-1][-1].update({'expected_keys': []})
            Roberta[-1][-1].update({'played_keys': []})
            Roberta[-1][-1].update({'velocities': []})
            Roberta[-1][-1].update({'TrialErr': []})
            Roberta[-1][-1].update({'KeyErr': []})
            Roberta[-1][-1].update({'RespDiff': []})
            Roberta[-1][-1].update({'iti_percent': []})
            
        # [[{}]]                 At this point,  this is how your data structure should look like
        # [[{},{},{},{}],[{}]]
        # [[{},{},{}]]
        # [[{sdfgh},{xcvbn},{sdfg},{wsdfg}],[{wewer},{wertytre},{}]]
        if 'EXPECTED_ONSET' in line:
            Roberta[-1][-1]['expected_onsets'].append(float(line[5]))
        if 'EXPECTED_KEY' in line:
            Roberta[-1][-1]['expected_keys'].append(int(line[6]))
        if 'KEY_ONSET' in line:
            Roberta[-1][-1]['played_onsets'].append(float(line[5]))
        if 'KEYPRESS' in line:
            Roberta[-1][-1]['played_keys'].append(int(line[5]))
#             print int(bl)
#             print Roberta[-1][-1]['trialID']
#             print Roberta[-1][-1]['played_keys']
            Roberta[-1][-1]['velocities'].append(float(line[6]))
        if line[4].startswith('Answer_'):
            Roberta[-1][-1].update({'enjoy':float(line[4].split('_')[1])})
        if line[4].startswith('Answer2_'):
            Roberta[-1][-1].update({'expectedness':float(line[4].split('_')[1])})
        
        if 'TrialFinish' in line: 
            TrialErr = matchExpectedLength(Roberta[-1][-1]['expected_onsets'], Roberta[-1][-1]['played_onsets']) #0 non errors, 1 trialerror
            Roberta[-1][-1].update({'TrialErr':int(TrialErr)})
            RespDiff = calculateRespDiff(Roberta[-1][-1]['expected_onsets'], Roberta[-1][-1]['played_onsets'])
            Roberta[-1][-1].update({'RespDiff':RespDiff})
            KeyErr = matchExpectedKeypress(Roberta[-1][-1]['expected_keys'], Roberta[-1][-1]['played_keys']) #0 non errors, 1 keyerror
            Roberta[-1][-1].update({'KeyErr':KeyErr})   
            if len(Roberta[-1][-1]['velocities']) != 4:
                Roberta[-1][-1].update({'velocities':['NaN', 'NaN', 'NaN', 'NaN']})  ###TO FIX: if there is a key press between trialstart and finish this is reported with the NaNs
            iti_percent = calculateITI(Roberta[-1][-1]['played_onsets'])
            Roberta[-1][-1].update({'iti_percent':iti_percent}) 
            
    inFile.close()
    return Roberta
    #return final_results

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
    # Get any rhythm files from this directory and subdirectories
    final = []
    for rootdir, dirs, files in os.walk(datadir):
        for f in files:
            if f.endswith(".txt") and (f.find("BMFP") > 0):
                # Report operation
                print 'Processing input file: ' + f
                
                #Split filename info
                f_split1 = string.split(f,in_delim1) #first pass, splits by ' - '
                f_split2 = string.split(f_split1[3],in_delim2)
                sID = f_split2[0]
                
                # Begin the parsing process
                results = parseLogFile(rootdir,f,outputdir, sID)
                clean_results = create_dataframe(results)
                
                # Write log output
                outfile = outputdir + '/' + 'Log_analysis_' + time_str + '_sub_' + sID + '.csv'
                
                #WriteDictToCSV(outfile,outfile_columns,results)   
                print 'writing file:' + sID 
                clean_results.to_csv(outfile, sep='\t', encoding='utf-8', header=True, columns=['subID','block','condition','repetition','key_num','trialID','TrialErr','Kerr','respdiff','vel', 'iti_percent_y','enjoy','expectedness'])
         
    print 'Processing complete.'
    
# invalid directory
else:
    print "Operation Cancelled."
