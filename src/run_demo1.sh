#soundfile=../../data/arti/pulse_120bpm.wav
#ref_beats_lab=../../data/arti/pulse_120bpm.lab
#ref_tempo_lab=../../data/arti/pulse_120bpm_tempo.lab

soundfile=../data/mirex2006/train1.wav
ref_beats_lab=../data/mirex2006/train1_1.lab
ref_tempo_lab=../data/mirex2006/train1_tempo.lab


python beat_detector_demo1.py  -i $soundfile -r $ref_beats_lab -R $ref_tempo_lab -o xxx.txt &
sleep 2
play $soundfile

