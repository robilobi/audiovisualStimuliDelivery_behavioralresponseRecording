'''
Roberta Bianco's MRI Piano (BMFP) Experiment Code
Based on MFST and TMSPython code
by Joseph Thibodeau
for Penhune Laboratory, Concordia University
2017

This is the main module for the BMFP protocol described by Roberta Bianco
Starting with Marianne Stephan's TMS code but adding MIDI Piano support
'''

from BMFP_GUI import *
from BMFP_Config import *
from BMFP_Logger import *
import sys
import os
import time
from random import randint, shuffle, seed

USAGE = 'wrong # of arguments. usage: python BMFP_Main.py <subjectname>'

def init_randoms(fingSeq):
    seqLen = len(f) #store the unadulterated sequence length
    randSeq = f #init output structure with the "correct" input structure for comparison --- we'll pull it out at the end
    #seed(19840909) #always seed with the same number (JT birthday) so we know that the randoms are the same for each participant
    tempSeq=randSeq.items() # List of tuples
    admissable = False
    while not admissable:
        admissable = True #start with an optimistic view
        shuffle(tempSeq)
        for elem in range(seqLen-1):
            if tempSeq[elem][1] == tempSeq[elem+1][1]:
                admissable = False # repeat found
                break # exit the element check
    print tempSeq[:]
    return tempSeq[:]

rand = init_randoms(f)

randl=[]
for item in rand:
    randl.append(item[0])


"""
build_Blocks function

This is where we create a list of instructions that we execute one-by-one until the experiment is over.
BMFP_Config should contain all the necessary variables to configure the details of this list (like
how many trials, etc)
"""
def build_Blocks(blocktype, numblocks, trialsperblock, trialrepet):

    instructionList = [] #start with an empty list

    for block in range(numblocks): # for each of the listen blocks

        instruction = (BLOCK_START_INST, block, blocktype) # make a 'block start' instruction with the block # as an argument
        instructionList.append(instruction) # append the instruction to the list

        for trial in range(trialsperblock): # for all trials in this block
            if blocktype == WARMUP_BLOCK:
                thistrial = trial
            else:
                thistrial = randl[trial]
            for counter in range(trialrepet):
                instruction = (TRIAL_START_INST, thistrial, counter) # make a 'trial start' instruction with the trial # as an argument
                instructionList.append(instruction) # append the instruction to the list
                # Any other special instructions to execute during the trial go here

                instruction = (TRIAL_FINISH_INST, thistrial, counter) # make a 'trial end' instruction with the trial # as an argument
                instructionList.append(instruction) # append the instruction to the list

        instruction = (BLOCK_FINISH_INST,block) # make a 'block start' instruction with the block # as an argument
        instructionList.append(instruction) # append the instruction to the list

    return instructionList # RECALL that to pop() this in proper order you need to reverse() it


"""
startui function

Prep the experiment and then launch the GUI application
"""
def startui(subjectName='noname'):

    logName = LOG_DIR + "Log_BMFP_" + str(subjectName) + ".txt"
    logger=Logger(logName)

    experiment = [] #start with empty experiment

    #experiment += build_Blocks(RATING_BLOCK, NUM_RATING_BLOCKS, TRIALS_PER_RATING_BLOCK, NUMB_REPET_RATING) # add list of instructions for RATING block
    experiment += build_Blocks(WARMUP_BLOCK, NUM_WARMUP_BLOCKS, TRIALS_PER_WARMUP_BLOCK, NUMB_REPET_WARMUP) # add list of instructions for playback block
    experiment += build_Blocks(PLAYBACK_BLOCK, NUM_PLAYBACK_BLOCKS, TRIALS_PER_PLAYBACK_BLOCK, NUMB_REPET_PLAYBACK) # add list of instructions for playback block
    experiment += build_Blocks(PERFORM_BLOCK, NUM_PERFORM_BLOCKS, TRIALS_PER_PERFORM_BLOCK, NUMB_REPET_PERFORM) # add list of instructions for playback block
       
    experiment.reverse() # need to reverse the experiment so that when you pop() instructions it removes the last one first
       
    gui = BMFP_GUI(None, experiment, logger)
    gui.master.title("LikePiano")
    gui.mainloop()

    logger.closefile()

    print "Goodbye :)" #TODO: put these messages in config
    return

"""
main function

This gets called at the beginning. Simply passes its arguments to the startui function
"""
if __name__=="__main__":
    startui(str(sys.argv[1]))
