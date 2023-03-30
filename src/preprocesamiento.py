# Importar librerias
from pathlib import Path
from scipy.io import wavfile
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt, IPython.display as ipd
import librosa, librosa.display
from librosa.util import normalize, fix_length
from scipy.signal import butter
from scipy.signal import filtfilt
import speech_recognition as sr
from sklearn import preprocessing
# from keras.utils import to_categorical

import noisereduce as nr
# Frecuencia de muestreo
fs = 44100    
# Definir el umbral de silencio en dB
top_db = 30

#Definir los parámetros para el espectrograma de mel
n_fft_parameter = int(0.025 * fs) # 25 ms en muestras
hop_length_parameter = int(n_fft_parameter/2) # 10 ms en muestras
n_mels_parameter = 40

# Definir las frecuencias de corte
lowcut = 4000
highcut = 5000

def butter_bandpass(lowcut, highcut, fs, order=2):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def preprocesamiento(audioBruto):
    # Quitar silencios 
    trimmed_signal, index = librosa.effects.trim(audioBruto, top_db=top_db)
    # print(trimmed_signal)
    # Filtro pasa banda
    b, a = butter_bandpass(lowcut, highcut, fs, order=2)
    filtered_signal = filtfilt(b, a, trimmed_signal)

    
      # print(normalized_signal)
    # print()
    # Normalizar las señales de audio
    normalized_signal = normalize(filtered_signal)

    # with np.printoptions(threshold=np.inf):
    #   print(filtered_signal)
    # normalized_signal = normalize(trimmed_signal)
    return normalized_signal

def entenderAudio(audioData):
    wav_data = audioData.get_wav_data()
    numpy_array = np.frombuffer(wav_data, dtype=np.int16)
    # Imprime la forma del arreglo de NumPy
    audioProccesed = preprocesamiento(numpy_array)
    # print("PASO ENTENDER AUDIO")
    audioFeatures = extract_features(audioProccesed)
    # print(audioFeatures.shape)
    return audioFeatures

def extract_features(audioNormalizado):
    print(audioNormalizado)
    melspec = librosa.feature.melspectrogram(y =audioNormalizado, sr=fs, power=2, n_mels=n_mels_parameter, center=False, hop_length=hop_length_parameter, n_fft=n_fft_parameter)
    print("PASO MEL")
    melspecM = np.mean(melspec.T, axis=0)
    
    melspec_db = librosa.power_to_db(melspec, ref=np.max)

    chroma = librosa.feature.chroma_stft(S=melspec_db, sr=fs)       
    chromaP = np.mean(chroma.T, axis=0)

    mfcc = librosa.feature.mfcc(y=audioNormalizado, n_mfcc=13)
    mfccM = np.mean(mfcc.T, axis=0)
    delta_mfcc = librosa.feature.delta(mfcc)
    delta_mfccM = np.mean(delta_mfcc.T, axis=0)
    delta_mfcc2 = librosa.feature.delta(mfcc, order=2)
    delta_mfcc2M = np.mean(delta_mfcc2.T, axis=0)
    
    features_signal = np.reshape(melspecM, (1, -1))
    features_signal = np.concatenate([mfccM, delta_mfccM, delta_mfcc2M, melspecM])
    features_signal = np.reshape(features_signal, (1, 79))
    # features_signal = np.reshape(features_signal, (1, 91))
    # features_signal =  preprocessing.MinMaxScaler(feature_range=(-1,1))

    return features_signal


