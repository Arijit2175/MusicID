import numpy as np

waveform = np.load('mic_recording.npy')

max_amp = np.max(np.abs(waveform))
if max_amp > 0:
    x_norm = waveform / max_amp
else:
    x_norm = waveform
print(f"Normalized waveform. Max amplitude: {np.max(np.abs(x_norm))}")

