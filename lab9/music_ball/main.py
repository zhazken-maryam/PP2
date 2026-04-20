import pygame
import sys
import os
from player import MusicPlayer  # импортируем класс плеера из player.py


def main():
    pygame.init()         # инициализация pygame
    pygame.mixer.init()   # инициализация музыкального модуля

    # размеры окна
    WIDTH, HEIGHT = 600, 400

    # создаем окно
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Music Player")

    # создаем шрифт
    font = pygame.font.SysFont(None, 36)

    # путь к текущей папке
    BASE_DIR = os.path.dirname(__file__)

    # путь к папке music
    music_path = os.path.join(BASE_DIR, "music")

    # создаем объект плеера
    player = MusicPlayer(music_path)

    # clock нужен для FPS
    clock = pygame.time.Clock()

    running = True
    while running:
        # закрашиваем фон темным цветом
        screen.fill((30, 30, 30))

        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # если нажата клавиша
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    player.play()         # воспроизвести текущий трек

                elif event.key == pygame.K_s:
                    player.stop()         # остановить музыку

                elif event.key == pygame.K_n:
                    player.next_track()   # следующий трек

                elif event.key == pygame.K_b:
                    player.prev_track()   # предыдущий трек

                elif event.key == pygame.K_q:
                    running = False       # выход из программы

        # получаем имя текущего трека
        track_name = player.get_current_track_name()

        # создаем текст с названием трека
        text = font.render(f"Track: {track_name}", True, (255, 255, 255))
        screen.blit(text, (50, 100))

        # в зависимости от состояния выводим статус
        if player.is_playing:
            status = "Playing"
            color = (0, 200, 0)
        else:
            status = "Stopped"
            color = (200, 0, 0)

        # рисуем статус
        status_text = font.render(f"Status: {status}", True, color)
        screen.blit(status_text, (50, 150))

        # выводим управление
        controls1 = font.render("P - Play", True, (180, 180, 180))
        controls2 = font.render("S - Stop", True, (180, 180, 180))
        controls3 = font.render("N - Next", True, (180, 180, 180))
        controls4 = font.render("B - Previous", True, (180, 180, 180))
        controls5 = font.render("Q - Quit", True, (180, 180, 180))

        screen.blit(controls1, (50, 200))
        screen.blit(controls2, (50, 235))
        screen.blit(controls3, (50, 270))
        screen.blit(controls4, (50, 305))
        screen.blit(controls5, (50, 340))

        # обновляем экран
        pygame.display.flip()

        # ограничиваем FPS
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()