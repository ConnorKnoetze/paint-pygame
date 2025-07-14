import pygame as py
import os
import threading

py.init()
screen = py.display.set_mode((1050,1000))
py.display.set_caption("Paint")
clock = py.time.Clock()
base_dir = os.path.abspath(os.path.dirname(__file__))
assets_dir_off = os.path.join(base_dir, "assets", "off")
assets_dir_on = os.path.join(base_dir, "assets", "on")
assets_on = [os.path.join(assets_dir_on, file) for file in os.listdir(assets_dir_on)]
assets_off = [os.path.join(assets_dir_off, file) for file in os.listdir(assets_dir_off)]

class Toolbar():
    def __init__(self):
        self.swapped = False
        self.rect = py.Rect(1000, 0, 50, 1000)

        gap = 41
        size = 32
        start = 1009

        self.assets_rects = [py.Rect(start, y, size, size) for y in range(9, len(assets_off)*gap, gap)] 
        self.images = [py.transform.scale(py.image.load(filepath).convert_alpha(), (size, size)) for filepath in assets_off]
        self.swap(0)
    
    def draw(self):
        py.draw.rect(screen, (50,50,50), self.rect)
        [screen.blit(self.images[i], self.assets_rects[i]) for i in range(len(self.assets_rects))]

    def get_rect(self):
        return self.rect

    def get_rects(self):
        return self.assets_rects

    def swap(self, index):
        if self.swapped:
            path = os.path.join(base_dir, assets_off[index])
        else:
            path = os.path.join(base_dir, assets_on[index])
        
        self.images[index] = py.transform.scale(py.image.load(path).convert_alpha(), (32,32))
        self.swapped = not self.swapped
    
    def update(self, mouse_pos):
        rects = self.get_rects()
        for i in range(len(rects)):
            rect = rects[i]
            if rect.collidepoint(mouse_pos) and not True in tool_selected:
                self.swap(i)
                tool_selected[i] = True
            elif rect.collidepoint(mouse_pos) and tool_selected[i]:
                self.swap(i)
                tool_selected[i] = False


class Canvas:
    def __init__(self, width, height):
        self.surface = py.Surface((width, height))
        self.surface.fill((255, 255, 255))
        self.brush_color = (0, 0, 0)

    def draw_brush(self, x, y, size=5):
        py.draw.circle(self.surface, self.brush_color, (x, y), size)  # Draw a brush stroke


    def render(self, screen):
        screen.blit(self.surface, (0, 0))  # Blit the canvas onto the main screen


class Display():
    def __init__(self):
        self.canvas = Canvas(1000, 1000)
        self.size = 1000

    def draw(self):
        self.canvas.render(screen)

    def update(self, mouse_pos):
        if tool_selected[0] and 0<= mouse_pos[0] < self.size and 0<= mouse_pos[1] < self.size:
            self.canvas.draw_brush(mouse_pos[0], mouse_pos[1], size=5)

display = Display()
toolbar = Toolbar()
tool_selected = [True]+[False for _ in assets_on][:-1]
running = True
pressed = False

while running:
    screen.fill((0,0,0))
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        elif event.type == py.MOUSEBUTTONDOWN:
            mouse_pos = py.mouse.get_pos()
            pressed = True
            toolbar.update(mouse_pos)
        elif event.type == py.MOUSEBUTTONUP:
            pressed = False
    if pressed:
        mouse_pos = py.mouse.get_pos()
        display.update(mouse_pos)

    display.draw()
    toolbar.draw()

    clock.tick(500)
    py.display.flip()