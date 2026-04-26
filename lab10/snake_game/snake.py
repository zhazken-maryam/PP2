import pygame
import random

class Snake:
    def __init__(self):
        self.body = [(300, 300)]
        self.dx = 10
        self.dy = 0
        self.is_grow = False

    def move(self):
        head = (self.body[0][0] + self.dx, self.body[0][1] + self.dy)
        self.body.insert(0, head)
        if not self.is_grow:
            self.body.pop()
        else:
            self.is_grow = False

    def grow(self):
        self.is_grow = True

    def controls(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and self.dy == 0:
            self.dx, self.dy = 0, -10
        if keys[pygame.K_DOWN] and self.dy == 0:
            self.dx, self.dy = 0, 10
        if keys[pygame.K_LEFT] and self.dx == 0:
            self.dx, self.dy = -10, 0
        if keys[pygame.K_RIGHT] and self.dx == 0:
            self.dx, self.dy = 10, 0

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, (0, 255, 0), (*segment, 20, 20))

class Food():
    def __init__(self):
        self.position = self.random_pos()

    def random_pos(self):
        return (random.randrange(60, 250, 20), random.randrange(60, 500, 20))

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (*self.position, 20, 20))