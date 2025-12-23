import sounddevice as sd
import numpy as np

SAMPLING_RATE = 44100 
DURATION = 5           
CHANNELS = 1   

print(f"Recording {DURATION} seconds of audio at {SAMPLING_RATE} Hz...")

recording = sd.rec(int(DURATION * SAMPLING_RATE), samplerate=SAMPLING_RATE, channels=CHANNELS, dtype='float32')
sd.wait() 

waveform = recording.flatten()

print(f"Audio captured. Shape: {waveform.shape}")

np.save('mic_recording.npy', waveform)
print("Waveform saved to mic_recording.npy")