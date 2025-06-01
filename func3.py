import mmh3
import func1
import db
# (frame_idx, freq_bin, band, amp,)

fan_out = 5
max_delta_frame=10
hop_size = func1.hop_size
sample_rate = func1.target_sr

def func3(peaks, song_name):
    fingerprints = []
    num_peaks = len(peaks)
    peaks = sorted(peaks, key= lambda x: x[0])
    for i in range(num_peaks):
        targets = []
        anchor = peaks[i]
        frame_i, freq_i, _, _ = anchor
        for j in range(i + 1, num_peaks):
            frame_j, freq_j, _, _ = peaks[j]
            if frame_j - frame_i > max_delta_frame:
                break
            targets.append(peaks[j])
        
        targets = targets[:fan_out]
        for target in targets:
            peak_t_j = target
            frame_t_j, freq_t_j, _, _ = peak_t_j
            delta_t = (frame_t_j - frame_i) * (hop_size) * 1000 / sample_rate
            hash_str = f"{freq_i}|{freq_t_j}|{delta_t}"
            hash_value = mmh3.hash(hash_str.encode(), 0, False)
            time_i_ms = frame_i * hop_size * 1000 / sample_rate
            fingerprints.append((hash_value, time_i_ms, song_name))
    return fingerprints
            
