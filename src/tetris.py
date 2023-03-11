from settings import *
from tetromino import Tetromino
import math

# La clase Tetris llevará el control de los elemtentos Tetromino y la visualización en pantalla de la grilla
class Tetris:
    def __init__(self,app):
        self.app =app
        self.field_array = self.get_field_array()
        # En este group, estarán todas las texturas de los Tetrominos y bloques que aparecerán en pantalla
        self.sprite_group = pg.sprite.Group()
        self.tetromino = Tetromino(self)

    # Para el sistema de colisiones entre bloques, es necesario mapear la cuadricula y conocer qué posicones están libres.
    def get_field_array(self):
        return [[0 for x in range(FIELD_W)] for y in range(FIELD_H)]

    def put_tetromino_blocks_in_array(self):
        for block in self.tetromino.blocks:
            x,y = int(block.pos.x),int(block.pos.y)
            # Guardamos las posiciones de los tetrominos en el arreglo de field_array y así podremos analizar que partes de la cuadrícula están ocupadas.
            self.field_array[y][x] = block

    def control(self,pressed_key):
        if pressed_key == pg.K_LEFT:
            self.tetromino.move(direction="left")
        elif pressed_key == pg.K_RIGHT:
            self.tetromino.move(direction="right")
        elif pressed_key == pg.K_UP:
            # Si presiona la tecla hacia arriba del teclado, el tetromino rota hacia la ¿izquierda?
            self.tetromino.rotate()

    # Dibuja la cuadrícula en pantalla con base en los ajustes del archivo "settings"
    def draw_grid(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.app.screen,"black",(x*TITLE_SIZE,y*TITLE_SIZE,TITLE_SIZE,TITLE_SIZE),1)

    # Este método verifica si el tetromino ha tocado el suelo o no
    def check_tetromino_landing(self):
        if self.tetromino.landing:
            # Coloca la posición del tetromino en el arreglo que contiene la información de la cuadrícula.
            self.put_tetromino_blocks_in_array()
            # SI el tetromino toca el suelo, se generará una nueva instancia de Tetromino
            self.tetromino = Tetromino(self)

    def update(self):
        if self.app.anim_trigger:
            self.tetromino.update()
            self.check_tetromino_landing()
        self.sprite_group.update()

    def draw(self):
       self.draw_grid()
       # Dibujará los sprites en la superficie de la pantalla de la aplicación previamente creada.
       self.sprite_group.draw(self.app.screen)

 