import pygame as py
import os, sys
import math
import Client
import threading

py.init()
screen = py.display.set_mode((1050,1000))
py.display.set_caption("Paint Pygame")
clock = py.time.Clock()
base_dir = os.path.abspath(os.path.dirname(__file__))

tool_assets_dir_off = os.path.join(base_dir, "assets", "tools","off")
tool_assets_dir_on = os.path.join(base_dir, "assets", "tools", "on")
tool_assets_off = [os.path.join(tool_assets_dir_off, file) for file in os.listdir(tool_assets_dir_off)]
tool_assets_on = [os.path.join(tool_assets_dir_on, file) for file in os.listdir(tool_assets_dir_on)]
tool_selected = [True]+[False for _ in tool_assets_on][:-1]

color_assets_dir_off = os.path.join(base_dir, "assets", "colors","off")
color_assets_dir_on = os.path.join(base_dir, "assets", "colors", "on")
color_assets_off = [os.path.join(color_assets_dir_off, file) for file in os.listdir(color_assets_dir_off)]
color_assets_on = [os.path.join(color_assets_dir_on, file) for file in os.listdir(color_assets_dir_on)]

size_assets_dir_off = os.path.join(base_dir, "assets", "size","off")
size_assets_dir_on = os.path.join(base_dir, "assets", "size", "on")
size_assets_off = [os.path.join(size_assets_dir_off, file) for file in os.listdir(size_assets_dir_off)]
size_assets_on = [os.path.join(size_assets_dir_on, file) for file in os.listdir(size_assets_dir_on)]


class Toolbar():
    def __init__(self):
        self.swapped = False
        self.rect = py.Rect(1000, 0, 50, 41 * len(tool_assets_off))
        self.tool_index = 0

        gap = 41
        size = 32
        start = 1009
        self.end = len(tool_assets_off)*gap

        self.assets_rects = [py.Rect(start, y, size, size) for y in range(9, self.end, gap)] 
        self.images = [py.transform.scale(py.image.load(filepath).convert_alpha(), (size, size)) for filepath in tool_assets_off]
        self.swap(0)
    
    def draw(self):
        py.draw.rect(screen, (100,100,100), self.rect)
        [screen.blit(self.images[i], self.assets_rects[i]) for i in range(len(self.assets_rects))]

    def get_end(self):
        return self.end

    def get_rect(self):
        return self.rect

    def get_rects(self):
        return self.assets_rects

    def swap(self, index):
        if self.swapped:
            path = os.path.join(base_dir, tool_assets_off[index])
        else:
            path = os.path.join(base_dir, tool_assets_on[index])
        
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
                    self.tool_index = None

                    self.swap(i)
                    self.tool_index = i
                    tool_selected[i] = True


class Colors():
    def __init__(self):
        black = (0, 0, 0)
        blue = (0, 0, 255)
        green = (0, 255, 0)
        red = (255, 0, 0)

        self.colors = [black, blue, green, red]

        gap = 41
        size = 32
        xstart = 1009
        ystart = 41*len(color_assets_off)
        image_start = ystart + 9
        self.end = image_start+ len(color_assets_off)*gap

        self.swapped = False
        self.rect = py.Rect(1000, ystart, 50, 41 * len(color_assets_off))
        self.color_index = 0

        self.assets_rects = [py.Rect(xstart, y, size, size) for y in range(image_start, self.end, gap)] 
        self.images = [py.transform.scale(py.image.load(filepath).convert_alpha(), (size, size)) for filepath in color_assets_off]
        self.swap(0)

    def get_end(self):
        return self.end
    
    def get_color(self):
        return self.colors[self.color_index]

    def draw(self):
        py.draw.rect(screen, (100,100,100), self.rect)
        [screen.blit(self.images[i], self.assets_rects[i]) for i in range(len(self.assets_rects))]

    def get_rects(self):
        return self.assets_rects

    def swap(self, index):
        if self.swapped:
            path = os.path.join(base_dir, color_assets_off[index])
        else:
            path = os.path.join(base_dir, color_assets_on[index])
        
        self.images[index] = py.transform.scale(py.image.load(path).convert_alpha(), (32,32))
        self.swapped = not self.swapped

    def update(self, mouse_pos):
        rects = self.get_rects()
        for i in range(len(rects)):
            rect = rects[i]
            if rect.collidepoint(mouse_pos):
                if self.color_index != None and self.color_index != i:
                    self.swap(self.color_index)
                    self.color_index = None

                    self.swap(i)
                    self.color_index = i

