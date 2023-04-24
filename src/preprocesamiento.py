# Importar librerias
from pathlib import Path
from scipy.io import wavfile
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import IPython.display as ipd
import librosa
import librosa.display
from librosa.util import normalize, fix_length
from scipy.signal import butter
from scipy.signal import filtfilt
import speech_recognition as sr
from sklearn import preprocessing
import noisereduce as nr

# from keras.models import load_model

# Frecuencia de muestreo
fs = 44100
# Definir el umbral de silencio en dB
top_db = 20

# Definir los parámetros para el espectrograma de mel
n_fft_parameter = int(0.025 * fs)  # 25 ms en muestras
hop_length_parameter = int(n_fft_parameter/2)  # 10 ms en muestras
n_mels_parameter = 40


def preprocesamiento(audioBruto):
    trimmed_signal = librosa.effects.trim(audioBruto, top_db=20)
    reduced_noise_signal = nr.reduce_noise(trimmed_signal[0], sr=fs)
    normalized_signal = librosa.util.normalize(reduced_noise_signal)

    melspec = librosa.feature.melspectrogram(y=normalized_signal, sr=fs, power=2, n_mels=n_mels_parameter,
                                             center=False, hop_length=hop_length_parameter, n_fft=n_fft_parameter)
    melspecM = np.mean(melspec.T, axis=0)

    mfcc = librosa.feature.mfcc(y=normalized_signal, n_mfcc=13)
    mfccM = np.mean(mfcc.T, axis=0)
    delta_mfcc = librosa.feature.delta(mfccM)
    delta2_mfcc = librosa.feature.delta(mfccM, order=2)

    chroma = librosa.feature.chroma_stft(y=normalized_signal, sr=fs)
    chromaM = np.mean(chroma.T, axis=0)

    signal_features = np.hstack(
        (mfccM, delta_mfcc, delta2_mfcc, melspecM, chromaM))
    # print(signal_features.shape)
    signal_features = np.reshape(signal_features, (1, 91))
    # print(signal_features.shape)
    return signal_features


def entenderAudio(audioData):
    wav_data = audioData.get_wav_data()

    # Imprime la forma del arreglo de NumPy
    numpy_array = np.frombuffer(wav_data, dtype=np.int16)
    # Cambia el dtype a float64
    numpy_array = numpy_array.astype(np.float64)

    audioProccesed = preprocesamiento(numpy_array)
    return audioProccesed
