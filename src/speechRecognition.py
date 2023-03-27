import speech_recognition as sr
import time
import joblib
import pathlib

from multiprocessing import Process, Queue
# from shared_variable import set_shared_variable,get_shared_variable
from accionTomada import VariableCompartida

from preprocesamiento import entenderAudio
# from main import mi_accion

r = sr.Recognizer()
r.energy_threshold=4000
m = sr.Microphone(0,sample_rate=44100)
# m = sr.Microphone(0,sample_rate=22050)

# Obtenemos el path actual del archivo main.py
current_path = pathlib.Path(__file__).parent
# modelo_ruta = pathlib.Path(current_path / "assets" / "models" / "Model081.joblib")
modelo_ruta = pathlib.Path(current_path / "assets" / "models" / "my_random_forest.joblib")

# Se carga el modelo de red neuronal entrenado.
modelo_entrenado = joblib.load(modelo_ruta)


mi_accion = VariableCompartida()

def callback(recognizer, audio):
    try:
        if(audio):
            soyMain(audio)
    except Exception as e:
        print(f"Excepcion: {str(e)}")

def soyMain(audio):
    palabra_predictor = entenderAudio(audio)
    # accion_escogida = 
    # print(palabra_predictor.shape)
    predicion, =modelo_entrenado.predict(palabra_predictor)
    y_prob = modelo_entrenado.predict_proba(palabra_predictor)
    accion = escoger_accion(predicion)
    # set_shared_variable(accion)
    mi_accion.actualizar_valor(accion)
    print(predicion)
    print(mi_accion.obtener_valor())
    # print(accion)
    print("----------------------------")
    # print("Vuelta...")
    # print(get_shared_variable())

def escoger_accion(comando_voz):
    desicion = ""
    if(comando_voz == 0):
        desicion = 0
    elif(comando_voz == 1):
        desicion = 1
    elif(comando_voz == 2):
        desicion = 2
    elif(comando_voz == 3):
        desicion = 3
    elif(comando_voz == 4):
        desicion = 4
    elif(comando_voz == 5):
        desicion = 5
    else:
        desicion = "Nose"
    return desicion

def start_recognizer():
    print("En start_recognizer")
    r.listen_in_background(m,callback=callback) #,phrase_time_limit=300
    while True:
        time.sleep(1000)
        
if __name__ == "__main__":
    start_recognizer()