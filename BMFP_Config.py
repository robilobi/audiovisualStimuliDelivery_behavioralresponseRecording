from __future__ import division
'''
Configuration module for Bianco LikePiano experiment
Joseph Thibodeau 2017
'''

#---------------------------
# Block types ---- the numbers here are arbitrary, just need to be unique
#---------------------------
RATING_BLOCK = 0
WARMUP_BLOCK = 1
PLAYBACK_BLOCK = 2
PERFORM_BLOCK = 3

#---------------------------
# Block numbers
#---------------------------
NUM_RATING_BLOCKS = 1
TRIALS_PER_RATING_BLOCK = 4
NUMB_REPET_RATING = 5

NUM_WARMUP_BLOCKS = 1
TRIALS_PER_WARMUP_BLOCK = 3
NUMB_REPET_WARMUP = 5

NUM_PLAYBACK_BLOCKS = 1
TRIALS_PER_PLAYBACK_BLOCK = 16
NUMB_REPET_PLAYBACK = 5

NUM_PERFORM_BLOCKS = 1
TRIALS_PER_PERFORM_BLOCK = 16
NUMB_REPET_PERFORM = 1

#---------------------------
# Instruction types ---- associated strings should probably be switched for numbers to save on CPU cycles in an embedded context, but for now I'll leave them human-readable.
#---------------------------
# All instructions are made of an instruction type and a list of arguments. For example, (BLOCK_START_INST, 1) means "start block 1"
BLOCK_START_INST = 'block_start'
BLOCK_FINISH_INST = 'block_finish'
TRIAL_START_INST = 'trial_start'
TRIAL_FINISH_INST = 'trial_finish'
TRIAL_REP = 'trial_repeat'

#---------------------------
# Timing
#---------------------------
NOTEDUR = 428 #ms, 140bpm
#---------------------------
# Experiment structure
#---------------------------

#---------------------------
# Logs
#---------------------------
LOG_DIR = './logs/'
DELIM = '\t'

#---------------------------
# Stims
#---------------------------
# tones are index 0-3, cue is index 4
STIM_SEQ = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
STIM_FILES = ['1a.wav','1b.wav','1c.wav','1d.wav','2a.wav','2b.wav','2c.wav', '2d.wav', '3a.wav', '3b.wav','3c.wav','3d.wav','4a.wav','4b.wav','4c.wav','4d.wav']
EXTRACT_SEQ = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
EXTRACT_FILES = ['1a_extract.wav','1b_extract.wav','1c_extract.wav','1d_extract.wav','2a_extract.wav','2b_extract.wav','2c_extract.wav', '2d_extract.wav', '3a_extract.wav', '3b_extract.wav','3c_extract.wav','3d_extract.wav','4a_extract.wav','4b_extract.wav','4c_extract.wav','4d_extract.wav']
PIANO_FILE = ['AUDIO_Piano.wav']
#METRO_FILE = ['22050Hz_testpulse.wav'] #testing timing characteristics. originally: 
METRO_FILE = ['cue.wav']
STIM_DIR = './audio/stim_real/'
EXTRACT_DIR = './audio/resp_real/'
CUE_INDEX = 4
NOTE_SET_LENGTH = 4

# visual stims
KEYBOARD_IMAGE = 'K0F0.jpg'
SLIDER_IMAGE = 'slider.jpg'

#---------------------------
# Inputs and mappings
#---------------------------
# INPUT_COND = {0:["a"], 1:["b"], 2:["c"],3:["d"],4:["a"], 5:["b"],6:["c"],7:["d"],8:["a"],9:["b"],10:["c"],11:["d"],12:["a"],13:["b"],14:["c"],15:["d"]}
INPUT_COND = ['a','b','c','d',
              'a','b','c','d',
              'a','b','c','d',
              'a','b','c','d',]
