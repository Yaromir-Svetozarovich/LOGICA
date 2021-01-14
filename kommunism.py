import pygame
from random import randint
import numpy as np


RES = 1600, 900
FPS = 20
TILE = 12
HEIGHT = 900
WIDTH = 1600
screen = pygame.display.set_mode(RES)
"""
class Conveyor:
    def __init__(self):
        self.cell_size = TILE

    def create(self):
        for y in range(HEIGHT):
                        for x in range(WIDTH):
                            pygame.draw.rect(screen, pygame.Color('red'),
                                (x * self.cell_size, y * self.cell_size,
                                self.cell_size, self.cell_size),0)

    def destroy(self):
        pass

"""       


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
        #Отрисовка границ тайлов
        for y in range(self.HEIGHT):
                for x in range(self.WIDTH):
                    if self.board[y][x] == 1:
                        pygame.draw.rect(screen, pygame.Color('yellow'),
                        (x * self.cell_size, y * self.cell_size, 
                        self.cell_size, self.cell_size), 0)
                    elif self.board[y][x] == 2:
                        pygame.draw.rect(screen, pygame.Color('green'),
                        (x * self.cell_size, y * self.cell_size, 
                        self.cell_size, self.cell_size), 0)
                    elif self.board[y][x] == 3:
                        pygame.draw.rect(screen, pygame.Color('red'),
                        (x * self.cell_size, y * self.cell_size, 
                        self.cell_size, self.cell_size), 0)
                #Отрисовка сетки
                    pygame.draw.rect(screen, pygame.Color('#282828'),
                        (x * self.cell_size, y * self.cell_size,
                        self.cell_size, self.cell_size),1)
    def update(self):
        for y in range(self.HEIGHT):
                for x in range(self.WIDTH):
                    if (self.board[y][x]  == 3 and  self.board[y-1][x] == 3 and self.board[y+1][x])== 3:
                           self.board[y][x] = 2
                           self.render()
                    if self.board[y][x]  == 2 :
                            self.board[y-1][x-1] == 3
                            self.board[y+1][x-1] == 3
                            self.board[y-1][x+1] == 3
                            self.board[y+1][x-1] == 3
                            self.render()


                        

#Получаем координаты мыши 

    def get_click(self, mouse_pos):
        cell_x = mouse_pos[0] // self.cell_size
        cell_y = mouse_pos[1] // self.cell_size

        if not(cell_x < 0 or cell_x >= self.WIDTH or cell_y < 0 or cell_y >= self.HEIGHT):
            self.board[cell_y][cell_x] = (self.board[cell_y][cell_x] + 1) % 4


world = Board(128, 64)










# EventLoop - бесконечный (почти ) игровой цикл
running = True
while running:
    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            world.get_click(event.pos)

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.K_ESCAPE:
            running = False
        
    screen.fill((10,10,10))
    world.render()
    world.update()
    pygame.display.flip()
    
pygame.quit()
