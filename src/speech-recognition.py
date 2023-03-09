import speech_recognition as sr;

def reconocerVoz():
    # * Se inicializa el micrófono.
    sr.Microphone(device_index=0);
    # sr.Microphone();
    # * Creamos un objeto de reconocimiento.
    r = sr.Recognizer()
    # * Representa el umbral desde el cuál se empezará a considerar voz del audio. Los valores por debajo de esta propiedad serán considerados silencios
    r.energy_threshold=4000
    # r.dynamic_energy_threshold = False;

    # Representa la mínima cantida de silencio en segundos que puede existir antes de que se corte a grabación.
    # r.non_speaking_duration = 0.5
    # r.pause_threshold=0.6;

    with sr.Microphone() as source:
        try:
            # r.adjust_for_ambient_noise(source,duration=0.2)
            print("Hable ahora...")

            audio = r.listen(source)
            text = r.recognize_google(audio,language="es-CO")
            print(f"Se reconoció: {text}")
        except TimeoutError:
            print("Se tardó demasiado tiempo en hablar.")
            quit()
        except sr.UnknownValueError:
            print("No se entendió.")
        else:
            print("Se escuchó nítido 😎")


reconocerVoz()