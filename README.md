# Tetrisfan

An implementation of speech recognizer created from Audio and Signals Processing subject at [UAO](https://www.uao.edu.co/) with Pygame. This last version uses the weights of a CNN created in `Proyecto_Tetrisfan_CNN.ipynb` for the prediction of the word said.

# Overview

-   🧠 [Getting Started](#getting-started)
-   🎮 [Running of the game](#🎮-running-of-the-game)
-   👥 [Credits and Attributions](#👥-credits-and-attributions)

# 🧠 Getting started

⚠ Note: This projects use [Python 3.8.10](https://www.python.org/downloads/release/python-3810/).

1. Install `virtualenv` to management the version of the libraries with `pip install virtualenv`.
2. Create a virtual enviroment with `python -m virtualenv env`.
3. Run `.\env\Scripts\activate` to active the virtual enviroment.
4. Run `pip install -r "requirements.txt"` to install all the libraries used with the specific version.
5. Open a terminal and run `python .\src\mainSocket.py` to launch the game. Wait and a message should appear saying: "Socket configurado 👻".
6. Open another terminal and run `python .\src\socket_client.py`. A message should appear saying: "Hable". From this moment, your microphone will open so you can pronunce one of the 5 words to give instructions to the game. Check [running of the game to more information](#🎮-running-of-the-game).
7. Play and test Tetrisfan 🤠

Para crear el fichero que contiene el nombre y versiones de las librerías utilizadas, se debe ejecutar en la terminal del entorno virual el siguiente código: `pip freeze > "requirements.txt"`

# 🎮 Running of the game

The speech recognizer identify 5 words, but only 4 has define instructions in the file `mainSocket.py` this way:

-   **Más**: move the current piece or tetromino to right.
-   **Menos**: move the current piece or tetromino to left.
-   **Girar**: turn left current piece or tetromino.
-   **Leprechaun**: increase the fall speed of tetromino radically.
-   **Empezar**: doesn't have and function implemented.

# 👥 Credits and Attributions

The base code of Tetris game was built thanks to
[Coder Space](https://www.youtube.com/@CoderSpaceChannel) and his video [Detailed Tetris Tutorial in Python](https://www.youtube.com/watch?v=RxWS5h1UfI4).

The Convolutional Neural Netword (CNN) buil drew inspiration from [VGG16](https://datagen.tech/guides/computer-vision/vgg16/).

If you want to know more about our projects, check our Github profiles:

-   [Andrés Felipe Aristizabal Miranda](https://github.com/Felipe-Aristizabal) - Multimedia engineer with focus on machine learning and videogames development.
-   [Hector Fabio Romero Bocanegra](https://github.com/Hector-f-Romero) - Multimedia engineer with focus on backend and software development.
