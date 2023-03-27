import pygame as pg

FPS= 60
FIELD_COLOR=(40,39,32)

TILE_SIZE=30 # Tamaño de las cuadriculas
FIELD_SIZE =FIELD_W,FIELD_H = 6,27
FIELD_RES = FIELD_W * TILE_SIZE,FIELD_H*TILE_SIZE;

# Aumentamos el tamaño de la ventana para agregar el sistema de puntos y visualización de la siguiente ficha.
FIELD_SCALE_W,FIELD_SCALE_H = 2.7,1.0
WIN_RES = WIN_W,WIN_H = FIELD_RES[0] * FIELD_SCALE_W, FIELD_RES[1] * FIELD_SCALE_H
BG_COLOR = (24,89,117)


# En este diccionario, se almacenan las coordenas de las figuras del tetris. El primer par de coordenadas hace refernecia al bloque de pivote, el cuál será la guía para la construcción de los otros bloques y así formar un tetromino
TETROMINOES = {
    'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
    'O': [(0, 0), (0, -1), (1, 0), (1, -1)],
    'J': [(0, 0), (-1, 0), (0, -1), (0, -2)],
    'L': [(0, 0), (1, 0), (0, -1), (0, -2)],
    'I': [(0, 0), (0, 1), (0, -1), (0, -2)],
    'S': [(0, 0), (-1, 0), (0, -1), (1, -1)],
    'Z': [(0, 0), (1, 0), (0, -1), (-1, -1)]
}

# Creamos un vector2D para gestionar de mejor manera la ubicación de las coordenadas de los bloques. Además, necesitamos darle un desplazamiento inicial para que el tetromino se vea completo en pantalla
vec = pg.math.Vector2
# La posición inicial del bloque aparecerá en la mitad de la pantalla horizontalmente y la posición 0 del canvas verticalmente
INIT_POS_OFFSET = vec(FIELD_W // 2 -1,0)   

# Gracias al vector2, podemos mover todas las figuras de forma sencilla al sumar los siguientes valores en X y Y
MOVE_DIRECTIONS = {"left":vec(-1,0),'right': vec(1, 0), 'down': vec(0, 1)}

# ANIM_TIME_INTERVAL = 750 # Milisegundos
ANIM_TIME_INTERVAL = 950 # Milisegundos
FAST_ANIM_TIME_INTERVAL = 15 # Milisegundos

SPRITE_DIR_PATH = "assets/sprites"
FONT_PATH ="assets/font/Montserrat-Bold.ttf"



NEXT_POS_OFFSET = vec(FIELD_W*1.8,FIELD_H*0.45)
