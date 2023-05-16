from driver import Light, Touch
from imgs import get_img
from front3x5 import add_front
from snake import Snake

from random import randint

light = Light()
touch = Touch()

snake = Snake()
      
class Block:
    def __init__(self, mat, color):
        self.current_index = randint(0,3)
        self.buf = []
        self.buf.append(mat)
        self.color = color
        for it in range(3):
            new_mat = [[0 for _ in range(4)] for _ in range(4)]
            for i in range(4):
                for j in range(4):
                    new_mat[j][3-i] = mat[i][j]
            self.buf.append(new_mat)
            mat = new_mat
    
    def turn_right(self):
        self.current_index = (self.current_index + 1) % 4
    
    def turn_left(self):
        self.current_index = (self.current_index + 3) % 4
    
    def get_entry(self):
        block = self.buf[0]
        return Block(block, self.color)
    
    def render(self, img, pos):
        x, y = pos
        block = self.buf[self.current_index]
        for i in range(4):
            for j in range(4):
                if block[i][j]:
                    img[y+i][x+j] = self.color
        
class Tetris:
    def __init__(self):
        self.score = 0
        self.game_over = False
        self.blocks = []

        t = [[0,0,0,0],[1,1,1,0],[0,1,0,0],[0,0,0,0]]
        l1 = [[0,0,0,0],[0,1,0,0],[0,1,0,0],[0,1,1,0]]
        l2 = [[0,0,0,0],[0,0,1,0],[0,0,1,0],[0,1,1,0]]
        z1 = [[0,0,0,0],[1,1,0,0],[0,1,1,0],[0,0,0,0]]
        z2 = [[0,0,0,0],[0,1,1,0],[1,1,0,0],[0,0,0,0]]
        zero = [[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]]
        i = [[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0]]
        self.blocks.append(Block(t, (0,204,0)))
        self.blocks.append(Block(l1, (255,0,255)))
        self.blocks.append(Block(l2, (0,0,255)))
        self.blocks.append(Block(z1, (0,204,0)))
        self.blocks.append(Block(z2, (204,0,102)))
        self.blocks.append(Block(zero, (255,102,102)))
        self.blocks.append(Block(i, (255,255,0)))
        
        self.next_block = self.get_rand_block()
        self.face = [[0 for _ in range(10)] for _ in range(6)]
        
    def get_rand_block(self):
        block = self.blocks[randint(0, 6)]
        return block.get_entry()
        
    def get_img(self):
        def get_background():
            img = [[(0,0,0) for col in range(12)] for row in range(10)]
            for i in range(10):
                img[i][0] = (100,100,100)
                img[i][7] = (100,100,100)
            for i in range(4, 10):
                img[i][7] = (100,100,100)
                img[i][8] = (100,100,100)
            for i in range(9,12):
                img[4][i] = (100,100,100)
                img[5][i] = (100,100,100)
                img[6][i] = (100,100,100)
                img[7][i] = (100,100,100)
                img[8][i] = (100,100,100)
                img[9][i] = (100,100,100)
            return img
        img = get_background()
        self.next_block.renderimg, (8,0))
        return img
    
    def update_face(self):
        pass
    
    def main_loop(self):
        pass

tetris = Tetris()
img = tetris.get_img()
block = tetris.get_rand_block()
block.render(img, (1,0))
light.show(img)

# snake.main_loop(light, touch)


