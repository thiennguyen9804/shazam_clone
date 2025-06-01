import func1 as f1
import numpy as np

target_sr = f1.target_sr
frame_size = f1.frame_size
num_band=32


def get_max(arr):
    max_val = arr[0]
    index = 0
    for i in range(len(arr)):
        if max_val < arr[i]:
            max_val = arr[i]
            index = i
    return (max_val, index)

def extract_peak_per_band(arr):
    length = len(arr)
    band_size = length // num_band
    candidate_peaks = []

    threshold = np.mean(arr)
    for band in range(num_band):
        start = band * band_size
        end = start + band_size if band != num_band - 1 else length
        band_arr = arr[start:end]
        max_val, max_idx = get_max(band_arr)
        if max_val > threshold:
            candidate_peaks.append((band, max_val, start + max_idx))
    return candidate_peaks

    
    
def extract_peaks_all_frames(complex_arr):

    num_frames = complex_arr.shape[0]
    all_peaks = []

    for frame_idx in range(num_frames):
        magnitude = np.abs(complex_arr[frame_idx])
        peaks = extract_peak_per_band(magnitude)  # [(band, max_val, freq_bin), ...]
        for band, max_val, freq_bin in peaks:
            all_peaks.append((frame_idx, freq_bin, band, max_val,))
    return all_peaks

