import pygame
import random

from db import save_result, get_personal_best


WIDTH = 800
HEIGHT = 600
CELL = 20

GRID_WIDTH = WIDTH // CELL
GRID_HEIGHT = HEIGHT // CELL

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DARK_GRAY = (80, 80, 80)
GREEN = (0, 180, 0)
RED = (220, 40, 40)
DARK_RED = (120, 0, 0)
BLUE = (50, 100, 230)
YELLOW = (230, 210, 40)
PURPLE = (160, 70, 220)
CYAN = (40, 200, 220)
ORANGE = (240, 140, 40)


def random_cell(forbidden):
    """Returns random cell that is not in forbidden set."""
    while True:
        pos = (
            random.randint(1, GRID_WIDTH - 2),
            random.randint(1, GRID_HEIGHT - 2)
        )

        if pos not in forbidden:
            return pos


def draw_grid(screen):
    """Draws grid overlay."""
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, (225, 225, 225), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, (225, 225, 225), (0, y), (WIDTH, y))


def draw_cell(screen, pos, color):
    """Draws one grid cell."""
    rect = pygame.Rect(pos[0] * CELL, pos[1] * CELL, CELL, CELL)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 1)


def create_obstacles(snake, food_positions):
    """
    Creates static obstacle blocks from level 3.
    It avoids snake area and food positions.
    """
    forbidden = set(snake) | set(food_positions)

    # Keep free area around snake head so it is not trapped immediately.
    head_x, head_y = snake[0]
    for dx in range(-2, 3):
        for dy in range(-2, 3):
            forbidden.add((head_x + dx, head_y + dy))

    obstacles = set()
    count = 8

    while len(obstacles) < count:
        pos = random_cell(forbidden | obstacles)
        obstacles.add(pos)

    return obstacles


def spawn_food(snake, obstacles):
    """Spawns weighted normal food."""
    forbidden = set(snake) | set(obstacles)
    pos = random_cell(forbidden)
    value = random.choice([1, 2, 3])
    created_at = pygame.time.get_ticks()
    return {
        "pos": pos,
        "value": value,
        "created_at": created_at,
        "lifetime": 7000
    }


def spawn_poison(snake, obstacles, food_pos):
    """Spawns poison food."""
    forbidden = set(snake) | set(obstacles) | {food_pos}
    return {
        "pos": random_cell(forbidden),
        "created_at": pygame.time.get_ticks(),
        "lifetime": 8000
    }


def spawn_powerup(snake, obstacles, food_pos, poison_pos):
    """Spawns one power-up on field."""
    forbidden = set(snake) | set(obstacles) | {food_pos, poison_pos}
    kind = random.choice(["speed", "slow", "shield"])
    return {
        "pos": random_cell(forbidden),
        "kind": kind,
        "created_at": pygame.time.get_ticks(),
        "lifetime": 8000
    }


def get_speed(level, active_power):
    """Returns snake speed depending on level and active power-up."""
    speed = 7 + level

    if active_power == "speed":
        speed += 5
    elif active_power == "slow":
        speed = max(4, speed - 4)

    return speed


