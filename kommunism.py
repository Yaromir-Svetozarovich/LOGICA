import pygame as pg
from random import randint
import numpy as np

RES = 1440, 900
FPS = 60
TILE = 16
HEIGHT = 900
WIDTH =  1440
pg.display.set_caption('ЛОГИКА')
gameicon = pg.image.load('logo.png')
pg.display.set_icon(gameicon)
main_screen = pg.display.set_mode(RES)

class Documentation:
    def __init__(self):
        self.screen = pg.display.set_mode(RES)
        self.screen.fill((0,0,0))
        self.sprite_doc = pg.image.load('doc.png')
        self.sprite_call_doc = pg.image.load('doc_call.png')
        self.sprite_destroyer = pg.image.load('destroy.png')
        
    def render_documentation(self):
        self.screen.blit(self.sprite_doc, (0,0))
    def buttom_render(self):
        self.screen.blit(self.sprite_call_doc, (1408, 868))
    def destroy_documentation(self):
        self.screen.blit(self.sprite_destroyer, (0,0))
    def program_mode(self):
        pg.font.init()
        self.font = pg.font.Font(None, 36)
        self.text = self.font.render(('Режим: '+ mode_text[mode]), 0, (255, 255, 255))
        self.textpos = self.text.get_rect()
        self.textpos.bottomleft = self.screen.get_rect().bottomleft
        self.screen.blit(self.text, self.textpos)

            


#Класс Board  - основа тайлового мира
class Board:
    def __init__(self, WIDTH, HEIGHT):
        self.screen = pg.display.set_mode(RES)
        self.screen.fill((10,10,10))
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.board = []
        self.signal_sprite = pg.image.load('signal.png')
        self.y = 0
        self.x = 0
        self.board = np.zeros((self.HEIGHT, self.WIDTH))
        self.cell_size = TILE
# Отрисовка мира
    def render(self):
        #Отрисовка границ тайлов
        for y in range(self.HEIGHT):
                for x in range(self.WIDTH):
                    #Отрисовка элементов
                    color={1: 'yellow', 3 : 'green',10: 'blue',20 : 'orange'}
                    if self.board[y][x] in color:                       
                        pg.draw.rect(self.screen, pg.Color(color[self.board[y][x]]),
                            (x * self.cell_size, y * self.cell_size, 
                            self.cell_size, self.cell_size), 0)     
                    #Отрисовка сетки
                    pg.draw.rect(self.screen, pg.Color('#212121'),
                        (x * self.cell_size, y * self.cell_size,
                        self.cell_size, self.cell_size),1)

    def update(self):
        for y in range(self.HEIGHT):
                for x in range(self.WIDTH):
                    #Генерирование сигналов
                    if self.board[y][x] == 100 and self.board[y-1][x] == 1:
                            self.board[y-1][x] = 3
                    if self.board[y][x]  == 3 and (self.board[y][x-1] == 1 or 
                        self.board[y][x+1] == 1 or self.board[y-1][x]== 1 
                        or self.board[y+1][x] ==1):
                           self.board[y][x] = 3
                    #Передача сигнала по проводам                     
                    if self.board[y][x]  == 3 : 
                        if self.board[y][x-1] == 1:
                            self.board[y][x-1] = 3
                        elif self.board[y][x+1] == 1:
                            self.board[y][x+1] = 3
                        elif self.board[y-1][x] == 1:
                            self.board[y-1][x] = 3
                        elif self.board[y+1][x] == 1:
                            self.board[y+1][x] = 3
#Логические элементы
#Вся логика работы логических элементов примитивна
                    #Логическое "И"
                    if self.board[y][x] == 10 and self.board[y][x-1] == 3 and self.board[y][x+1] == 3:
                        self.board[y-1][x] = 3
                    #Логическое "ИЛИ"
                    if self.board[y][x] == 20 and (self.board[y][x-1] == 3 or self.board[y][x+1] == 3 or self.board[y+1][x] == 3):
                        self.board[y-1][x] = 3
    def clear(self):
        self.screen.fill((10,10,10))
        self.board = np.zeros((self.HEIGHT, self.WIDTH))

