import numpy as np
import hashlib

FAN_VALUE = 5  
TARGET_ZONE_TIME = 15 

peaks = np.load('spectral_peaks.npy')

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
            h = hashlib.sha1(str(fp_tuple).encode('utf-8')).hexdigest()[:20]  # Truncate for storage
            fingerprints.append((h, int(anchor_time)))

print(f"Generated {len(fingerprints)} fingerprints.")


