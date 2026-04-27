import pygame
import sys
import json

from db import create_tables, get_top_scores
from game import run_game, WIDTH, HEIGHT
from settings import load_settings, save_settings


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (170, 170, 170)
DARK_GRAY = (80, 80, 80)
BLUE = (60, 120, 230)
RED = (220, 60, 60)


class Button:
    """Simple button class."""
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen, font):
        color = GRAY if self.rect.collidepoint(pygame.mouse.get_pos()) else DARK_GRAY
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=8)

        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def center_text(screen, font, text, y, color=BLACK):
    """Draws centered text."""
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(WIDTH // 2, y))
    screen.blit(surface, rect)


def username_screen(screen, clock):
    """Username entry using Pygame keyboard input."""
    font_big = pygame.font.SysFont(None, 56)
    font = pygame.font.SysFont(None, 34)

    username = ""

    while True:
        screen.fill((235, 235, 235))
        center_text(screen, font_big, "Snake Game", 130)
        center_text(screen, font, "Enter username:", 230)
        center_text(screen, font, username + "|", 285)
        center_text(screen, font, "Press Enter to continue", 350)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if username.strip():
                        return username.strip()

                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                elif event.key == pygame.K_ESCAPE:
                    return None

                else:
                    if len(username) < 15:
                        username += event.unicode

        clock.tick(60)


def main_menu(screen, clock, username):
    """Main menu screen."""
    font_big = pygame.font.SysFont(None, 56)
    font = pygame.font.SysFont(None, 34)

    play = Button(300, 220, 200, 55, "Play")
    leaderboard = Button(300, 295, 200, 55, "Leaderboard")
    settings = Button(300, 370, 200, 55, "Settings")
    quit_btn = Button(300, 445, 200, 55, "Quit")

    while True:
        screen.fill((235, 235, 235))
        center_text(screen, font_big, "TSIS4 Snake Game", 110)
        center_text(screen, font, f"Player: {username}", 170)

        for btn in [play, leaderboard, settings, quit_btn]:
            btn.draw(screen, font)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if play.clicked(event):
                return "play"
            if leaderboard.clicked(event):
                return "leaderboard"
            if settings.clicked(event):
                return "settings"
            if quit_btn.clicked(event):
                return "quit"

        clock.tick(60)


def leaderboard_screen(screen, clock):
    """Shows top 10 from PostgreSQL."""
    font_big = pygame.font.SysFont(None, 54)
    font = pygame.font.SysFont(None, 30)
    back = Button(300, 530, 200, 50, "Back")

    while True:
        scores = get_top_scores()

        screen.fill((235, 235, 235))
        center_text(screen, font_big, "Leaderboard Top 10", 60)

        y = 120
        if not scores:
            center_text(screen, font, "No scores yet.", y)
        else:
            for i, row in enumerate(scores, start=1):
                username, score, level, date = row
                text = f"{i}. {username} | Score: {score} | Level: {level} | {date}"
                screen.blit(font.render(text, True, BLACK), (80, y))
                y += 36

        back.draw(screen, font)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if back.clicked(event):
                return "menu"

        clock.tick(60)


def settings_screen(screen, clock, settings):
    """Settings screen: grid, sound, snake color."""
    font_big = pygame.font.SysFont(None, 54)
    font = pygame.font.SysFont(None, 32)

    grid_btn = Button(300, 240, 200, 50, "Toggle Grid")
    sound_btn = Button(300, 310, 200, 50, "Toggle Sound")
    color_btn = Button(300, 380, 200, 50, "Change Color")
    save_btn = Button(300, 480, 200, 50, "Save & Back")

    colors = [
        [0, 180, 0],
        [60, 120, 230],
        [220, 60, 60],
        [180, 70, 220]
    ]

    while True:
        screen.fill((235, 235, 235))
        center_text(screen, font_big, "Settings", 80)

        grid_text = "Grid: ON" if settings["grid"] else "Grid: OFF"
        sound_text = "Sound: ON" if settings["sound"] else "Sound: OFF"
        color_text = f"Snake color: {settings['snake_color']}"

        screen.blit(font.render(grid_text, True, BLACK), (280, 150))
        screen.blit(font.render(sound_text, True, BLACK), (280, 185))
        screen.blit(font.render(color_text, True, BLACK), (280, 220))

        for btn in [grid_btn, sound_btn, color_btn, save_btn]:
            btn.draw(screen, font)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if grid_btn.clicked(event):
                settings["grid"] = not settings["grid"]

            if sound_btn.clicked(event):
                settings["sound"] = not settings["sound"]

            if color_btn.clicked(event):
                index = colors.index(settings["snake_color"]) if settings["snake_color"] in colors else 0
                settings["snake_color"] = colors[(index + 1) % len(colors)]

            if save_btn.clicked(event):
                save_settings(settings)
                return "menu"

        clock.tick(60)


def game_over_screen(screen, clock, result):
    """Game over screen."""
    font_big = pygame.font.SysFont(None, 60)
    font = pygame.font.SysFont(None, 34)

    retry = Button(300, 360, 200, 55, "Retry")
    menu = Button(300, 435, 200, 55, "Main Menu")

    while True:
        screen.fill((235, 235, 235))
        center_text(screen, font_big, "Game Over", 120, RED)
        center_text(screen, font, f"Final score: {result['score']}", 210)
        center_text(screen, font, f"Level reached: {result['level']}", 255)
        center_text(screen, font, f"Personal best: {result['personal_best']}", 300)

        retry.draw(screen, font)
        menu.draw(screen, font)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if retry.clicked(event):
                return "retry"

            if menu.clicked(event):
                return "menu"

        clock.tick(60)


def main():
    pygame.init()

    create_tables()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS4 Snake Game")
    clock = pygame.time.Clock()

    settings = load_settings()
    username = username_screen(screen, clock)

    if username is None:
        pygame.quit()
        sys.exit()

    while True:
        action = main_menu(screen, clock, username)

        if action == "quit":
            break

        elif action == "leaderboard":
            result = leaderboard_screen(screen, clock)
            if result == "quit":
                break

        elif action == "settings":
            result = settings_screen(screen, clock, settings)
            if result == "quit":
                break

        elif action == "play":
            while True:
                result = run_game(screen, clock, username, settings)

                if result is None:
                    pygame.quit()
                    sys.exit()

                after_game = game_over_screen(screen, clock, result)

                if after_game == "retry":
                    continue

                if after_game == "menu":
                    break

                if after_game == "quit":
                    pygame.quit()
                    sys.exit()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()