import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Paint")
    clock = pygame.time.Clock()

    radius = 5
    mode = 'blue'
    tool = 'brush'

    drawing = False
    start_pos = None
    points = []

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'

                # инструменты
                elif event.key == pygame.K_1:
                    tool = 'brush'
                elif event.key == pygame.K_2:
                    tool = 'rect'
                elif event.key == pygame.K_3:
                    tool = 'circle'
                elif event.key == pygame.K_4:
                    tool = 'eraser'
                elif event.key == pygame.K_5:
                    tool = "square"
                elif event.key == pygame.K_6:
                    tool = "rtriangle"
                elif event.key == pygame.K_7:
                    tool = "etriangle"
                elif event.key == pygame.K_8:
                    tool = "rhombus"

            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False

                if tool == 'rect':
                    draw_rect(screen, start_pos, event.pos, get_color(mode))
                elif tool == 'circle':
                    draw_circle(screen, start_pos, event.pos, get_color(mode))
                elif tool == 'square':
                    draw_square(screen, start_pos, event.pos, get_color(mode))
                elif tool == 'rtriangle':
                    draw_right_triangle(screen, start_pos, event.pos, get_color(mode))
                elif tool == 'etriangle':
                    draw_equilateral_triangle(screen, start_pos, event.pos, get_color(mode))
                elif tool == 'rhombus':
                    draw_rhombus(screen, start_pos, event.pos, get_color(mode))

            if event.type == pygame.MOUSEMOTION and drawing:
                if tool == 'brush':
                    points.append(event.pos)
                    points = points[-256:]
                elif tool == 'eraser':
                    pygame.draw.circle(screen, (0, 0, 0), event.pos, 20)



        for i in range(len(points) - 1):
            drawLineBetween(screen, i, points[i], points[i + 1], radius, mode)

        pygame.display.flip()
        clock.tick(60)


def get_color(mode):
    if mode == 'blue':
        return (0, 0, 255)
    elif mode == 'red':
        return (255, 0, 0)
    elif mode == 'green':
        return (0, 255, 0)


def draw_rect(screen, start, end, color):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w = abs(start[0] - end[0])
    h = abs(start[1] - end[1])
    pygame.draw.rect(screen, color, (x, y, w, h), 2)


def draw_circle(screen, start, end, color):
    radius = int(((end[0]-start[0])**2 + (end[1]-start[1])**2) ** 0.5)
    pygame.draw.circle(screen, color, start, radius, 2)


def drawLineBetween(screen, index, start, end, width, color_mode):
    if color_mode == 'blue':
        color = (0, 0, 255)
    elif color_mode == 'red':
        color = (255, 0, 0)
    elif color_mode == 'green':
        color = (0, 255, 0)

    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    for i in range(iterations):
        progress = i / iterations
        x = int(start[0] * (1 - progress) + end[0] * progress)
        y = int(start[1] * (1 - progress) + end[1] * progress)
        pygame.draw.circle(screen, color, (x, y), width)


def draw_square(screen, start, end, color):
    size = min(abs(end[0] - start[0]), abs(end[1] - start[1]))
    x = start[0]
    y = start[1]

    if end[0] < start[0]:
        x -= size
    if end[1] < start[1]:
        y -= size

    pygame.draw.rect(screen, color, (x, y, size, size), 2)


def draw_right_triangle(screen, start, end, color):
    p1 = start
    p2 = (start[0], end[1])
    p3 = end

    pygame.draw.polygon(screen, color, [p1, p2, p3], 2)


def draw_equilateral_triangle(screen, start, end, color):
    side = abs(end[0] - start[0])
    height = int((math.sqrt(3) / 2) * side)

    p1 = start
    p2 = (start[0] + side, start[1])
    p3 = (start[0] + side // 2, start[1] - height)

    pygame.draw.polygon(screen, color, [p1, p2, p3], 2)


def draw_rhombus(screen, start, end, color):
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2

    width = abs(end[0] - start[0]) // 2
    height = abs(end[1] - start[1]) // 2

    p1 = (cx, cy - height)
    p2 = (cx + width, cy)
    p3 = (cx, cy + height)
    p4 = (cx - width, cy)

    pygame.draw.polygon(screen, color, [p1, p2, p3, p4], 2)

main()