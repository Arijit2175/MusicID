import numpy as np
import hashlib

FAN_VALUE = 5  
TARGET_ZONE_TIME = 15 

peaks = np.load('spectral_peaks.npy')

peaks = peaks[np.argsort(peaks[:, 1])]

