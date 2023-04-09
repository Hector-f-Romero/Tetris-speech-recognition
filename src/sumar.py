import time

def sumarChimbita(getter,setter):
    while True:
        value = getter()
        print(f"En sumar chimbita, el valor del getter es: {value}")
        a = 2
        b = value +a
        setter(b)
        time.sleep(3)
    # func()
    
