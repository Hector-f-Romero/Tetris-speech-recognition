import numpy as np
import matplotlib.pyplot as plt
import librosa;
import librosa.display

# Frecuencia de muestreo
fs = 44100

# El método load retorna un arreglo de Numpy y el número de muestras de este arreglo
y,sr = librosa.load("./audios/Más-HectorRomero-1.wav",mono=True,sr=fs)

librosa.display.waveshow(y,sr=fs);
plt.show()