class Sizes():
    def __init__(self):
        five = 5
        seven = 7
        ten = 10
        twelve = 12

        self.sizes = [five, seven, ten, twelve]

        gap = 41
        size = 32
        xstart = 1009
        ystart = 41*len(color_assets_off) * 2
        image_start = ystart + 9
        self.end = image_start+ len(size_assets_off)*gap

        self.swapped = False
        self.rect = py.Rect(1000, ystart, 50, 41 * len(color_assets_off))
        self.size_index = 0

        self.assets_rects = [py.Rect(xstart, y, size, size) for y in range(image_start, self.end, gap)] 
        self.images = [py.transform.scale(py.image.load(filepath).convert_alpha(), (size, size)) for filepath in size_assets_off]
        self.swap(0)

    def get_end(self):
        return self.end
    
    def get_size(self):
        return self.sizes[self.size_index]

    def draw(self):
        py.draw.rect(screen, (100,100,100), self.rect)
        [screen.blit(self.images[i], self.assets_rects[i]) for i in range(len(self.assets_rects))]

    def get_rects(self):
        return self.assets_rects

    def swap(self, index):
        if self.swapped:
            path = os.path.join(base_dir, size_assets_off[index])
        else:
            path = os.path.join(base_dir, size_assets_on[index])
        
        self.images[index] = py.transform.scale(py.image.load(path).convert_alpha(), (32,32))
        self.swapped = not self.swapped

    def update(self, mouse_pos):
        rects = self.get_rects()
        for i in range(len(rects)):
            rect = rects[i]
            if rect.collidepoint(mouse_pos):
                if self.size_index != None and self.size_index != i:
                    self.swap(self.size_index)
                    self.size_index = None

                    self.swap(i)
                    self.size_index = i


class Canvas:
    def __init__(self, width, height):
        self.surface = py.Surface((width, height))
        self.surface.fill((255, 255, 255))
        self.brush_color = (0, 0, 0)
        self.size = 5

    def draw_message(self, color, x, y, size=5):
        py.draw.circle(self.surface, color, (x, y), size)

    def draw_brush(self, x, y):
        py.draw.circle(self.surface, self.brush_color, (x, y), self.size)

    def assign_color(self, color):
        self.brush_color = color
    
    def assign_size(self, size):
        self.size = size

    def draw_square(self, points, message_points):
        x1,y1 = points[0]
        x2,y2 = points[1]

        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)
        
        for x in range(min_x, max_x, 1):
            self.draw_brush(x, y1)
            self.draw_brush(x, y2)
            message_points.append((x, y1))
            message_points.append((x, y2))

        for y in range(min_y, max_y, 1):
            self.draw_brush(x1, y)
            self.draw_brush(x2, y)
            message_points.append((x1, y))
            message_points.append((x2, y))

        
    def draw_circle(self, points, message_points):
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
                x, y = mid_x + smajor * math.cos(t), mid_y + sminor * math.sin(t)
                self.draw_brush(x, y)
                message_points.append((int(x),int(y)))
        else:
            for t in range(0, int(2*math.pi * 100),1):
                x, y = mid_x + sminor * math.cos(t), mid_y + smajor * math.sin(t)
                self.draw_brush(x, y)
                message_points.append((int(x),int(y)))

    def draw_line(self, points, message_points):
        # Bresenham's Line Algorithm
        x1, y1 = points[0]
        x2, y2 = points[1]

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            message_points.append((x1, y1))
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
        screen.blit(self.surface, (0, 0))
    
    def to_bytes(self):
        return py.image.tobytes(self.surface, "RGBA")
    
    def from_bytes(self, byte_string, size=(1000,1000)):
        return py.image.frombytes(byte_string, size, "RGBA")


