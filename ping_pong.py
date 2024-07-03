from turtle import right, width
import pygame
import random

pygame.init() #initilized the pygame

#screen dimensions

WIDTH, HEIGHT = 800,600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

# Player speeds
PADDLE_SPEED = 10
BALL_X_SPEED = 7
BALL_Y_SPEED = 7

# Define the Paddle class
class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, up=True):
        if up:
            self.y -= PADDLE_SPEED
        else:
            self.y += PADDLE_SPEED
        self.rect.y = self.y

    def draw(self, win):
        pygame.draw.rect(win, WHITE, self.rect)

# Define the Ball class
class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_vel = BALL_X_SPEED
        self.y_vel = BALL_Y_SPEED
        self.rect = pygame.Rect(x, y, BALL_RADIUS * 2, BALL_RADIUS * 2)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, win):
        pygame.draw.ellipse(win, WHITE, self.rect)

    def reset(self):
        self.x = WIDTH // 2 - BALL_RADIUS
        self.y = HEIGHT // 2 - BALL_RADIUS
        self.x_vel = BALL_X_SPEED * random.choice((-1, 1))
        self.y_vel = BALL_Y_SPEED * random.choice((-1, 1))
        self.rect.x = self.x
        self.rect.y = self.y

# Draw function
def draw(win, paddles, ball):
    win.fill(BLACK)
    for paddle in paddles:
        paddle.draw(win)
    ball.draw(win)
    pygame.display.update()

# Handle collision with paddles
def handle_collision(ball, paddles):
    if ball.y + BALL_RADIUS * 2 >= HEIGHT or ball.y <= 0:
        ball.y_vel *= -1

    for paddle in paddles:
        if ball.rect.colliderect(paddle.rect):
            ball.x_vel *= -1

# Main function
def main():
    run = True
    clock = pygame.time.Clock()

    # Initialize paddles and ball
    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS)
    paddles = [left_paddle, right_paddle]

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle.y - PADDLE_SPEED >= 0:
            left_paddle.move(up=True)
        if keys[pygame.K_s] and left_paddle.y + PADDLE_SPEED + PADDLE_HEIGHT <= HEIGHT:
            left_paddle.move(up=False)

        # AI Movement
        if right_paddle.y + PADDLE_HEIGHT / 2 < ball.y:
            right_paddle.move(up=False)
        elif right_paddle.y + PADDLE_HEIGHT / 2 > ball.y:
            right_paddle.move(up=True)

        ball.move()
        handle_collision(ball, paddles)

        if ball.x + BALL_RADIUS * 2 >= WIDTH or ball.x <= 0:
            ball.reset()

        draw(WIN, paddles, ball)

    pygame.quit()

if __name__ == "__main__":
    main()
 
 