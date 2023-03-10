from settings import *

# Los bloques al estar incluidos en un sprite group del padre, es necesario pasarle como parámetro un tetromino y su posición. El atributo de posición será un arreglo que contendrá la posición en X y Y del bloque a dibujar
class Block(pg.sprite.Sprite):
    def __init__(self,tetromino,pos):
        self.tetromino = tetromino

        # Para dibujar el bloque en pantalla, necesitamos las coordenadas del Tetromino padre y su atributo de Sprite_Group
        super().__init__(tetromino.tetris.sprite_group)
        # El método Surface permite la representación de imágenes en Pygame. Sus dos primeros parámetros son las medidas de la imagen.
        self.image = pg.Surface([TITLE_SIZE,TITLE_SIZE])
        self.image.fill("orange")

        self.rect = self.image.get_rect()
        # Dibujamos el rectángiulo en la esquina superior izquierda para que el rectángulo se ubique de manera correcta en la cuadrícula.
        self.rect.topleft = pos[0] * TITLE_SIZE,pos[1]*TITLE_SIZE   

class Tetromino:
    def __init__(self,tetris):
        self.tetris =tetris
        Block(self,(4,7))
    
    def update(self):
        pass