#Получаем координаты мыши 

    def get_cellPos(self, mouse_pos):
        cell_x = mouse_pos[0] // self.cell_size
        cell_y = mouse_pos[1] // self.cell_size
        return [cell_x,cell_y]

    def get_click(self, cell_pos):
        cell_x=cell_pos[0]
        cell_y=cell_pos[1]
        if not(cell_x < 0 or cell_x >= self.WIDTH or cell_y < 0 or cell_y >= self.HEIGHT):
            self.board[cell_y][cell_x] = (self.board[cell_y][cell_x] + 1) % 4
    def get_logic(self, cell_pos):
        cell_x=cell_pos[0]
        cell_y=cell_pos[1]
        if not(cell_x < 0 or cell_x >= self.WIDTH or cell_y < 0 or cell_y >= self.HEIGHT):
            self.board[cell_y][cell_x] = (self.board[cell_y][cell_x] + 10)
        #Циклическое создание лог. элементов
            if self.board[cell_y][cell_x] == 40:
                self.board[cell_y][cell_x] = 0
    
    def save_to_file(self):
        np.save('board.npy',self.board)

    def load_from_file(self):
        self.board = np.load('board.npy')

mode_text = {0 : 'Меню', 1:'Рисование', 2:'Симуляция',3:'Сохранение схемы ...'}
mode = 0
def main():    
    world = Board(88, 54)
    Doc = Documentation()
    mode_text = {0 : 'Меню', 1:'Рисование', 2:'Симуляция',3:'Сохранение схемы ...'}
    mode = 0
    # EventLoop - бесконечный (почти ) игровой цикл
    running = True
    mDown = False 
    lastPos=[-1,-1]
    while running:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and mode == 1:
                lastPos = world.get_cellPos(event.pos)
                world.get_click(lastPos)
                mDown=True;
            if event.type == pg.MOUSEBUTTONUP and event.button == 1 and mode == 1:
                mDown=False;
            if mDown and mode == 1:
                if (world.get_cellPos(event.pos)!=lastPos):
                    lastPos=world.get_cellPos(event.pos)
                    world.get_click(lastPos) 
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 3 and mode == 1:
                lastPos = world.get_cellPos(event.pos)
                world.get_logic(lastPos)

                #Проверка на совпадение координат мыши с координатами кнопки    
            mouse_position = pg.mouse.get_pos()
            doc_view = False
            if (mouse_position >=(1408,868) and mouse_position <=(1440, 900)) and (event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                if doc_view:
                    Doc.destroy_documentation()
                else:
                    Doc.render_documentation()
                doc_view = not(doc_view)  

            if event.type == pg.KEYDOWN:
                    #print(event.key)
                if event.key == pg.QUIT:
                    running = False
                elif event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_SPACE:
                    mode+=1
                elif event.key ==  pg.K_s:
                    world.save_to_file()
                    mode = 3
                elif event.key ==  pg.K_v:
                    world.load_from_file()
                    world.render()


    #Изменение состояние симулятора ( 1 = режим рисования, 2 = режим симуляции, 0 = пустой режим) 
        if mode == 0:
            Doc.program_mode()
        if mode == 1:
            Doc.destroy_documentation()
            Doc.program_mode() 
            world.render()
        if mode == 2:
            Doc.destroy_documentation()
            world.update()
            Doc.program_mode()
            world.render()
        if mode == 3:
            Doc.destroy_documentation()
            Doc.program_mode()
            world.render()
        if mode == 4:
            mode = 0
            world.clear()
            
        Doc.buttom_render()
        pg.display.flip()
        

        pg.time.delay(FPS)    
        pg.quit()
    return mode_text
if __name__ == '__main__': 
    main()