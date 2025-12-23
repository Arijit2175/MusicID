import sounddevice as sd
import numpy as np
from scipy.signal import stft
from scipy.ndimage import maximum_filter, generate_binary_structure, binary_erosion
import hashlib
import mysql.connector
from collections import Counter

