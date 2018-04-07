# File: beat_detector_demo1.py
# Author: Amir Harati, 2017
# A simple script based on LibROSA 
# current demo is not real time and is used to show how the algirthm works
# This code will produce beat output, temp output and graphical presentations.
# it also accept some paramters for tuning. 
# You need to install : https://librosa.github.io/librosa/index.html


import sys
import getopt
import numpy as np
import soundfile as sf
import librosa as lr
import librosa.display
import matplotlib.pyplot as plt
from scipy import signal


def main(argv):
    
    # algorith parameters
    hop_length = 512
    start_bpm = 120 
    onset_lag = 1
    onset_max_size = 1 #size (in frequency bins) of the local max filter. set to 1 to disable filtering.
    onset_detrend = False #Filter the onset strength to remove the DC component

    # input variables
    input_wav = ""
    ref_labels_file = ""
    ref_bpm_file = ""
    output_beats = None
    verbosity = "full" # can be none/full
    try:
        opts, args = getopt.getopt(argv, "hi:r:R:o:v:", ["input_wav=","reference_labels=","reference_bpm=", "output_beats=","verbosity="])
    except getopt.GetoptError:
        print ('beat_detector_demo1.py -i <input_wav> -r <reference_labels (optional)> -R <reference_bpm (optional)> -o <output_beats(text format)> -v <none/full>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('beat_detector_demo1.py -i <input_wav> -r <reference_labels (optional)> -o <output_beats(text format)> -v <none/full>')
            sys.exit()
        elif opt in ("-i", "--input_wav"):
            input_wav = arg
        elif opt in ("-o", "--output_beats"):
            output_beats = arg
        elif opt in ("-v", "--verbosity"):
            verbosity = arg    
        elif opt in ("-r", "--reference_labels"):
            ref_labels_file = arg
        elif opt in ("-R", "--reference_bpm"):
            ref_bpm_file = arg    
            pass
        pass


    # read the input wave file
    m_sig, fs = sf.read(input_wav)

    # read the input labels if specifed
    if (ref_labels_file != ""):
        ref_labels = np.loadtxt(ref_labels_file, usecols=(0,))
    else:
        ref_labels = None
        pass

    if (ref_bpm_file != ""):
        ref_bpm = np.loadtxt(ref_bpm_file, usecols=(0,1))
    else:
        ref_bpm = None
        pass

    
    # run the beat detetcion
    # compute spectrum features
    S = lr.feature.melspectrogram(y=m_sig, sr=fs, fmax=fs/2)
    # compute the onsets
    onset_env = lr.onset.onset_strength(S=S, sr=fs, 
                                        lag=onset_lag, max_size=onset_max_size, detrend = onset_detrend,
                                        aggregate=np.median) # use median to aggregate for different channels
    # compute tempo and beats
    tempo, beats = lr.beat.beat_track(onset_envelope=onset_env, sr=fs,
                                      hop_length=hop_length, start_bpm=start_bpm)
    
    times = lr.frames_to_time(np.arange(len(onset_env)),
                                   sr=fs, hop_length=hop_length)

    # print tempo to output
    print "Estimated BPM: ", '{0:.2f}'.format(tempo)

    
    # write the beats to output file if specified
    if (output_beats is not None):
        ofile = open(output_beats, "w")
        ofile.write("\n".join('{0:.4f}'.format(v) for v in times[beats]))
        ofile.close()

    plt.figure(figsize=(14, 12))
       
    plt.subplot(2, 1, 1)
    lr.display.waveplot(m_sig, fs, alpha=.3,label='Signal')
    plt.vlines(times[beats], 0, 1, alpha=0.5, color='r',
               linestyle='--', label='Estimated Beats')
    if (ref_labels is not None):
        plt.vlines(ref_labels, 0, 1, alpha=1, color='g',
                   linestyle='--', label='Reference Beats')

    plt.legend(frameon=True, framealpha=0.75)
    
    plt.subplot(2, 1, 2)
    plt.plot(times, lr.util.normalize(onset_env),
             label='Onset strength')
    plt.vlines(times[beats], 0, 1, alpha=0.5, color='r',
               linestyle='--', label='Estimated Beats')
    if(ref_labels is not None):
        plt.vlines(ref_labels, 0, 1, alpha=0.25, color='g',
                   linestyle='--', label='Reference Beats')

    plt.text(times[-1:]/2+1,.9,"Estimated BPM:" + '{0:.2f}'.format(tempo), 
             bbox={'facecolor':'red', 'alpha':0.9, 'pad':10})     

    if (ref_bpm is not None):
        plt.text(times[-1:]/2,.8,"Reference BPMs(slow/fast):" + ", ".join('{0:.2f}'.format(v) for v in ref_bpm), 
             bbox={'facecolor':'green', 'alpha':0.9, 'pad':10})
        
    plt.legend(frameon=True, framealpha=0.75)
    
    plt.gca().xaxis.set_major_formatter(lr.display.TimeFormatter())
    plt.tight_layout()
    plt.show()
    


if __name__ == "__main__":
    main(sys.argv[1:])

