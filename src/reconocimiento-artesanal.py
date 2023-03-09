import numpy as np
import matplotlib.pyplot as plt
import librosa;
import librosa.display
from pathlib import Path
from scipy import signal

# Frecuencia de muestreo
fs = 44100

# print(os.path.join(os.getcwd(),"/audios/Más.wav"))
# print(audioPath)

# fig, ax =  plt.subplots(nrows=3, sharex=True)

# plt.figure(figsize=(14, 5))

# El método load retorna un arreglo de Numpy que contiene el dominio de la señal de audio y el número de muestras de este arreglo
y,sr = librosa.load("Mas.wav",mono=True,sr=fs)

librosa.display.waveshow(y,sr=fs);

# ? Calculamos la stft para consturir el espectograma
plt.figure(figsize=(14, 5))
Y = librosa.stft(y)
Xdb = librosa.amplitude_to_db(abs(Y))
librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz',)
plt.colorbar()

# ? Se procede a remover los silencios
audio_trimmed,_ = librosa.effects.trim(y, top_db= 20)
# plt.plot(clip)
print('Audio File shape:', np.shape(audio_trimmed))
plt.show()


# ? Se realiza el espectrograma de Mel para conocer en decibeles las características del audio
s1 = librosa.feature.melspectrogram(y=y,sr=fs,n_mels=64)
# Convierte la información a escala de dB
d1 = librosa.power_to_db(s1, ref=np.max)
librosa.display.specshow(d1, x_axis='time', y_axis='mel')
plt.title('Mel power spectrogram')
plt.show()

# ? librosa.effects.hpss: descompone el audio en series de armónicos y componentes de percusión.
y_harm, y_perc = librosa.effects.hpss(y)
plt.figure(figsize = (16, 6))
plt.plot(y_harm, color = '#A300F9');
plt.plot(y_perc, color = '#FFB100');
plt.show()

def filtro_pasa_alta(y,Fs):
    b,a = signal.butter(10, 2048/(Fs/2), btype='highpass')
    yf = signal.lfilter(b,a,y)
    return yf

yf1 = filtro_pasa_alta(y, fs)

librosa.display.waveshow(y,sr=fs, x_axis='time');
librosa.display.waveshow(yf1,sr=fs, x_axis='time');
plt.show()