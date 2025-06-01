import os
import func1
import func2
import func3
import db

song_dir = "songs" 

songs = [f for f in os.listdir(song_dir) if f.endswith(".mp3")]

for song in songs:
    song_name = song.split('.')[0]
    full_path = os.path.join(song_dir, song)
    complex_arr = func1.func1(full_path)
    peaks = func2.extract_peaks_all_frames(complex_arr=complex_arr)
    fingerprints = func3.func3(peaks, song_name)
    for hash_value, anchor_time_ms, song_name in fingerprints:
        db.add_to_db(hash_value, anchor_time_ms, song_name) 
    