def run_game(screen, clock, username, settings):
    """
    Main Snake game loop.
    Returns result dictionary after game over.
    """
    font = pygame.font.SysFont(None, 28)

    personal_best = get_personal_best(username)

    snake = [(10, 10), (9, 10), (8, 10)]
    direction = (1, 0)
    next_direction = direction

    score = 0
    level = 1
    eaten_count = 0

    obstacles = set()

    food = spawn_food(snake, obstacles)
    poison = None
    powerup = None

    active_power = None
    active_power_end = 0
    shield = False

    last_level_for_obstacles = level
    running = True

    while running:
        now = pygame.time.get_ticks()

        speed = get_speed(level, active_power)
        clock.tick(speed)

        # Timed active power-ups
        if active_power in ("speed", "slow") and now > active_power_end:
            active_power = None

        # Food disappears after timer
        if now - food["created_at"] > food["lifetime"]:
            food = spawn_food(snake, obstacles)

        # Poison appears sometimes and disappears after timer
        if poison is None and random.randint(1, 100) <= 5:
            poison = spawn_poison(snake, obstacles, food["pos"])

        if poison is not None and now - poison["created_at"] > poison["lifetime"]:
            poison = None

        # Only one power-up active on field
        if powerup is None and random.randint(1, 100) <= 4:
            poison_pos = poison["pos"] if poison else (-1, -1)
            powerup = spawn_powerup(snake, obstacles, food["pos"], poison_pos)

        if powerup is not None and now - powerup["created_at"] > powerup["lifetime"]:
            powerup = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    next_direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    next_direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    next_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    next_direction = (1, 0)

        direction = next_direction

        head_x, head_y = snake[0]
        new_head = (head_x + direction[0], head_y + direction[1])

        hit_wall = (
            new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT
        )

        hit_self = new_head in snake
        hit_obstacle = new_head in obstacles

        if hit_wall or hit_self or hit_obstacle:
            if shield:
                shield = False
                new_head = snake[0]
            else:
                running = False
                continue

        snake.insert(0, new_head)

        ate_food = new_head == food["pos"]
        ate_poison = poison is not None and new_head == poison["pos"]
        ate_powerup = powerup is not None and new_head == powerup["pos"]

        if ate_food:
            score += food["value"] * 10
            eaten_count += 1

            if eaten_count % 3 == 0:
                level += 1

            food = spawn_food(snake, obstacles)

        else:
            snake.pop()

        if ate_poison:
            # Shorten snake by 2 segments
            for _ in range(2):
                if len(snake) > 0:
                    snake.pop()

            poison = None

            if len(snake) <= 1:
                running = False
                continue

        if ate_powerup:
            if powerup["kind"] == "speed":
                active_power = "speed"
                active_power_end = now + 5000
                shield = False

            elif powerup["kind"] == "slow":
                active_power = "slow"
                active_power_end = now + 5000
                shield = False

            elif powerup["kind"] == "shield":
                active_power = None
                shield = True

            powerup = None

        if level >= 3 and level != last_level_for_obstacles:
            poison_pos = poison["pos"] if poison else (-1, -1)
            obstacles = create_obstacles(snake, [food["pos"], poison_pos])
            last_level_for_obstacles = level

        # ---------- DRAW ----------
        screen.fill(WHITE)

        if settings["grid"]:
            draw_grid(screen)

        # Draw border
        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, HEIGHT), 4)

        for block in obstacles:
            draw_cell(screen, block, DARK_GRAY)

        # Draw snake
        snake_color = tuple(settings["snake_color"])
        for part in snake:
            draw_cell(screen, part, snake_color)

        # Draw normal food color by value
        food_color = YELLOW if food["value"] == 1 else ORANGE if food["value"] == 2 else RED
        draw_cell(screen, food["pos"], food_color)

        if poison:
            draw_cell(screen, poison["pos"], DARK_RED)

        if powerup:
            if powerup["kind"] == "speed":
                color = CYAN
            elif powerup["kind"] == "slow":
                color = BLUE
            else:
                color = PURPLE
            draw_cell(screen, powerup["pos"], color)

        power_text = "None"
        if active_power:
            left = max(0, (active_power_end - now) // 1000)
            power_text = f"{active_power} {left}s"
        elif shield:
            power_text = "Shield ready"

        hud_lines = [
            f"Player: {username}",
            f"Score: {score}",
            f"Level: {level}",
            f"Best: {personal_best}",
            f"Power-up: {power_text}",
            "Food: yellow/orange/red | Poison: dark red"
        ]

        y = 10
        for line in hud_lines:
            screen.blit(font.render(line, True, BLACK), (10, y))
            y += 24

        pygame.display.flip()

    save_result(username, score, level)

    return {
        "score": score,
        "level": level,
        "personal_best": max(personal_best, score)
    }