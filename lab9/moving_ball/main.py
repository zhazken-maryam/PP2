import pygame  # библиотека для графики

pygame.init()  # запуск pygame

# размеры окна
WIDTH, HEIGHT = 700, 500

# создаем окно
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

# цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# объект для контроля FPS
clock = pygame.time.Clock()

# начальная позиция шара - центр окна
x, y = WIDTH // 2, HEIGHT // 2

# радиус шара
radius = 25

# шаг движения
step = 20

running = True
while running:
    # обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # если нажата клавиша
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= step
            elif event.key == pygame.K_RIGHT:
                x += step
            elif event.key == pygame.K_UP:
                y -= step
            elif event.key == pygame.K_DOWN:
                y += step

    # ограничиваем движение по x
    # шар не должен выходить за левую и правую границы
    x = max(radius, min(WIDTH - radius, x))

    # ограничиваем движение по y
    # шар не должен выходить за верхнюю и нижнюю границы
    y = max(radius, min(HEIGHT - radius, y))

    # закрашиваем экран белым
    screen.fill(WHITE)

    # рисуем красный шар
    pygame.draw.circle(screen, RED, (x, y), radius)

    # обновляем экран
    pygame.display.flip()

    # 60 кадров в секунду
    clock.tick(60)

pygame.quit()