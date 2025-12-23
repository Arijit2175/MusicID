import sounddevice as sd
import numpy as np
from scipy.signal import stft
from scipy.ndimage import maximum_filter, generate_binary_structure, binary_erosion
import hashlib
import mysql.connector
from collections import Counter

SAMPLING_RATE = 44100
DURATION = 5
CHANNELS = 1
N_PER_SEG = 4096
HOP_LENGTH = 2048
NEIGHBORHOOD_SIZE = 20
THRESHOLD_PERCENTILE = 75
FAN_VALUE = 5
TARGET_ZONE_TIME = 15
DB_NAME = 'musicid_db'
TABLE_NAME = 'fingerprints'

print(f"Recording {DURATION} seconds of audio at {SAMPLING_RATE} Hz...")
recording = sd.rec(int(DURATION * SAMPLING_RATE), samplerate=SAMPLING_RATE, channels=CHANNELS, dtype='float32')
sd.wait()
waveform = recording.flatten()

max_amp = np.max(np.abs(waveform))
x_norm = waveform / max_amp if max_amp > 0 else waveform
hann_window = np.hanning(len(x_norm))
x_windowed = x_norm * hann_window

frequencies, times, Zxx = stft(x_windowed, fs=SAMPLING_RATE, nperseg=N_PER_SEG, noverlap=N_PER_SEG - HOP_LENGTH)
spectrogram = np.abs(Zxx)

threshold = np.percentile(spectrogram, THRESHOLD_PERCENTILE)
mask = spectrogram >= threshold
structure = generate_binary_structure(2, 2)
local_max = maximum_filter(spectrogram, footprint=np.ones((NEIGHBORHOOD_SIZE, NEIGHBORHOOD_SIZE))) == spectrogram
background = (spectrogram == 0)
eroded_background = binary_erosion(background, structure=structure, border_value=1)
detected_peaks = local_max ^ eroded_background
peaks = np.argwhere(mask & detected_peaks)
peaks = peaks[np.argsort(peaks[:, 1])]

