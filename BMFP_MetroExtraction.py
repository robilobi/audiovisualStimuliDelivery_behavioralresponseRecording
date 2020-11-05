import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as iow
import aifc
import scipy.signal as sig
import os


######################################
#     MAIN SCORING FUNCTION          #
######################################
def scoreFiles(root,filename,sID,sCH,blockID,trialID,IBI,stimname,show_visuals,writer):
    # root: file directory
    # filename: path and name to file
    # sID: subject name
    # blockID: block number of this file
    # trialID: trial number of this file
    # IBI: period of the target beat
    # stimname: name of the stim
    # show_visuals: whether or not to plot the results

#    DEBUG_STIM_VISUALS = False
#    DEBUG_TAP_VISUALS = False

    filepath = os.path.join(root, filename)


    # read input file (WAV)
    sfile = iow.read(filepath)


    #get sampling rate (WAV)
    fs = sfile[0]

    #get signal data (WAV)
    signal = np.asfarray(sfile[1])
    msec = np.divide(range(len(signal)),float(fs))
    msec = msec*1000.0
    samps = np.asfarray(range(len(signal)))

    sig_abs = np.abs(signal)
    sig_norm = np.divide(sig_abs,np.max(sig_abs))

    useSamps = False
    if useSamps:
        msec = samps
        msperbuff = 512.0
    else:
        buffsize = 512.0
        msperbuff = 1000.0*512.0/44100.0

    uptimes = msec[np.nonzero(np.where(sig_norm > 0.5, 1, 0))[0]]
    uptimes2 = []

    for s in range(len(uptimes)):
        if (s == 0) or (uptimes[s] - uptimes[s-1] >= 500.0):
            uptimes2.append(uptimes[s])
    uptimes2 = np.asarray(uptimes2)

    updiffs = np.diff(uptimes2)
    edges = updiffs[np.nonzero(np.where(updiffs > 500.0, 1, 0))[0]]
    edges2 = edges[np.nonzero(np.where(edges < 3000.0, 1, 0))[0]]

    edges2 = edges2
    middleedge = np.mean(edges2)
    edges3 = np.copy(edges2)

    for e in range(len(edges2)):
        if edges2[e] > middleedge:
            edges3[e] = edges2[e] - msperbuff;

    # set up the return values
    out_struct = edges2

    plt.figure(1)
    plt.stem(edges2,'r:x')
    plt.stem(edges3,'b-o')
    plt.show(True)
#    trial_struct = {}
#    trial_struct['stimname'] = stimname
#    trial_struct['samplerate'] = fs
#    trial_struct['beats'] = stim_fake_indices
#    trial_struct['taps'] = tap_on_idx
#    out_struct['trial' + str(trialID)] = trial_struct
    return out_struct
