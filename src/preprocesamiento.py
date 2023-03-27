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
# from keras.utils import to_categorical

import noisereduce as nr
# Frecuencia de muestreo
fs = 44100    
# Definir el umbral de silencio en dB
top_db = 20

#Definir los parámetros para el espectrograma de mel
n_fft_parameter = int(0.025 * fs) # 25 ms en muestras
hop_length_parameter = int(n_fft_parameter/2) # 10 ms en muestras
n_mels_parameter = 40

# Definir las frecuencias de corte
lowcut = 3000
highcut = 6000

def butter_bandpass(lowcut, highcut, fs, order=2):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def preprocesamiento(audioBruto):
    # Quitar silencios 
    trimmed_signal, index = librosa.effects.trim(audioBruto, top_db=top_db)

    # Filtro pasa banda
    b, a = butter_bandpass(lowcut, highcut, fs, order=2)
    filtered_signal = filtfilt(b, a, trimmed_signal)

    # Normalizar las señales de audio
    normalized_signal = normalize(filtered_signal)
    return normalized_signal

  #Encontrar la señal de audio de mayor tamaño
#   max_len = 0
#   for signal in signals_norm:
#     length_signal = len(signal)
#     if length_signal > max_len:
#       max_len = length_signal

  #Hacer que todas las señales tengan el mismo tamaño
#   for signal in signals_norm:
#     fixed_signal = fix_length(signal, size=max_len)
#     signals_fixed.append(fixed_signal)

  

def extract_features(audioBruto):

    melspec = librosa.feature.melspectrogram(y =audioBruto, sr=fs, power=2, n_mels=n_mels_parameter, center=False, hop_length=hop_length_parameter, n_fft=n_fft_parameter)
    melspecM = np.mean(melspec.T, axis=0)

    melspec_db = librosa.power_to_db(melspec, ref=np.max)

    chroma = librosa.feature.chroma_stft(S=melspec_db, sr=fs)       
    chromaP = np.mean(chroma.T, axis=0)

    mfcc = librosa.feature.mfcc(y=audioBruto, n_mfcc=13)
    mfccM = np.mean(mfcc.T, axis=0)
    delta_mfcc = librosa.feature.delta(mfcc)
    delta_mfccM = np.mean(delta_mfcc.T, axis=0)
    delta_mfcc2 = librosa.feature.delta(mfcc, order=2)
    delta_mfcc2M = np.mean(delta_mfcc2.T, axis=0)
    
    features_signal = np.reshape(melspecM, (1, -1))
    features_signal = np.concatenate([mfccM, delta_mfccM, delta_mfcc2M, melspecM,chromaP])
    # features_signal = np.reshape(features_signal, (1, 79))
    features_signal = np.reshape(features_signal, (1, 91))

    return features_signal


def entenderAudio(audioData):
    # print(audioData)
    # print(type(audioData))
    # audio = librosa.load(audioData,sr=44100,mono=True)
    # print(audio)
    # Obtiene los datos de audio en formato WAV
    wav_data = audioData.get_wav_data()

    # Convierte los datos de audio WAV en un arreglo de NumPy
    # numpy_array = np.frombuffer(wav_data, dtype=np.float32)
    numpy_array = np.frombuffer(wav_data, dtype=np.int16)
    # print('Forma del arreglo de NumPy:', numpy_array.shape)

    # Verifica si np_audio es más largo que padlen
    # padlen = 15
    # if numpy_array.shape[0] > padlen:
    #     # Rellena los datos de audio con ceros al principio y al final
    #     np_padded_audio = np.pad(numpy_array, (padlen, padlen), 'constant', constant_values=0)
    #     print(np_padded_audio)

    #     audioProccesed = preprocesamiento(np_padded_audio)
    #     audioFeatures = extract_features(audioProccesed)
    #     return audioFeatures
        

    # Imprime la forma del arreglo de NumPy
    audioProccesed = preprocesamiento(numpy_array)
    audioFeatures = extract_features(audioProccesed)
    # print(audioFeatures.shape)
    return audioFeatures