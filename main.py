import soundfile
import numpy as np
import sys
from scipy.fft import fft, fftfreq
from scipy.signal import decimate

def load_audio(file_path):
    audio_data, sample_rate = soundfile.read(file_path, always_2d=True)
    # Convert to single channel (mono)
    if audio_data.shape[1] == 2:
        audio_data = np.mean(audio_data, axis=1)
    else:
        audio_data = audio_data[:, 0]
    return audio_data, sample_rate


def window_function(signal, window_param=14):
    return signal * np.kaiser(len(signal), window_param)


def harmonic_product_spectrum(fft_signal, harmonics=4):
    if harmonics < 2:
        harmonics = 2
    processed_fft = fft_signal.copy()
    for harmonic in range(2, harmonics + 1):
        downsampled = decimate(fft_signal, harmonic)
        processed_fft[:len(downsampled)] *= downsampled
    processed_fft[:10] = 0
    return processed_fft


def signal_preprocessing(audio_signal):
    processed_signal = audio_signal
    processed_signal = window_function(processed_signal, window_param=50)
    processed_signal = abs(fft(processed_signal))
    processed_signal = harmonic_product_spectrum(processed_signal, harmonics=4)
    return processed_signal


def classify_gender(fft_bins, fft_magnitude):
    male_range = [85, 180]
    female_range = [165, 255]
    frequency_mask = (male_range[0] <= fft_bins) & (fft_bins <= female_range[1])
    dominant_frequency = fft_bins[frequency_mask][np.argmax(fft_magnitude[frequency_mask])]
    avg_male_freq = np.mean(male_range)
    avg_female_freq = np.mean(female_range)
    gender = 'M' if abs(dominant_frequency - avg_male_freq) < abs(dominant_frequency - avg_female_freq) else 'K'
    return gender, dominant_frequency



def analyze_audio(file_path):
    audio, rate = load_audio(file_path)
    fft_bins = fftfreq(len(audio), d=1 / rate)
    processed_fft = signal_preprocessing(audio)
    gender_label, frequency = classify_gender(fft_bins, processed_fft)
    return gender_label, frequency


if __name__ == '__main__':
    try:
        input_file = sys.argv[1]
        gender, _ = analyze_audio(input_file)
        print(gender)

    except Exception:
        print('M')
