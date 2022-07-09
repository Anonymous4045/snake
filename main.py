import pygame, time, random

width = 15 # number of columns
height = 10 # number of rows

initial_speed = 25
initial_speed_rate = 1 # How much the speed increases per apple eaten

pygame.init()

# Assets
snake_body = pygame.image.load('Assets/snake_body(32x32).png')
apple = pygame.image.load('Assets/snake apple.png')
snake_head = pygame.image.load('Assets/snake head.png')


pygame.display.set_caption('Snake')
pygame.display.set_icon(pygame.image.load('Assets/snake_body.png'))

screen_size = 32 * width, 32 * height
screen = pygame.display.set_mode(screen_size)


# Colors
black = 0, 0, 0

# Keys
w = pygame.K_w
a = pygame.K_a
s = pygame.K_s
d = pygame.K_d
q = pygame.K_q


def apple_pos():
    global head_x, head_y, apple_x, apple_y
    x_positions = []
    for i in range((32 * width)):
        if i % 32 == 0:
            x_positions.append(i)
    y_positions = []
    for i in range((32 * height)):
        if i % 32 == 0:
            y_positions.append(i)
    while True:
        rand_x, rand_y = random.randint(0, len(x_positions) - 1), random.randint(0, len(y_positions) - 1)
        if x_positions[rand_x] != head_x and y_positions[rand_y] != head_y:
            apple_x, apple_y = x_positions[rand_x], y_positions[rand_y]
            return apple_x, apple_y


def opposite_direction():
    global direction
    direction = {'up':'down', 'down':'up', 'left':'right', 'right':'left'}[direction]


while True:
    head_x, head_y = 32 * width / 2, 32 * height / 2
    if head_x % 32 != 0:
        head_x -= head_x % 32
    if head_y % 32 != 0:
        head_y -= head_y % 32
        
    apple_x, apple_y = 0, 0

    apple_pos()

    direction = 'right'

    speed = 10 / initial_speed
    speed_cap = .1
    speed_rate = 10 / initial_speed_rate

    segments = 1

    all_positions = [(0, 100000)]

    game_loop = True
    while game_loop:
        all_positions.append((head_x, head_y))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == q:
                    print('Game quit')
                    pygame.quit()
                    game_loop = False
                elif event.key == a and direction != 'right':
                    direction = 'left'
                elif event.key == d and direction != 'left':
                    direction = 'right'
                elif event.key == w and direction != 'down':
                    direction = 'up'
                elif event.key == s and direction != 'up':
                    direction = 'down'

        if direction == 'up':
            head_y -= 32
        elif direction == 'down':
            head_y += 32
        elif direction == 'left':
            head_x -= 32
        elif direction == 'right':
            head_x += 32

        if head_x > 32 * (width - 1):
            head_x = 0
        if head_x < 0:
            head_x = 32 * (width - 1)
        if head_y > 32 * (height - 1):
            head_y = 0
        if head_y < 0:
            head_y = 32 * (height - 1)

        if not game_loop:
            break

        if head_x == apple_x and head_y == apple_y:
            apple_pos()
            speed -= speed_rate
            segments += 1
            if speed <= speed_cap:
                speed = speed_cap

        screen.fill(black)
        screen.blit(snake_head, (head_x, head_y))
        screen.blit(apple, (apple_x, apple_y))

        if segments > 0:
            for segment in range(segments):
                segment_pos = all_positions[-1 * segment]
                if segment_pos == (head_x, head_y):
                    if segment == 2:
                        if direction == 'left':
                            head_x += 32
                            opposite_direction()
                            pass
                        elif direction == 'right':
                            head_x -= 32
                            opposite_direction()
                            pass
                        elif direction == 'up':
                            head_y += 32
                            opposite_direction()
                            pass
                        elif direction == 'down':
                            head_y -= 32
                            opposite_direction()
                            pass
                    else:
                        print('You died!')
                        game_loop = False
                screen.blit(snake_body, segment_pos)

        pygame.display.flip()
        time.sleep(speed)
