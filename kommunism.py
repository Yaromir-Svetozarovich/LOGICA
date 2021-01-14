import pygame
from random import randint
import numpy as np


RES = 1440, 900
FPS = 20
TILE = 32

screen = pygame.display.set_mode(RES)

#Класс Board  - основа тайлового мира
class Board:
    def __init__(self, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.board = []
        for y in range(self.HEIGHT):
            line = []
            for x in range(self.WIDTH):
                line.append(0)
            self.board.append(line)
        self.cell_size = TILE
# Отрисовка мира
    def render(self):
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                pygame.draw.rect(screen, pygame.Color('dimgray'),
                    (x * self.cell_size, y* self.cell_size, self.cell_size, self.cell_size),1)

#Получаем координаты мыши 
    def get_click(self, mouse_pos):
        cell_x = mouse_pos[0] // self.cell_size
        cell_y = mouse_pos[1] // self.cell_size

        if not(cell_x < 0 or cell_x >= self.WIDTH or cell_y < 0 or cell_y >= self.HEIGHT):
            self.board[cell_y][cell_x] = (self.board[cell_y][cell_x] + 1) %3

world = Board(32, 16)










# EventLoop - бесконечный (почти ) игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            world.get_click(event.pos)
        if event.type == pygame.QUIT:
            running = False
    screen.fill((10,10,10))
    world.render()
    pygame.display.flip()
    
pygame.quit()
