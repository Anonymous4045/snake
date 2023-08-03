"""
A simple game of snake, with a few twists.
"""

import random
import time

import pygame

WIDTH = 15  # number of columns
HEIGHT = 10  # number of rows

INITIAL_SPEED = 25
SPEED_INCREASE_PER_APPLE = 1

pygame.init()

# assets
SNAKE_BODY = pygame.image.load("assets/snake_body(32x32).png")
APPLE = pygame.image.load("assets/apple.png")
SNAKE_HEAD = pygame.image.load("assets/snake_head.png")


pygame.display.set_caption("Snake")
pygame.display.set_icon(pygame.image.load("assets/snake_body.png"))

SCREEN_SIZE = 32 * WIDTH, 32 * HEIGHT
SCREEN = pygame.display.set_mode(SCREEN_SIZE)

x_positions = [i for i in range(32 * WIDTH) if i % 32 == 0]
y_positions = [i for i in range(32 * HEIGHT) if i % 32 == 0]


# Colors
BLACK = 0, 0, 0

# Keys
w = pygame.K_w
a = pygame.K_a
s = pygame.K_s
d = pygame.K_d
q = pygame.K_q


def make_apple() -> tuple[int, int] | None:
    """
    Generates a new position for the apple. If none is found, return None.
    :return:
    """

    while True:
        rand_x, rand_y = random.randint(0, len(x_positions) - 1), random.randint(
            0, len(y_positions) - 1
        )
        if x_positions[rand_x] != head_x and y_positions[rand_y] != head_y:
            return x_positions[rand_x], y_positions[rand_y]


def change_direction(current_direction) -> str | None:
    """
    Inverts the direction of the snake.
    :param current_direction: The direction the snake is traveling
    :return: The new direction
    """

    return {"up": "down", "down": "up", "left": "right", "right": "left"}.get(
        current_direction
    )


while True:
    head_x, head_y = 32 * WIDTH / 2, 32 * HEIGHT / 2
    if head_x % 32 != 0:
        head_x -= head_x % 32
    if head_y % 32 != 0:
        head_y -= head_y % 32

    apple_x, apple_y = 0, 0

    make_apple()

    direction = "right"

    speed = 10 / INITIAL_SPEED
    speed_cap = 0.1
    speed_rate = 0.01 * SPEED_INCREASE_PER_APPLE

    segments = 1

    all_positions = [(0, 100000)]

    game_loop = True
    while game_loop:
        all_positions.append((head_x, head_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Game quit")
                pygame.quit()
                game_loop = False
            if event.type == pygame.KEYDOWN:
                if event.key == q:
                    print("Game quit")
                    pygame.quit()
                    game_loop = False
                elif event.key == a and direction != "right":
                    direction = "left"
                elif event.key == d and direction != "left":
                    direction = "right"
                elif event.key == w and direction != "down":
                    direction = "up"
                elif event.key == s and direction != "up":
                    direction = "down"

        if direction == "up":
            head_y -= 32
        elif direction == "down":
            head_y += 32
        elif direction == "left":
            head_x -= 32
        elif direction == "right":
            head_x += 32

        if head_x > 32 * (WIDTH - 1):
            head_x = 0
        if head_x < 0:
            head_x = 32 * (WIDTH - 1)
        if head_y > 32 * (HEIGHT - 1):
            head_y = 0
        if head_y < 0:
            head_y = 32 * (HEIGHT - 1)

        if not game_loop:
            break

        print(speed)
        if head_x == apple_x and head_y == apple_y:
            apple_x, apple_y = make_apple()
            speed -= speed_rate
            segments += 1
            speed = max(speed, speed_cap)

        SCREEN.fill(BLACK)
        SCREEN.blit(SNAKE_HEAD, (head_x, head_y))
        SCREEN.blit(APPLE, (apple_x, apple_y))

        if segments > 0:
            for segment in range(segments):
                segment_pos = all_positions[-1 * segment]
                if segment_pos == (head_x, head_y):
                    if segment == 2:
                        if direction == "left":
                            head_x += 32
                        elif direction == "right":
                            head_x -= 32
                        elif direction == "up":
                            head_y += 32
                        elif direction == "down":
                            head_y -= 32
                        direction = change_direction(direction)
                    else:
                        print("You died!")
                        game_loop = False
                SCREEN.blit(SNAKE_BODY, segment_pos)

        pygame.display.flip()
        time.sleep(speed)