class Display():
    def __init__(self):
        self.canvas = Canvas(1000, 1000)
        self.size = 1000

    def draw(self):
        self.canvas.render(screen)

    def update(self, mouse_pos, message_points):
        if tool_selected[0] and 0<= mouse_pos[0] < self.size and 0<= mouse_pos[1] < self.size:
            message_points.append(mouse_pos)
            self.canvas.draw_brush(mouse_pos[0], mouse_pos[1])


def main():
    display = Display()
    toolbar = Toolbar()
    colors = Colors()
    sizes = Sizes()

    running = True
    pressed = False

    message_points = []
    point_buffer = []

    server = "127.0.0.1" # change to current device ip address to let all devices on LAN connect

    portid = 5000
    port = None
    sock = None

    try:
        port = Client.Port()
        sock = port.connect(server, portid)
    except Exception as e:
        print(e)
        sys.exit(1)

    recv_messages = []
    lock = threading.Lock()

    recv_thread = threading.Thread(target=Client.receive_messages, args=(sock, recv_messages, lock), daemon=True)
    recv_thread.start()

    while running:
        screen.fill((100,100,100))
        with lock:
            if recv_messages:
                temp = recv_messages[0].split("//")
                size, color, message = temp[0], temp[1], temp[2]
                color = color.split(",")
                color = int(color[0]), int(color[1]), int(color[2])
                points = [point.split(",") for point in message.split("/")[:-1]]
                [display.canvas.draw_message(color, int(point[0]), int(point[1]), size=int(size)) for point in points]
                recv_messages.clear()
        
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
            elif event.type == py.MOUSEBUTTONDOWN:
                mouse_pos = py.mouse.get_pos()
                pressed = True
                if 0 <= mouse_pos[0] < 1000 and 0 <= mouse_pos[1] < 1000:
                    point_buffer.append(mouse_pos)
                elif 1000 <= mouse_pos[0] < 1050 and 0 <= mouse_pos[1] < toolbar.get_end():
                    toolbar.update(mouse_pos)
                elif 1000 <= mouse_pos[0] < 1050 and toolbar.get_end() <= mouse_pos[1] < colors.get_end():
                    colors.update(mouse_pos)
                    display.canvas.assign_color(colors.get_color())
                elif 1000 <= mouse_pos[0] < 1050 and colors.get_end() <= mouse_pos[1] < sizes.get_end():
                    sizes.update(mouse_pos)
                    display.canvas.assign_size(sizes.get_size())
                        
            elif event.type == py.MOUSEBUTTONUP:
                pressed = False
                mouse_pos = py.mouse.get_pos()
                if 0 <= mouse_pos[0] < 1000 and 0 <= mouse_pos[1] < 1000 and len(point_buffer) > 0:
                    point_buffer.append(mouse_pos)
                    if tool_selected[1]:
                        display.canvas.draw_circle(point_buffer, message_points)
                    elif tool_selected[2]:
                        display.canvas.draw_line(point_buffer, message_points)
                    elif tool_selected[3]:
                        display.canvas.draw_square(point_buffer, message_points)
                    point_buffer = []
                else:
                    point_buffer = []

        if pressed:
            mouse_pos = py.mouse.get_pos()
            display.update(mouse_pos, message_points)
        else:
            if message_points:
                color = display.canvas.brush_color
                Client.send_message(f"{sizes.get_size()}//"+f"{color[0]},{color[1]},{color[2]}//"+"".join([f"{m[0]},{m[1]}/"for m in set(message_points)]), sock)
            message_points = []

        display.draw()
        toolbar.draw()
        colors.draw()
        sizes.draw()

        clock.tick(500)
        py.display.flip()

    py.quit()

if __name__ == "__main__":
    main()