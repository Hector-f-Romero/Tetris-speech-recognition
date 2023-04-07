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
import noisereduce as nr
import joblib
import pathlib
from keras.models import load_model

import soundfile as sf

# Frecuencia de muestreo
fs = 44100    
# Definir el umbral de silencio en dB
top_db = 20

#Definir los parámetros para el espectrograma de mel
n_fft_parameter = int(0.025 * fs) # 25 ms en muestras
hop_length_parameter = int(n_fft_parameter/2) # 10 ms en muestras
n_mels_parameter = 40

# ?------------------------------------------------------------------------------------
r = sr.Recognizer()
r.energy_threshold=4000
m = sr.Microphone(0,sample_rate=22050)

# Obtenemos el path actual del archivo main.py
current_path = pathlib.Path(__file__).parent
modelo_ruta = pathlib.Path(current_path / "assets" / "models" / "DiosPadre-DiosHijo-DiosEspirituSanto.joblib")
# modelo_ruta = pathlib.Path(current_path / "assets" / "models" / "ModelSinMas.joblib")
# modelo_ann_ruta = pathlib.Path(current_path / "assets" / "models" / "modelo_porfavorfunciona077.h5")

# Se carga el modelo de red neuronal entrenado.
modelo_entrenado = joblib.load(modelo_ruta)
# ?------------------------------------------------------------------------------------

def preprocesamiento(audioBruto):
    # Quitar silencios
    audio,sr = librosa.load(path=audioBruto,sr=fs/2,mono=True) 
    
    trimmed_signal, index = librosa.effects.trim(audio, top_db=top_db)
    normalized_signal = normalize(trimmed_signal)
    normalized_noise_reduced = nr.reduce_noise(normalized_signal, sr=fs)
    
    # with open("ayuda.wav","wb") as f:
    sf.write("Normalizado.wav",data=normalized_noise_reduced,samplerate=44100)

    return normalized_noise_reduced

def entenderAudio(audioData):
    wav_data = audioData.get_wav_data()
    with open("ayuda.wav","wb") as f:
         f.write(wav_data)

    # Imprime la forma del arreglo de NumPy
    # numpy_array = np.frombuffer(wav_data, dtype=np.int16)
    # Cambia el dtype a float64
    # numpy_array = numpy_array.astype(np.float64)

    # audioProccesed = preprocesamiento(numpy_array)
    # audioFeatures = extract_features(audioProccesed)
    audioProccesed = preprocesamiento("ayuda.wav")
    audioFeatures = extract_features(audioProccesed)

    return audioFeatures

def extract_features(audioNormalizado):
    print(audioNormalizado.dtype)
    melspec = librosa.feature.melspectrogram(y =audioNormalizado, sr=fs, power=2, n_mels=n_mels_parameter, center=False, hop_length=hop_length_parameter, n_fft=n_fft_parameter)
    melspecM = np.mean(melspec.T, axis=0)
    
    mfcc = librosa.feature.mfcc(y=audioNormalizado, n_mfcc=13)
    mfccM = np.mean(mfcc.T, axis=0)
    delta_mfcc = librosa.feature.delta(mfcc)
    delta_mfccM = np.mean(delta_mfcc.T, axis=0)
    delta_mfcc2 = librosa.feature.delta(mfcc, order=2)
    delta_mfcc2M = np.mean(delta_mfcc2.T, axis=0)
    
    features_signal = np.reshape(melspecM, (1, -1))
    features_signal = np.hstack([mfccM, delta_mfccM, delta_mfcc2M, melspecM])
    features_signal = np.expand_dims(features_signal, axis=0)
    return features_signal

if __name__ == "__main__":
    with m as source:
        try:
            print("Hable")
            # r.adjust_for_ambient_noise(source)
            audio = r.listen(source) #,,,,,timeout=4 ,phrase_time_limit=3
            palabra_predictor = entenderAudio(audio)
            print(palabra_predictor.dtype)
            # model = load_model("modeloporfavorfunciona077.h5")

            predicion, = modelo_entrenado.predict(palabra_predictor) #.argmax(axis=0)
            y_prob = modelo_entrenado.predict_proba(palabra_predictor)
            print(predicion)
            print(y_prob)
            # predi = model.predict(palabra_predictor)
            # print(predi)
            if(predicion == 0):
                desicion = "Empezar"
            elif(predicion == 1):
                desicion = "Girar"
            elif(predicion == 2):
                desicion = "Leprechaun"
            elif(predicion == 3):
                 desicion = "Mas"
            elif(predicion == 4):
                desicion = "Menos"
            else:
                desicion = ""
            # print(desicion)
            # print(y_prob)
        except Exception as e:
                print(f"Excepcion: {str(e)}")


