from itertools import combinations
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

from collections import defaultdict
from db import query_by_hash  # giả sử trả về list[dict]: {"song_name": ..., "anchor_time_ms": ...}

def build_query(query_fingerprints):
    """
    Xây dựng map chứa các match giữa query và DB:
    {
        "song_name_1": [(query_time1, db_time1), (query_time2, db_time2), ...],
        "song_name_2": [(query_timeX, db_timeX), ...],
        ...
    }
    """
    res = defaultdict(list)

    for hash_val, query_time_ms in query_fingerprints.items():
        matches = query_by_hash(hash_val)
        for match in matches:
            song = match["song_name"]
            db_time = match["anchor_time_ms"]
            res[hash_val].append((song, db_time))

    return res


def search():
    complex_arr = func1.func1(full_path)
    peaks = func2.extract_peaks_all_frames(complex_arr=complex_arr)
    fingerprints = func3.func3_for_search(peaks, song_name=None)
    song_scores = defaultdict(int)
    db_entries = build_query(fingerprints)
    for hash_val in db_entries:
        if hash_val not in fingerprints:
            continue

        query_times = fingerprints[hash_val]
        db_matches = db_entries[hash_val]

        if not query_times or not db_matches:
            continue

        # Chọn mốc đầu tiên
        query0 = fingerprints[hash_val][0][1]
        db0 = db_matches[0][1]  # db_matches = list of (song_name, db_time)

        for _, query_time in query_times:
            delta_query = query_time - query0
            for song_name, db_time in db_matches:
                delta_db = db_time - db0
                if abs(delta_query - delta_db) <= tolerance:
                    song_scores[song_name] += 1

    sorted_results = sorted(song_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_results
        

best_matches = search()
for (song_name, _) in best_matches:
    print(song_name)
