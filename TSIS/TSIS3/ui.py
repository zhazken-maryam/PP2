import pygame


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DARK_GRAY = (80, 80, 80)
BLUE = (60, 120, 230)
GREEN = (40, 170, 80)
RED = (220, 60, 60)
YELLOW = (230, 200, 30)


class Button:
    """Simple rectangle button."""
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen, font):
        mouse_pos = pygame.mouse.get_pos()
        color = GRAY if self.rect.collidepoint(mouse_pos) else DARK_GRAY

        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=8)

        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def draw_center_text(screen, font, text, y, color=BLACK):
    """Draws centered text."""
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=(screen.get_width() // 2, y))
    screen.blit(text_surface, rect)


def ask_username(screen, clock):
    """Simple username input screen before game starts."""
    font_big = pygame.font.SysFont(None, 56)
    font = pygame.font.SysFont(None, 34)

    name = ""

    while True:
        screen.fill((235, 235, 235))
        draw_center_text(screen, font_big, "Enter your name", 190)
        draw_center_text(screen, font, name + "|", 270)
        draw_center_text(screen, font, "Press Enter to start", 340)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name.strip():
                        return name.strip()
                elif event.key == pygame.K_ESCAPE:
                    return None
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 12:
                        name += event.unicode

        clock.tick(60)


def draw_hud(screen, font, score, coins, distance, finish_distance, active_power, power_time, shield):
    """Draws in-game HUD."""
    remaining = max(0, int(finish_distance - distance))

    lines = [
        f"Score: {score}",
        f"Coins: {coins}",
        f"Distance: {int(distance)} m",
        f"Remaining: {remaining} m",
    ]

    if active_power:
        lines.append(f"Power-up: {active_power} {power_time:.1f}s")
    elif shield:
        lines.append("Power-up: Shield ready")
    else:
        lines.append("Power-up: None")

    x = 10
    y = 10
    for line in lines:
        screen.blit(font.render(line, True, BLACK), (x, y))
        y += 24


def draw_leaderboard(screen, leaderboard, back_button):
    """Draws top 10 leaderboard screen."""
    font_big = pygame.font.SysFont(None, 54)
    font = pygame.font.SysFont(None, 32)

    screen.fill((235, 235, 235))
    draw_center_text(screen, font_big, "Leaderboard Top 10", 70)

    y = 130
    if not leaderboard:
        draw_center_text(screen, font, "No scores yet.", y)
    else:
        for i, item in enumerate(leaderboard, start=1):
            text = f"{i}. {item['name']}   Score: {item['score']}   Distance: {item['distance']} m"
            screen.blit(font.render(text, True, BLACK), (160, y))
            y += 38

    back_button.draw(screen, font)


def draw_settings(screen, settings, buttons):
    """Draws settings screen."""
    font_big = pygame.font.SysFont(None, 54)
    font = pygame.font.SysFont(None, 32)

    screen.fill((235, 235, 235))
    draw_center_text(screen, font_big, "Settings", 70)

    sound_text = "Sound: ON" if settings["sound"] else "Sound: OFF"
    color_text = f"Car color: {settings['car_color']}"
    difficulty_text = f"Difficulty: {settings['difficulty']}"

    screen.blit(font.render(sound_text, True, BLACK), (360, 140))
    screen.blit(font.render(color_text, True, BLACK), (360, 185))
    screen.blit(font.render(difficulty_text, True, BLACK), (360, 230))

    for button in buttons:
        button.draw(screen, font)


def draw_game_over(screen, font_big, font, score, distance, coins, retry_button, menu_button):
    """Draws game over screen."""
    screen.fill((235, 235, 235))

    draw_center_text(screen, font_big, "Game Over", 130, RED)
    draw_center_text(screen, font, f"Score: {score}", 220)
    draw_center_text(screen, font, f"Distance: {int(distance)} m", 260)
    draw_center_text(screen, font, f"Coins: {coins}", 300)

    retry_button.draw(screen, font)
    menu_button.draw(screen, font)
