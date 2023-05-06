import socket
import speech_recognition as sr
import pathlib
import tensorflow as tf
import time

from preprocesamientoConv import entenderAudio

# * --------------------------------------------------
# AJUSTES DEL SPEECH RECOGNITION
r = sr.Recognizer()
r.energy_threshold = 4000
m = sr.Microphone(0, sample_rate=44100)

# Obtenemos el path actual del archivo main.py
current_path = pathlib.Path(__file__).parent
modelo_ruta = pathlib.Path(current_path / "assets" /
                           "models" / "Nika_Cenit.h5")

# Se carga el modelo de red neuronal entrenado.
modelo_entrenado = tf.keras.models.load_model(modelo_ruta)

# * --------------------------------------------------


def start_recognizer():
    while True:
        with m as source:
            try:
                mi_socket = socket.socket()
                mi_socket.connect(("localhost", 8000))
                print("Hable")
                audio = r.listen(source, phrase_time_limit=3)
                palabra_predictor = entenderAudio(audio)
                predicion = modelo_entrenado.predict(
                    palabra_predictor, verbose=0).argmax()
                desicion = ""
                if (predicion == 0):
                    desicion = "Empezar"
                elif (predicion == 1):
                    desicion = "Girar"
                elif (predicion == 2):
                    desicion = "Leprechaun"
                elif (predicion == 3):
                    desicion = "Mas"
                elif (predicion == 4):
                    desicion = "Menos"
                else:
                    desicion = ""
                # print(desicion)
                mi_socket.send(desicion.encode())
                mi_socket.close()

                time.sleep(0.5)
                print("-----------------------")
            except Exception as e:
                print(f"Excepcion: {str(e)}")


if __name__ == "__main__":
    start_recognizer()
