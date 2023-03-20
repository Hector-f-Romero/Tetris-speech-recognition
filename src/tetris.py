from settings import *
from tetromino import Tetromino
import pygame.freetype as ft
import pathlib
import math

# La clase Tetris llevará el control de los elemtentos Tetromino y la visualización en pantalla de la grilla
class Tetris:
    def __init__(self,app):
        self.app =app
        self.field_array = self.get_field_array()
        # En este group, estarán todas las texturas de los Tetrominos y bloques que aparecerán en pantalla
        self.sprite_group = pg.sprite.Group()
        self.tetromino = Tetromino(self)
        self.speed_up = False
        # Crearemos el tetromino siguiente para poder visualizarlo en la pantalla antes de que salga
        self.next_tetromino = Tetromino(self,current=False)
        self.score =0
        self.full_lines = 0
        self.points_per_lines = {0:0,1:200,2:400,3:700,4:1500}

    def get_score(self):
        self.score += self.points_per_lines[self.full_lines]
        self.full_lines = 0 

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
        elif pressed_key == pg.K_DOWN:
            self.speed_up = True

    # Dibuja la cuadrícula en pantalla con base en los ajustes del archivo "settings"
    def draw_grid(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.app.screen,"black",(x*TILE_SIZE,y*TILE_SIZE,TILE_SIZE,TILE_SIZE),1)

    # Este método verifica si el tetromino ha tocado el suelo o no
    def check_tetromino_landing(self):
        if self.tetromino.landing:
            # Si el método de is_game_over retorna True, se inicializa nuevamente el juego reiniciando la app.
            if self.is_game_over():
                self.__init__(self.app)
            else:
                self.speed_up = False
                # Coloca la posición del tetromino en el arreglo que contiene la información de la cuadrícula.
                self.put_tetromino_blocks_in_array()
                self.next_tetromino.current = True
                # Asignamos el valor del tetromino siguiente al actual y creamos una nuevo con el atributo de current en False
                self.tetromino = self.next_tetromino
                # SI el tetromino toca el suelo, se generará una nueva instancia de Tetromino
                self.next_tetromino = Tetromino(self,current=False)

    def check_full_lines(self):
        row = FIELD_H-1
        for y in range(FIELD_H-1,-1,-1):
            for x in range(FIELD_W):
                self.field_array[row][x] = self.field_array[y][x]

                if(self.field_array[y][x]):
                    self.field_array[row][x].pos = vec(x,y)

            # Se verifica el número de bloques en la línea actual
            if sum(map(bool,self.field_array[y])) < FIELD_W:
                # Si no está completa la fila, reducimos el valor de la variable row en 1
                row -=1
            else:
                for x in range(FIELD_W):
                    self.field_array[row][x].alive = False
                    # Eliminamos todos los valores de la fila colocando 0
                    self.field_array[row][x] = 0

                # Suma las líneas completas
                self.full_lines +=1

    def update(self):
        trigger = [self.app.anim_trigger,self.app.fast_anim_trigger][self.speed_up]
        if trigger:
            self.check_full_lines()
            self.tetromino.update()
            self.check_tetromino_landing()
            self.get_score()
        self.sprite_group.update()

    def draw(self):
       self.draw_grid()
       # Dibujará los sprites en la superficie de la pantalla de la aplicación previamente creada.
       self.sprite_group.draw(self.app.screen)

    def is_game_over(self):
        # Si el tetromino se encuentra en el tope de la pantalla, se pausa el juego y devuelve True
        if self.tetromino.blocks[0].pos.y == INIT_POS_OFFSET[1]:
            pg.time.wait(1300)
            return True

class Text:
    def __init__(self,app):
        self.app = app
        # Obtenemos el path actual del archivo main.py
        current_path = pathlib.Path(__file__).parent
        # Guardamos la ruta donde se encuentran los sprites
        font_path = pathlib.Path(current_path / FONT_PATH)
        # Cargamos la fuente en la ruta especificada.
        self.font = ft.Font(font_path)

    def draw(self):
        self.font.render_to(self.app.screen,(WIN_W*0.607,WIN_H*0.02),text="TETRISFÁN",fgcolor="white",size=TILE_SIZE*1.15,bgcolor="black")
        self.font.render_to(self.app.screen, (WIN_W * 0.65, WIN_H * 0.22),text='Next', fgcolor='orange',size=TILE_SIZE * 1.4)
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.67),text='Score', fgcolor='orange',size=TILE_SIZE * 1.4)
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.8), text=f'{self.app.tetris.score}', fgcolor='white',size=TILE_SIZE * 1.8)