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
import io
from PIL import Image

# from keras.models import load_model

# Frecuencia de muestreo
fs = 44100
# Definir el umbral de silencio en dB
top_db = 20

# Definir los parámetros para el espectrograma de mel
n_fft_parameter = int(0.025 * fs)  # 25 ms en muestras
hop_length_parameter = int(n_fft_parameter/2)  # 10 ms en muestras
n_mels_parameter = 40


def preprocesamiento(signal):
    trimmed_signal = librosa.effects.trim(signal, top_db=20)
    reduced_noise_signal = nr.reduce_noise(trimmed_signal[0], fs)
    normalized_signal = librosa.util.normalize(reduced_noise_signal)

    fig, ax = plt.subplots()
    spectrum, frequs, t, im = ax.specgram(
        x=normalized_signal, Fs=fs, Fc=0, NFFT=n_fft_parameter, cmap=plt.cm.jet, scale='dB')
    ax.axis('off')
    buf = io.BytesIO()
    fig.savefig(buf, format='jpg', bbox_inches='tight',
                pad_inches=0, transparent=True)
    buf.seek(0)
    img = Image.open(buf)
    plt.close()

    box = (80, 58, 576, 427)
    img_crop = img.crop(box)
    img_array = np.asarray(img)

    return img_array


def entenderAudio(audioData):
    wav_data = audioData.get_wav_data()

    # Imprime la forma del arreglo de NumPy
    numpy_array = np.frombuffer(wav_data, dtype=np.int16)
    # Cambia el dtype a float64
    numpy_array = numpy_array.astype(np.float64)

    audioProccesed = preprocesamiento(numpy_array)
    prueba_signals = audioProccesed.reshape((1, 369, 496, 3))
    return prueba_signals
