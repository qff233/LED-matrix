from random import randint
from time import sleep, ticks_ms
from front3x5 import add_front

class Direction:  # 触摸按键的数字的映射
    Left = 5
    Right = 9
    Up = 6
    Down = 7

class Snake:
    def __init__(self):
        self.snake = [(5,3), (5,4), (5,5)]
        self.update_apple_pos()
        self.time_stemp = ticks_ms()
        self.del_time_ms = 1200 # 1.2秒走一次，随着吃的苹果越来越多，时间越来越短
        self.score = 0
        self.game_over = False
        
    def update_apple_pos(self):
        while True:
            self.apple_pos = (randint(0,11), randint(0,9))
            for pos in self.snake:
                if pos == self.apple_pos:
                    continue
            break
            
    def move(self, direction):
        def update(new_x, new_y):
            if new_x < 0 or new_x >= 12 or new_y < 0 or new_y >= 10: # 撞墙
                self.game_over = True
                return
            for body in self.snake:
                if body == (new_x, new_y):
                    self.game_over = True
                    return
                
            self.snake.insert(0, (new_x, new_y))
            if (new_x, new_y) != self.apple_pos:  # 没有吃到苹果
                self.snake.pop()
            else: #吃到了苹果
                self.score = self.score + 20
                self.update_apple_pos()
                self.del_time_ms = self.del_time_ms - 100
                
        x, y = self.snake[0] # 取出头的坐标
        if direction == Direction.Left:
            update(x-1, y)
        elif direction == Direction.Right:
            update(x+1, y)
        elif direction == Direction.Up:
            update(x, y-1)
        elif direction == Direction.Down:
            update(x, y+1)
        else:
            assert(False)
        
    def get_img(self):
        img = [[(0,0,0) for col in range(12)] for row in range(10)]
        if self.game_over:
            print("游戏结束！", self.score)
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
        
        else:
            for snake in self.snake:
                x, y = snake
                img[y][x] = (255, 0, 0)
            head_x, head_y = self.snake[0]
            img[head_y][head_x] = (0,0,255)
            
            x, y = self.apple_pos
            img[y][x] = (0, 255, 0)
            return img
        
    def main_loop(self, light, touch):  
        self.current_direction = Direction.Up
        keys = [Direction.Left, Direction.Right, Direction.Up, Direction.Down]  # 要是同时有两个方向键按下？ 目前是按此列表的优先级
        def key_update():
            x, y = self.snake[0]
            if touch.is_touch(Direction.Left):
                if (x-1, y) != self.snake[1]:
                    self.current_direction = Direction.Left
                    return
            if touch.is_touch(Direction.Right):
                if (x+1, y) != self.snake[1]:
                    self.current_direction = Direction.Right
                    return
            if touch.is_touch(Direction.Up):
                if (x, y-1) != self.snake[1]:
                    self.current_direction = Direction.Up
                    return
            if touch.is_touch(Direction.Down):
                if (x, y+1) != self.snake[1]:
                    self.current_direction = Direction.Down
                    return

        while True:
            if self.game_over:
                while True:
                    if touch.is_touch(10):
                        break
                    sleep(1.0)
                break
            light.show(self.get_img())
            key_update()
            current_time = ticks_ms()
            if current_time - self.time_stemp > self.del_time_ms:
                self.score = self.score + 1
                self.move(self.current_direction)
                light.show(self.get_img())
                self.time_stemp = current_time

