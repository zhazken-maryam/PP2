import pygame              # библиотека для графики
import datetime            # работа с текущим временем
import math                # sin, cos, radians
import os                  # работа с путями
import sys                 # завершение программы

pygame.init()              # инициализация pygame

# размеры окна
W, H = 600, 400

# центр окна
CENTER = (W // 2, H // 2)

# создаем окно
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Mickey Clock")

# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# объект для контроля скорости обновления
clock = pygame.time.Clock()

# путь к папке текущего файла
base = os.path.dirname(__file__)

# путь к папке images
img_path = os.path.join(base, "images")

# загружаем картинку циферблата
face = pygame.image.load(os.path.join(img_path, "clock.png")).convert_alpha()

# подгоняем картинку под размер окна
face = pygame.transform.scale(face, (W, H))


def get_hand_end(center, angle_deg, length):
    # переводим угол в радианы
    # -90 нужен, чтобы 0 градусов смотрел вверх
    angle_rad = math.radians(angle_deg - 90)

    # вычисляем конец стрелки
    x = center[0] + length * math.cos(angle_rad)
    y = center[1] + length * math.sin(angle_rad)

    return int(x), int(y)


def draw_hand(surface, color, center, angle, length, width):
    # получаем координаты конца стрелки
    end_pos = get_hand_end(center, angle, length)

    # рисуем стрелку
    pygame.draw.line(surface, color, center, end_pos, width)


def get_angles(now):
    # берем только минуты и секунды
    minute = now.minute
    second = now.second

    # 1 минута = 6 градусов
    minute_angle = minute * 6

    # 1 секунда = 6 градусов
    second_angle = second * 6

    return minute_angle, second_angle


run = True
while run:
    # обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # текущее системное время
    now = datetime.datetime.now()

    # углы для минут и секунд
    minute_angle, second_angle = get_angles(now)

    # очищаем экран
    screen.fill(WHITE)

    # рисуем фон
    screen.blit(face, (0, 0))

    # рисуем минутную стрелку
    draw_hand(screen, BLACK, CENTER, minute_angle, 100, 5)

    # рисуем секундную стрелку
    draw_hand(screen, RED, CENTER, second_angle, 120, 3)

    # рисуем центр
    pygame.draw.circle(screen, BLACK, CENTER, 6)

    # обновляем экран
    pygame.display.flip()

    # обновляем раз в секунду
    clock.tick(1)

pygame.quit()
sys.exit()