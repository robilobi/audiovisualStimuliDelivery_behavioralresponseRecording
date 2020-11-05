# -*- coding: utf-8 -*-
"""
Created on Fri May  8 15:08:13 2015

@author: thibodeauj

Wrapper script for batch-processing IGVP wav files
"""

import Tkinter, tkFileDialog
import os
import csv
from BMFP_MetroExtraction import *
from datetime import datetime
import scipy.io as sio
import sys

#############################
#      MAIN SCRIPT          #
#############################
#root = Tkinter.Tk()
#datadir = tkFileDialog.askdirectory(parent=root,initialdir=".",title='Select Subject Data Directory')
#outputdir = tkFileDialog.askdirectory(parent=root,initialdir=".",title='Select Output Directory')
datadir = './output/'
outputdir = './output/'
subjects = ['may032017']
# subjects = ['test']

#directory parsing info
dir_delim = '/'
Task = -1

#filename parsing info
fname_delim = '_'
SID = 2
BlockID = 4
TrialID = 6

#tapping target period (seconds)
IBI = 0.5

#    # set up the return values
#    outlist = []
#    outlist.append(complexity)
#    outlist.append(variant)
#    outlist.append(IBI_raw)
#    outlist.append(stim_real_jitter)
#    outlist.append(num_taps)
#    outlist.append(correct_taps)
#    outlist.append(tap_interval_mean)
#    outlist.append(asynch_mean)
#    outlist.append(asynch_ref)
#    for tap in asynch_taps:
#        outlist.append(tap)

# options
show_visuals = False

# Construct the header
headerColumns = ['Subject',
                 'BlockID',
                 'TrialID',
                 'IBI',
                 'Num_Responses',
                 'Correct_Responses',
                 'MeanITI',
                 'MeanAsynch',
                 'AllAsynchs']
header = '\t'.join(headerColumns) #insert tabs between header columns for printing

# open the output file
time_now = datetime.now()
millisecond = time_now.microsecond/1000
delim='-'
time_str=str(time_now.year)+delim+str(time_now.month)+delim+str(time_now.day)+delim+str(time_now.hour)+delim+str(time_now.minute)
outFileName = outputdir + 'BMFP_Output_' + time_str
outFID = open(outFileName,'wb')
# try:
writer = csv.writer(outFID,delimiter='\t')
writer.writerow(headerColumns)
out_struct = {}
for subj in range(len(subjects)):
    hh_struct = {}
    nohh_struct = {}
    s = subjects[subj]
    out_struct[s] = {}
    c = 1 #XXX: hardcoded
    print "Processing " + s
    search_dir = datadir + s + '/'
    # Get any scanning files from this directory and subdirectories
    for root, dirs, files in os.walk(search_dir):
        files.sort()
        for f in files:
            if f.find("wav") > 0: # only process wave files
                # MEAT OF THE SCRIPT GOES HERE
                # Begin the parsing process
                print root + f
                rsplit = root.split(dir_delim)
                fsplit = f.split('.')[0].split(fname_delim)
                hhsplit = fsplit[-1].split('-')
                hhname = hhsplit[0]

                if (s == 'pilot01' or s == 'pilot02' or s == 'pilot03'):
                    stimname = fsplit[4:-1:1]
                    stimname = '_'.join(stimname)
                    oldnamesplit = fsplit[3].split('-')
                    oldtrial = oldnamesplit[2]
                    if hhname == 'HH':
                        oldblock = 1
                    elif hhname == 'noHH':
                        oldblock = 2
                    result = scoreFiles(root,f,s,c,oldblock,oldtrial,IBI,stimname,show_visuals)
                else:
                    stimname = fsplit[7:-1:1]
                    stimname = '_'.join(stimname)
                    result = scoreFiles(root,f,s,c,0,fsplit[1],IBI,stimname,show_visuals,writer)

                # Write edges into a file
                writer.writerow(result)
outFID.close()
print "Batch processing complete"