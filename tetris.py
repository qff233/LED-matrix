from random import randint
from time import sleep, ticks_ms
from front3x5 import add_front

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
    
    def get_buf(self):
        return self.buf[self.current_index]
    
    def get_entry(self):
        block = self.buf[0]
        return Block(block, self.color)
    
    def get_color(self):
        return self.color
    
    def render(self, img, pos):
        x, y = pos
        block = self.buf[self.current_index]
        for i in range(4):
            for j in range(4):
                if block[i][j]:
                    if y+i > 10:
                        continue
                    img[y+i][x+j] = self.color

class Direction:
    TurnRight = 8
    TurnLeft  = 4
    Right     = 9
    Left      = 5
    Down      = 7
    Nil       = 11

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
        
        self.current_block = self.get_rand_block()
        self.next_block = self.get_rand_block()
        self.block_x = randint(0,2)
        self.block_y = 0
        self.face = [[0 for _ in range(8)] for _ in range(11)]
        for it in range(8):
            self.face[10][it] = 1
        for it in range(10):
            self.face[it][0] = 1
            self.face[it][7] = 1
        self.face_color = [[(0,0,0) for _ in range(6)] for _ in range(10)]
        
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
        
        if not self.game_over:
            img = get_background()
            self.current_block.render(img, (self.block_x+1, self.block_y))
            for i in range(10):
                for j in range(6):
                    if img[i][j+1] == (0,0,0):
                        img[i][j+1] = self.face_color[i][j]
            self.next_block.render(img, (8,0))
            return img
        else:
            print("游戏结束！", self.score)
            img = [[(0,0,0) for col in range(12)] for row in range(10)]
            nums = []
            while True:
                nums.insert(0, int(self.score) % 10)
                self.score = int(self.score) / 10
                if int(self.score) == 0:
                    break
            for i in range(len(nums)):
                row = int(i / 3)
                col = int(i % 3)
                add_front(img, (col*4, row*5), str(nums[i]))
            return img

    def block_and_face(self, direction):  # 方块和固定的方块做与操作
        buf = self.current_block.get_buf()
        if direction == Direction.Nil:
            for i in range(4):
                for j in range(4):
                    if j + self.block_x > 7 or j + self.block_x < 0:
                        continue
                    if self.face[i+self.block_y][j + self.block_x+1] & buf[i][j]:
                        return True
            return False
        elif direction == Direction.Down:
            for i in range(4):
                for j in range(4):
                    if j + self.block_x + 1 > 7 or j + self.block_x < 0:
                        continue
                    if self.face[i+self.block_y+1][j + self.block_x+1] & buf[i][j]:
                        return True
            return False
        elif direction == Direction.Left:
            for i in range(4):
                for j in range(4):
                    if j + self.block_x < 0:
                         continue
                    if self.face[i+self.block_y][j + self.block_x] & buf[i][j]:
                        return True
            return False
        elif direction == Direction.Right:
            for i in range(4):
                for j in range(4):
                    if j + 2 + self.block_x > 7:
                        continue
                    if self.face[i+self.block_y][j + 2 + self.block_x] & buf[i][j]:
                        return True
            return False
        elif direction == Direction.TurnLeft:
            self.current_block.turn_left()
            buf = self.current_block.get_buf()
            for i in range(4):
                for j in range(4):
                    if j + self.block_x > 7:
                        continue
                    if self.face[i+self.block_y][j + 1 + self.block_x] & buf[i][j]:
                        self.current_block.turn_right()
                        return True
            self.current_block.turn_right()
            return False
        elif direction == Direction.TurnRight:
            self.current_block.turn_right()
            buf = self.current_block.get_buf()
            for i in range(4):
                for j in range(4):
                    if j + self.block_x > 7:
                        continue
                    if self.face[i+self.block_y][j + 1 + self.block_x] & buf[i][j]:
                        self.current_block.turn_left()
                        return True
            self.current_block.turn_left()
            return False
        
    def move_down(self):
        self.block_y = self.block_y + 1
        
    def update(self):
        def update_face(buf):
            for i in range(4):
                for j in range(4):
                    if self.block_x+j+1 > 7:
                        continue
                    self.face[self.block_y+i][self.block_x+j+1] = self.face[self.block_y+i][self.block_x+j+1] | buf[i][j]
        def update_face_color(buf, color): # 更改face的渲染列表
            for i in range(4):
                for j in range(4):
                    if self.block_y+i > 9 or self.block_x+j > 5:
                        continue
                    if buf[i][j] and self.face_color[self.block_y+i][self.block_x+j] == (0,0,0):
                        self.face_color[self.block_y+i][self.block_x+j] = color
        def update_block():
            self.current_block = self.next_block
            self.next_block = self.get_rand_block()
            self.block_x = randint(0,2)
            self.block_y = 0
        def remove_bottom(): # 判断消除行  加分数
            remove_count = 0
            while True:
                count = 0
                for i in range(len(self.face)-1):
                    if self.face[i] == [1,1,1,1,1,1,1,1]:
                        self.face.pop(i)
                        print(i)
                        self.face_color.pop(i)
                        remove_count = remove_count + 1
                        count = count + 1
                        self.score = self.score + 50
                        break
                if count == 0:
                    break
            for i in range(remove_count):
                face_row = [1,0,0,0,0,0,0,1]
                face_color_raw = [(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)]
                self.face.insert(0, face_row)
                self.face_color.insert(0, face_color_raw)
                print(self.face_color)
                print(self.face)
        
        buf = self.current_block.get_buf()
        if self.block_and_face(Direction.Down):  # 下一步有方块卡住
            color = self.current_block.get_color()
            update_face_color(buf, color)
            update_face(buf)
            print(self.face)
            remove_bottom()
            update_block()
            if self.block_and_face(Direction.Nil): # 判断游戏结束
                self.game_over = True
                return
        
    def main_loop(self, light, touch):
        def get_key():
            if touch.is_touch(Direction.TurnRight):
                return Direction.TurnRight
            elif touch.is_touch(Direction.TurnLeft):
                return Direction.TurnLeft
            elif touch.is_touch(Direction.Right):
                return Direction.Right
            elif touch.is_touch(Direction.Left):
                return Direction.Left
            elif touch.is_touch(Direction.Down):
                return Direction.Down
            else:
                return Direction.Nil
            
        time_stamp = ticks_ms()
        last_key = Direction.Nil
        del_time = 500
        while True:
            if self.game_over:
                while True:
                    if touch.is_touch(10):
                        break
                    sleep(1.0)
                break
            current_time = ticks_ms()
            key = get_key()
            if key != last_key:
                if key == Direction.TurnRight:
                    last_key = Direction.TurnRight
                    if not self.block_and_face(last_key):
                        self.current_block.turn_right()
                elif key == Direction.TurnLeft:
                    last_key = Direction.TurnLeft
                    if not self.block_and_face(last_key):
                        self.current_block.turn_left()
                elif key == Direction.Right:
                    last_key = Direction.Right
                    if not self.block_and_face(last_key):
                        self.block_x = self.block_x + 1
                elif key == Direction.Left:
                    last_key = Direction.Left
                    if not self.block_and_face(last_key):
                        self.block_x = self.block_x - 1
                elif key == Direction.Down:
                    last_key = Direction.Down
                else:
                    last_key = Direction.Nil
                    
                if last_key == Direction.Down:
                    del_time = 250
                else:
                    del_time = 500
                self.update()
                light.show(self.get_img())
            if current_time - time_stamp > del_time:
                time_stamp = current_time
                self.move_down()
                self.update()
                light.show(self.get_img())
