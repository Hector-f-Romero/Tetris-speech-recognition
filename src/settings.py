import pygame as pg

FPS= 60
FIELD_COLOR=(40,39,32)





TITLE_SIZE=30 # Tamaño de las cuadriculas
FIELD_SIZE =FIELD_W,FIELD_H = 10,20
FIELD_RES = FIELD_W * TITLE_SIZE,FIELD_H*TITLE_SIZE;

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

ANIM_TIME_INTERVAL = 150 # Milisegundos
