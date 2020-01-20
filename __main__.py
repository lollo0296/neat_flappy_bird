from models import Window, PipePair, BaseOverlay, Bird
from time import sleep
import pygame



w = Window()

pipe_pairs = [ PipePair() ]
w.graphic_elements.append(pipe_pairs)
base_overlay = BaseOverlay()
w.graphic_elements.append( [ base_overlay ] )
bird = Bird()
w.graphic_elements.append( [ bird ] )


run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()
    w.clock.tick(30)
    w.draw()
    w.update()

    elems_to_remove = []
    for pipe_pair in pipe_pairs:
        if pipe_pair.get_x() < 0 - pipe_pair.get_width():
            elems_to_remove.append(pipe_pair)
        if pipe_pair.get_x() == w.width - 400:
            pipe_pairs.append(PipePair())    
        pipe_pair.move_by_offset(-5, 0)
    
    for elem_to_remove in elems_to_remove:
        pipe_pairs.remove(elem_to_remove)

    base_overlay.move_by_offset(-5, 0)
    bird.fly()