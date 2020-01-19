import pygame
import os
import random
import math
pygame.init()

class GraphicElement:
    IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), "imgs")
    x = None
    y = None
    image = None

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
    
    def move_by_offset(self, xoffset, yoffset):
        self.x += xoffset
        self.y += yoffset

class Window(GraphicElement):

    def __init__(self, width = 600, height = 800, caption = "Flappy Bird"):
        self.win = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)

        self.width = width
        self.height = height
        self.caption = caption
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(self.IMAGE_FOLDER, "bg.png")).convert_alpha(), (600, 900))
        self.image_coordinates = []
        for i in range(1 + math.floor(width / 600)):
            self.image_coordinates.append((0 + 600 * i, 0))
        self.clock = pygame.time.Clock()
        self.graphic_elements = []
    
    def draw(self):
        
        for coordinate in self.image_coordinates:
            self.win.blit(self.image, coordinate)
        for graphic_element in self.graphic_elements:
            for instance in graphic_element:
                instance.draw(self.win)

    def fill(self, color):
        self.win.fill(color)

    def update(self):
        pygame.display.update()

class Base(GraphicElement):
    IMAGE = pygame.image.load(os.path.join(GraphicElement.IMAGE_FOLDER, "base.png"))

    def __init__(self, x, y):
        self.image = pygame.transform.scale2x(self.IMAGE.convert_alpha())
        self.x = x
        self.y = y

class BaseOverlay():
    def __init__(self, width, y = 730):
        self.y = y
        self.width = width
        self.count = 2 + math.floor(width / Base.IMAGE.get_width())
        self.bases = []
        for i in range(self.count):
            self.bases.append(Base((Base.IMAGE.get_width() * i), y))
    
    def draw(self, win):
        for base in self.bases:
            base.draw(win)

    def move_by_offset(self, xoffset, yoffset):
        for base in self.bases:
            base.move_by_offset(xoffset, yoffset)
        if self.bases[0].x < 0 - Base.IMAGE.get_width():
            self.bases.pop(0)
            self.bases.append(Base((Base.IMAGE.get_width() * (self.count - 1)), self.y))

class Pipe(GraphicElement):
    PIPE_TOP = "pipe_top"
    PIPE_BOTTOM = "pipe_bottom"

    IMAGE_PIPE = pygame.image.load(os.path.join(GraphicElement.IMAGE_FOLDER, "pipe.png"))

    def __init__(self, pipeType, y, x):
        if pipeType == self.PIPE_TOP:
            self.image = pygame.transform.flip(pygame.transform.scale2x(self.IMAGE_PIPE.convert_alpha()), 0, 1)
        elif pipeType == self.PIPE_BOTTOM:
            self.image = pygame.transform.scale2x(self.IMAGE_PIPE.convert_alpha())
        else:
            raise ValueError()
        self.x = x
        self.y = y
    
class PipePair:
    def __init__(self, height = 0, gap = 200, screen_width = 600):
        if height == 0:
            self.height = random.randrange(50, 450)
        else:
            self.height = height
        self.gap = gap
        self.screen_width = screen_width
        self.pipe_top = Pipe(Pipe.PIPE_TOP, self.height - Pipe.IMAGE_PIPE.get_height()*2, self.screen_width)
        self.pipe_bottom = Pipe(Pipe.PIPE_BOTTOM, self.height + self.gap, self.screen_width)
    
    def draw(self, win):
        self.pipe_top.draw(win)
        self.pipe_bottom.draw(win)

    def move_by_offset(self, xoffset, yoffset):
        self.pipe_top.move_by_offset(xoffset, yoffset)
        self.pipe_bottom.move_by_offset(xoffset, yoffset)

    def get_x(self):
        return self.pipe_top.x

    def get_width(self):
        return self.pipe_top.image.get_width()

class Bird(GraphicElement):
    IMAGES = [pygame.transform.scale2x(pygame.image.load(os.path.join(GraphicElement.IMAGE_FOLDER, "bird1.png"))),
        pygame.transform.scale2x(pygame.image.load(os.path.join(GraphicElement.IMAGE_FOLDER, "bird2.png"))),
        pygame.transform.scale2x(pygame.image.load(os.path.join(GraphicElement.IMAGE_FOLDER, "bird3.png")))]

    def __init__(self, startx = 230, starty = 350):
        self.x = startx
        self.y = starty
        self.image_index = 0
        self.index_changer = None
        self.image = self.IMAGES[self.image_index]

    def move_wings(self):
        if self.image_index == 0:
            self.index_changer = 1
        if self.image_index == len(self.IMAGES) - 1:
            self.index_changer = -1
        self.image_index += self.index_changer
        self.image = self.IMAGES[self.image_index]
    
    def move_by_offset(self, xoffset, yoffset):
        self.move_wings()
        self.x += xoffset
        self.y += yoffset

