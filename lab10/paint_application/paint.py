import pygame

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

            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False

                if tool == 'rect':
                    draw_rect(screen, start_pos, event.pos, get_color(mode))
                elif tool == 'circle':
                    draw_circle(screen, start_pos, event.pos, get_color(mode))

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


main()