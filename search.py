import os
import func1
import func2
import func3
import db
from collections import defaultdict

tolerance = 100 #ms


song_dir = "queries" 

songs = [f for f in os.listdir(song_dir) if f.endswith(".mp3")]
song = songs[0]
song_name = song.split('.')[0]
full_path = os.path.join(song_dir, song)



def search():
    complex_arr = func1.func1(full_path)
    peaks = func2.extract_peaks_all_frames(complex_arr=complex_arr)
    fingerprints = func3.func3(peaks, song_name=song_name)
    song_scores = defaultdict(int)
    for hash_value, time_query, _ in fingerprints:
        matches = db.query_by_hash(hash_value)
        for match in matches:
            time_db = match["anchor_time_ms"]
            song = match["song_name"]
            offset = round(time_db - time_query)
            song_scores[(song, offset)] += 1
            
    if not song_scores:
        return None

    best_matches = sorted(song_scores.items(), key=lambda x: x[1])
    return best_matches

best_matches = search()
for (song_name, _), _ in best_matches:
    print(song_name)
