import speech_recognition as sr
import time


r = sr.Recognizer()
r.energy_threshold=4000
m = sr.Microphone(0)

def callback(recognizer, audio):
    try:
        print(audio)
        if(audio):
            soyMain()
    except Exception as e:
        print(f"Excepcion: {str(e)}")

def soyMain():
    print("Estoy en el main :D")

def start_recognizer():
    print("En start_recognizer")
    r.listen_in_background(m,callback=callback,phrase_time_limit=300)
    time.sleep(1000000)

if __name__ == "__main__":
    # get_audio()
    start_recognizer()