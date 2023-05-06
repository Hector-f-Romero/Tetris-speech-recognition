# Tetris - PDSA

Se debe crear un entorno virtual para instalar los paquetes de este proyecto. Para crear un entorno virtual se debe ejecutar los siguientes pasos:

(Instalar la libreria `virtualenv` de antemano).

```
python -m virtualenv env

# Activa el entorno virtual
.\env\Scripts\activate

pip install -r "requirements.txt"

```

Para crear el fichero que contiene el nombre y versiones de las librerías utilizadas, se debe ejecutar en la terminal del entorno virual el siguiente código: `pip freeze > "requirements.txt"`

# Funcionamiento del juego

1. Ejecutar en una terminal el archivo `mainSocket.py` para que Pygame ejecute el juego y esperar a que en consola aparezca el mensaje "Socket configurado 👻".
2. Ejecutar en una terminal diferente el archivo `socket_client.py`.
3. En la primera terminal verá las acciones que el modelo entrenado detectó desde la segunda terminal.
4. Disfrute de la experiencia.
