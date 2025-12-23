import numpy as np
from scipy.ndimage import maximum_filter, generate_binary_structure, binary_erosion

NEIGHBORHOOD_SIZE = 20  
THRESHOLD_PERCENTILE = 75  

spectrogram = np.load('spectrogram.npy')

