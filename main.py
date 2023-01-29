import sys
import time
import pygame
import random
from pygame.math import Vector2

pygame.display.set_caption("Alchemiest snake")
pygame.init()
cell_size = 32
cell_number = 25
WIDTH = cell_number * cell_size
HEIGHT = cell_number * cell_size
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class hero:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False
        self.score = 0

    def draw_snake(self):
        for index, block in enumerate(self.body):
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            if index == 0:
                head_relation = self.body[1] - self.body[0]
                if head_relation == Vector2(1, 0):
                    self.head = head_left
                elif head_relation == Vector2(-1, 0):
                    self.head = head_right
                elif head_relation == Vector2(0, 1):
                    self.head = head_up
                elif head_relation == Vector2(0, -1):
                    self.head = head_down
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(bodyy, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(bodyx, block_rect)
                else:
                    if previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(body3, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(body1, block_rect)
                    elif previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(body4, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(body2, block_rect)

    def movesnake(self):
        if self.new_block:
            bodyadd = self.body[:]
            bodyadd.insert(0, bodyadd[0] + self.direction)
            self.body = bodyadd[:]
            self.new_block = False
        else:
            bodyadd = self.body[:-1]
            bodyadd.insert(0, bodyadd[0] + self.direction)
            self.body = bodyadd[:]

    def add_block(self):
        self.new_block = True

    def goldearn(self):
        random.choice([goldearnsound1, goldearnsound2, goldearnsound3]).play()
        self.score += 1
        print(self.score)

    def score(self):
        return self.score

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class golds:
    def __init__(self):
        self.randspawn()

    def drawgold(self):
        goldr = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        screen.blit(gold, goldr)

    def randspawn(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class game:
    def __init__(self):
        self.snake = hero()
        self.gold = golds()

    def update(self):
        self.snake.movesnake()
        self.checkcol()
        self.gameover()

    def drawel(self):
        self.gold.drawgold()
        self.snake.draw_snake()

    def checkcol(self):
        if self.gold.pos == self.snake.body[0]:
            self.snake.goldearn()
            self.snake.add_block()
            self.gold.randspawn()
        for block in self.snake.body[1:]:
            if block == self.gold.pos:
                self.gold.randspawn()

    def gameover(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.snake.reset()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.snake.reset()


def terminate():
    pygame.quit()
    sys.exit()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()


def texload(a):
    return pygame.image.load('textures/' + str(a) + '.png').convert_alpha()


clock = pygame.time.Clock()
gold = texload('gold')
head_up = texload('head_up')
head_down = texload('head_down')
head_right = texload('head_right')
head_left = texload('head_left')
tail = texload('tail')
bodyy = texload('bodyy')
bodyx = texload('bodyx')
body1 = texload('body1')
body2 = texload('body2')
body3 = texload('body3')
body4 = texload('body4')
goldearnsound1 = pygame.mixer.Sound('sounds/goldearn1.wav')
goldearnsound2 = pygame.mixer.Sound('sounds/goldearn2.wav')
goldearnsound3 = pygame.mixer.Sound('sounds/goldearn3.wav')
SCREEN_UPDATE = pygame.USEREVENT
screen.blit(pygame.image.load('fon.png'), (0, 0))
pygame.time.set_timer(SCREEN_UPDATE, 100)
main_game = game()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            st = hero()
            print('СТАТИСТИКА ЗА ИГРУ:')
            print("ВЫ НАБРАЛИ", st.score, "ЗОЛОТА!")
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
    screen.blit(pygame.image.load('fon.png'), (0, 0))
    main_game.drawel()
    pygame.display.update()
