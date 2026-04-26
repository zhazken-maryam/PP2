import pygame
from snake import Snake, Food

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
snake = Snake()
food = Food()

font = pygame.font.SysFont(None, 36)

score = 0
level = 1
to_next_level = 4
speed = 10

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False

    snake.controls()
    snake.move()

    if snake.body[0] == food.position:
        snake.grow()
        food.position = food.random_pos()

        score += 1

        if score % to_next_level == 0:
            level += 1
            speed += 2

    x, y = snake.body[0]
    if x < 0 or x >= 600 or y < 0 or y >= 600:
        print("Game Over")
        run = False

    if snake.body[0] in snake.body[1:]:
        print("Game Over")
        run = False

    screen.fill((0, 0, 0))
    snake.draw(screen)
    food.draw(screen)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    level_text = font.render(f"Level: {level}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))
    pygame.display.update()
    clock.tick(speed)

pygame.quit()