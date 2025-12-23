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

fingerprints = []
for i, anchor in enumerate(peaks):
    anchor_freq, anchor_time = anchor[0], anchor[1]
    for j in range(1, FAN_VALUE + 1):
        if i + j >= len(peaks):
            break
        target = peaks[i + j]
        target_freq, target_time = target[0], target[1]
        time_delta = target_time - anchor_time
        if 0 < time_delta <= TARGET_ZONE_TIME:
            fp_tuple = (int(anchor_freq), int(target_freq), int(time_delta))
            h = hashlib.sha1(str(fp_tuple).encode('utf-8')).hexdigest()[:20]
            fingerprints.append((h, int(anchor_time)))

print(f"Generated {len(fingerprints)} live fingerprints.")

conn = mysql.connector.connect(host='localhost', user='root', password='', database=DB_NAME)
c = conn.cursor()
song_matches = []
for fp_hash, time_offset in fingerprints:
    c.execute(f'SELECT song_id, time_offset FROM {TABLE_NAME} WHERE hash = %s', (fp_hash,))
    results = c.fetchall()
    for song_id, db_time in results:
        song_matches.append((song_id, db_time - time_offset))

conn.close()

if not song_matches:
    print("No matches found in database.")
else:
    counter = Counter((song_id for song_id, _ in song_matches))
    best_song, best_count = counter.most_common(1)[0]
    print(f"Most likely song_id: {best_song} (matches: {best_count})")
    offset_counter = Counter((offset for song_id, offset in song_matches if song_id == best_song))
    best_offset, offset_count = offset_counter.most_common(1)[0]
    print(f"Best offset: {best_offset} (count: {offset_count})")
