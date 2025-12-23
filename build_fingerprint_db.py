import numpy as np
import mysql.connector

DB_NAME = 'musicid_db'
TABLE_NAME = 'fingerprints'
SONG_ID = 1

fingerprints = np.load('fingerprints.npy', allow_pickle=True)

