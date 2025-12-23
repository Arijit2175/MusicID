import numpy as np
import mysql.connector

DB_NAME = 'musicid_db'
TABLE_NAME = 'fingerprints'
SONG_ID = 1

fingerprints = np.load('fingerprints.npy', allow_pickle=True)

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password=''  
)
c = conn.cursor()

c.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
c.execute(f"USE {DB_NAME}")

c.execute(f'''
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    hash VARCHAR(40),
    song_id INT,
    time_offset INT
)
''')

