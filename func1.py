import ffmpeg
import numpy as np

target_sr = 22050
frame_size = 2048
hop_size = 512


def frame_audio(signals):
    num_frames = 1 + (len(signals) - frame_size) // hop_size
    frames = np.zeros((num_frames, frame_size))
    for i in range(num_frames):
        start = i * hop_size
        frames[i] = signals[start:start+frame_size]
        
    return frames


def func1():
    process = (
        ffmpeg
            .input('meikai.mp3')
            .output('pipe:', format='f32le', ac=1, ar=target_sr)
            .run_async(pipe_stdout=True, pipe_stderr=True)
    )

    out, _ = process.communicate()
    audio_data = np.frombuffer(out, np.float32)
    
    frames = frame_audio(audio_data)
    window = np.hanning(frame_size)
    windowed_frame = frames * window
    complex_arr = np.fft.fft(windowed_frame)
    
    return complex_arr
    