INPUT_TARGETS = [65, 67, 69, 71]
INPUT_MAPS = {0: [69, 71, 72, 74],
              1: [69, 71, 72, 74], 
               2: [72, 74, 75, 77], 
               3: [72, 74, 75, 77], 
               4: [66, 67, 69, 71], 
               5: [66, 67, 69, 71],
               6: [69, 70, 72, 75], 
               7: [69, 70, 72, 75],
               8: [71, 73, 74, 76], 
               9: [71, 73, 74, 76], 
               10: [74, 76, 77, 79], 
               11: [74, 76, 77, 79], 
               12: [64, 65, 67, 69],  
               13: [64, 65, 67, 69],  
               14: [65, 68, 70, 72],
               15: [65, 68, 70, 72]} 

INPUT_FINGERS = {0:["4", "3", "2", "3"], 
                 1:["4", "3", "2", "3"], 
                 2:["4", "3", "2", "3"], 
                 3:["4", "3", "2", "3"], 
                 4:["3", "2", "1", "2"], 
                 5:["3", "2", "1", "2"], 
                 6:["3", "2", "1", "2"],
                 7:["3", "2", "1", "2"], 
                 8:["4", "1", "2", "3"], 
                 9:["4", "1", "2", "3"], 
                 10:["4", "1", "2", "3"], 
                 11:["4", "1", "2", "3"], 
                 12:["1", "2", "3", "2"],
                 13:["1", "2", "3", "2"],
                 14:["1", "2", "3", "2"],
                 15:["1", "2", "3", "2"]}
f = {0:[0], 1:[0], 2:[0], 3:[0], 4:[1], 5:[1], 6:[1], 7:[1], 8:[2], 9:[2], 10:[2], 11:[2], 12:[3],13:[3], 14:[3],15:[3]}

warmupINPUT_FINGERS = {0:["4", "3", "1", "2"], 
                       1:["2", "3", "4", "1"],
                       2:["2", "1", "3", "2"],
                       3:["3", "2", "3", "4"]}


PAUSE_BUTTON = "p"
SPACEBAR = " " # TODO: generalize the block advancement, like instead of 'spacebar' by default just have a general config item called "advance past prompt" or something
responseButts = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# 
#---------------------------
# User prompts
#---------------------------
BLANK_TEXT = ''
PROCEED = '\r\nPress <space> to continue'
OPENING_PROMPT = 'Welcome to the Like & Sound experiment!' + PROCEED

RATING_PROMPT = '''This is the start of a rating block.
Do some rating!'''+ PROCEED # This comes before every melody listening block (LISTEN_PROMPT_before)

WARMUP_PROMPT = '''This is the start of a "WARM UP" block. 
Place your fingers (thumb, index, middle and ring fingers) on the yellow keys.
You will listen to 3 metronome beats; at the 4th beat you will have to serially press 4 keys 
by following the colored squares displayed on the keyboard.

Each trial will be repeated 5 times.

Do some practice!''' + PROCEED

PLAYBACK_PROMPT = '''This is the start of a "PRACTICE" block. 
Place your fingers (thumb, index, middle and ring fingers) on the yellow keys.

You will listen to the first part of a melody with 3 superimposed metronome beats; 
at the 4th beat you will have to complete the melody by playing the last 4 notes.

Try to keep the time and play by following the colored squares displayed on the keyboard.
Each melody will be repeated 5 times.

Do some practice!''' + PROCEED

PERFORM_PROMPT = '''This is the start of a "PERFORM" block.
First, you will listen to the entire melody. 

Then, you will listen to the first part of a melody, and will have to complete it with the last 4 notes (as you have done in the practice block).

After each melody, you will be asked to rate how much (from: not at all, to: very much) you ENJOYED to play the melody (even if the performance wasn't perfect!).
Also, you will be asked to rate how much (from: not at all, to: very much) the melody was familiar to you.

Play your heart out!''' + PROCEED

BLOCK_COMPLETION_PROMPT = '''Block complete.
''' + PROCEED