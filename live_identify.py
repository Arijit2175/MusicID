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

