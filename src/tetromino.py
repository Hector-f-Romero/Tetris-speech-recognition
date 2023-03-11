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

    def rotate(self, pivot_pos):
        translated = self.pos - pivot_pos
        rotated = translated.rotate(90)
        return rotated + pivot_pos

    def set_rect_pos(self):
        # Se mueve la posición del bloque y se multiplica por el tamaño fijado.
        self.rect.topleft = self.pos *TITLE_SIZE

    def update(self):
        # Pintamos en pantalla la posición del bloque cada segundo
        self.set_rect_pos()

    def is_collide(self, pos):
        # Obtenemos los valores enteros de la posición actual del bloque
        x,y = int(pos.x),int(pos.y)

        # Si el bloque se encuentra dentro de los límites de la cuadrícula, no ha colisonado.
        # Y si el bloque no se encuentra ubicado en una posición ocupada anteriormente por otro bloque, aún se puede mover y retorna true
        if 0<= x < FIELD_W and y < FIELD_H and (y<0 or not self.tetromino.tetris.field_array[y][x]):
            return False
        return True

class Tetromino:
    def __init__(self,tetris):
        self.tetris =tetris
        # Se selecciona una forma aleatoria del diccionario creado en settings
        self.shape = random.choice(list(TETROMINOES.keys()))
        # Los bloques se crearán a partir de las posiciones dadas en el archivo settings y se construirán gracias a un ciclo for
        self.blocks = [Block(self,pos) for pos in TETROMINOES[self.shape]]
        self.landing = False # Esta propiedad indicará cuándo ha colisionado el tetromino con el suelo
    
    def is_collide(self, block_position):
        return any(map(Block.is_collide,self.blocks,block_position))
    
    def move(self,direction):
        # Busca el valor de la key que pasamos como parámetro en el diccionario
        move_direction = MOVE_DIRECTIONS[direction]

        # Guardamos en una variable la siguiente posición de los bloques
        new_block_positions = [block.pos + move_direction for block in self.blocks]
        # Verificamos si en esa nueva posición existe una colisión
        is_collide = self.is_collide(new_block_positions)

        # Si no existe colisión, cambiará la posición actual de los bloques.
        if not is_collide:
            for block in self.blocks:
                # Para cada uno de los bloques del tetromino se suma el vector perteneciente a la acción encontrada en el diccionario.
                block.pos +=move_direction
        elif direction == "down":
            self.landing = True

    def rotate(self):
        pivot_pos = self.blocks[0].pos
        # Rota cada uno de los bloques del tetromino
        new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

        if not self.is_collide(new_block_positions):
            for i,block in enumerate(self.blocks):
                block.pos = new_block_positions[i]


    def update(self):
        self.move(direction="down")
