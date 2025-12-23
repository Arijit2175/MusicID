import numpy as np
from scipy.signal import stft
import matplotlib.pyplot as plt

SAMPLING_RATE = 44100
N_PER_SEG = 4096  
HOP_LENGTH = 2048 

data = np.load('preprocessed_waveform.npy')

frequencies, times, Zxx = stft(data, fs=SAMPLING_RATE, nperseg=N_PER_SEG, noverlap=N_PER_SEG - HOP_LENGTH)
spectrogram = np.abs(Zxx)

print(f"Spectrogram shape: {spectrogram.shape} (freq bins × time frames)")

np.save('spectrogram.npy', spectrogram)
print("Spectrogram saved to spectrogram.npy")

plt.figure(figsize=(10, 4))
plt.pcolormesh(times, frequencies, 20 * np.log10(spectrogram + 1e-10), shading='gouraud')
plt.title('Spectrogram (dB)')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.colorbar(label='Magnitude (dB)')
plt.tight_layout()
plt.savefig('spectrogram.png')
print("Spectrogram image saved to spectrogram.png")