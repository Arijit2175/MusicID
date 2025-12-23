import numpy as np
from scipy.ndimage import maximum_filter, generate_binary_structure, binary_erosion

NEIGHBORHOOD_SIZE = 20  
THRESHOLD_PERCENTILE = 75  

spectrogram = np.load('spectrogram.npy')

threshold = np.percentile(spectrogram, THRESHOLD_PERCENTILE)
mask = spectrogram >= threshold

structure = generate_binary_structure(2, 2)
local_max = maximum_filter(spectrogram, footprint=np.ones((NEIGHBORHOOD_SIZE, NEIGHBORHOOD_SIZE))) == spectrogram
background = (spectrogram == 0)
eroded_background = binary_erosion(background, structure=structure, border_value=1)
detected_peaks = local_max ^ eroded_background

peaks = np.argwhere(mask & detected_peaks)

print(f"Detected {len(peaks)} spectral peaks.")

