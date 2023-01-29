import sys
import pygame
import random
from pygame.math import Vector2

class hero:
	def __init__(self):
		self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
		self.direction = Vector2(0, 0)
		self.new_block = False


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

	def move_snake(self):
		if self.new_block:
			body_copy = self.body[:]
			body_copy.insert(0,body_copy[0] + self.direction)
			self.body = body_copy[:]
			self.new_block = False
		else:
			body_copy = self.body[:-1]
			body_copy.insert(0,body_copy[0] + self.direction)
			self.body = body_copy[:]

	def add_block(self):
		self.new_block = True

	def goldearn(self):
		random.choice([goldearnsound1, goldearnsound2, goldearnsound3]).play()

	def reset(self):
		self.body = [Vector2(5, 10),Vector2(4, 10),Vector2(3, 10)]
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
		self.snake.move_snake()
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
		


pygame.init()
cell_size = 32
cell_number = 26
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
gold = pygame.image.load('textures/gold.png').convert_alpha()
head_up = pygame.image.load('textures/head_up.png').convert_alpha()
head_down = pygame.image.load('textures/head_down.png').convert_alpha()
head_right = pygame.image.load('textures/head_right.png').convert_alpha()
head_left = pygame.image.load('textures/head_left.png').convert_alpha()
tail = pygame.image.load('textures/tail.png').convert_alpha()
bodyy = pygame.image.load('textures/bodyy.png').convert_alpha()
bodyx = pygame.image.load('textures/bodyx.png').convert_alpha()
body1 = pygame.image.load('textures/body1.png').convert_alpha()
body2 = pygame.image.load('textures/body2.png').convert_alpha()
body3 = pygame.image.load('textures/body3.png').convert_alpha()
body4 = pygame.image.load('textures/body4.png').convert_alpha()
goldearnsound1 = pygame.mixer.Sound('sounds/goldearn1.wav')
goldearnsound2 = pygame.mixer.Sound('sounds/goldearn2.wav')
goldearnsound3 = pygame.mixer.Sound('sounds/goldearn3.wav')
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100)
main_game = game()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
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

	screen.fill((0, 0, 0))
	main_game.drawel()
	pygame.display.update()
