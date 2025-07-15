import pygame as py
import os
import threading
import math

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
        self.tool_index = 0

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
            if rect.collidepoint(mouse_pos):
                if self.tool_index != None and self.tool_index != i:
                    self.swap(self.tool_index)
                    tool_selected[self.tool_index] = False
                self.swap(i)
                tool_selected[i] = not tool_selected[i]
                self.tool_index = i


class Canvas:
    def __init__(self, width, height):
        self.surface = py.Surface((width, height))
        self.surface.fill((255, 255, 255))
        self.brush_color = (0, 0, 0)

    def draw_brush(self, x, y, size=5):
        py.draw.circle(self.surface, self.brush_color, (x, y), size)  # Draw a brush stroke

    def draw_square(self, points):
        x1,y1 = points[0]
        x2,y2 = points[1]

        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)
        
        for x in range(min_x, max_x, 1):
            self.draw_brush(x, y1)
            self.draw_brush(x, y2)

        for y in range(min_y, max_y, 1):
            self.draw_brush(x1, y)
            self.draw_brush(x2, y)

        
    def draw_circle(self, points):
        x1,y1 = points[0]
        x2,y2 = points[1]

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)

        mid_x = abs(x2 - x1) // 2 + min(x1, x2)
        mid_y = abs(y2 - y1) // 2 + min(y1, y2)
        
        smajor = max(abs(x2 - x1), abs(y2 - y1)) //2
        sminor = min(abs(x2 - x1), abs(y2 - y1)) //2

        if min(dx, dy) == dy:
            for t in range(0, int(2*math.pi * 100),1):
                self.draw_brush(mid_x + smajor * math.cos(t), mid_y + sminor * math.sin(t))
        else:
            for t in range(0, int(2*math.pi * 100),1):
                self.draw_brush(mid_x + sminor * math.cos(t), mid_y + smajor * math.sin(t))

    def draw_line(self, points):
        # Bresenham's Line Algorithm
        x1, y1 = points[0]
        x2, y2 = points[1]

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.draw_brush(x1, y1)
            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

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
point_buffer = []

while running:
    screen.fill((0,0,0))
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        elif event.type == py.MOUSEBUTTONDOWN:
            mouse_pos = py.mouse.get_pos()
            pressed = True
            toolbar.update(mouse_pos)
            if 0 <= mouse_pos[0] < 1000 and 0 <= mouse_pos[1] < 1000 and (tool_selected[1] or tool_selected[2] or tool_selected[3]):
                point_buffer.append(mouse_pos)
            elif 1000 <= mouse_pos[0] < 1050 and 0 <= mouse_pos[1] < 1000:
                if tool_selected[4]:
                    display.canvas.brush_color = (0,0,0)
                elif tool_selected[5]:
                    display.canvas.brush_color = (0,0,255)
                elif tool_selected[6]:
                    display.canvas.brush_color = (0,255,0)
                elif tool_selected[7]:
                    display.canvas.brush_color = (255,0,0)
                    
        elif event.type == py.MOUSEBUTTONUP:
            pressed = False
            mouse_pos = py.mouse.get_pos()
            if 0 <= mouse_pos[0] < 1000 and 0 <= mouse_pos[1] < 1000:
                point_buffer.append(mouse_pos)
                if tool_selected[1]:
                    display.canvas.draw_circle(point_buffer)
                elif tool_selected[2]:
                    display.canvas.draw_line(point_buffer)
                elif tool_selected[3]:
                    display.canvas.draw_square(point_buffer)
                point_buffer = []
            else:
                point_buffer = []

    if pressed:
        mouse_pos = py.mouse.get_pos()
        display.update(mouse_pos)

    display.draw()
    toolbar.draw()

    clock.tick(500)
    py.display.flip()

py.quit()