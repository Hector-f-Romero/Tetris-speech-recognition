from settings import *
import random

# Los bloques al estar incluidos en un sprite group del padre, es necesario pasarle como parámetro un tetromino y su posición. El atributo de posición será un arreglo que contendrá la posición en X y Y del bloque a dibujar
class Block(pg.sprite.Sprite):
    def __init__(self,tetromino,pos):
        self.tetromino = tetromino
        self.pos = vec(pos) + INIT_POS_OFFSET

        # Para dibujar el bloque en pantalla, necesitamos las coordenadas del Tetromino padre y su atributo de Sprite_Group
        super().__init__(tetromino.tetris.sprite_group)
        # El método Surface permite la representación de imágenes en Pygame. Sus dos primeros parámetros son las medidas de la imagen.
        self.image = pg.Surface([TITLE_SIZE,TITLE_SIZE])
        self.image.fill("orange")
        # Dibujamos el rectángulo en la esquina superior izquierda para que el rectángulo se ubique de manera correcta en la cuadrícula.
        self.rect = self.image.get_rect()

    def set_rect_pos(self):
        # Se mueve la posición del bloque y se multiplica por el tamaño fijado.
        self.rect.topleft = self.pos *TITLE_SIZE

    def update(self):
        self.set_rect_pos()

class Tetromino:
    def __init__(self,tetris):
        self.tetris =tetris
        # Se selecciona una forma aleatoria del diccionario creado en settings
        self.shape = random.choice(list(TETROMINOES.keys()))
        # Los bloques se crearán a partir de las posiciones dadas en el archivo settings y se construirán gracias a un ciclo for
        self.blocks = [Block(self,pos) for pos in TETROMINOES[self.shape]]
    
    def move(self,direction):
        # Busca el valor de la key que pasamos como parámetro en el diccionario
        move_increment = MOVE_DIRECTIONS[direction]
        for block in self.blocks:
            # Para cada uno de los bloques del tetromino se suma el vector perteneciente a la acción encontrada en el diccionario.
            block.pos +=move_increment

    def update(self):
        self.move(direction="down")