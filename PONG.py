import pygame
import random
import math
import os

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG")

WHITE = (255,255,255)
SKY_BLUE = (173, 216, 230)
GRAY = (105,105,105)
BLACK = (0,0,0)

TEXT_FONT = pygame.font.SysFont('roboto', 40)

STRIKER_WIDTH, STRIKER_HEIGHT = 10,60
STRIKER_MARGIN = 20
BALL_RADIUS = 5

VELOCITY = 7 # no. of pixels striker moves once the key is pressed
BALL_VEL = 5

FPS = 60

LEFT_POINT = 0
RIGHT_POINT = 0

Point_Sound = pygame.mixer.Sound(os.path.join('Assets', 'Point.mp3'))
Striker_Collision_Sound = pygame.mixer.Sound(os.path.join('Assets', 'Striker_Collision.wav'))
Top_Bottom_Collision_Sound = pygame.mixer.Sound(os.path.join('Assets', 'Top_Bottom_Collision.wav'))


x_dir,y_dir=0,0


# coordinate system starts from top left
# increasing x -> move right ; increasing y -> move down
def update_window(left_striker, right_striker, ball):
    WIN.fill(GRAY)
    pygame.draw.rect(WIN, WHITE, [left_striker.x, left_striker.y, STRIKER_WIDTH, STRIKER_HEIGHT], 0)
    pygame.draw.rect(WIN, WHITE, [right_striker.x, right_striker.y, STRIKER_WIDTH, STRIKER_HEIGHT], 0)
    pygame.draw.circle(WIN, BLACK, [ball.x, ball.y], BALL_RADIUS, 0)

    left_point_text = TEXT_FONT.render("LEFT : " + str(LEFT_POINT), 1, SKY_BLUE)
    right_point_text = TEXT_FONT.render("RIGHT : " + str(RIGHT_POINT), 1, SKY_BLUE)
    WIN.blit(left_point_text, ((WIDTH/2 - left_point_text.get_width())/2, 10))
    WIN.blit(right_point_text, ((3*WIDTH/2 - right_point_text.get_width())/2, 10))

    pygame.display.update()

def striker_movement(keys_pressed, left_striker, right_striker): # both strikers' movements are executed here
    if keys_pressed[pygame.K_w] and left_striker.y - VELOCITY > 0: # UP for left striker
        left_striker.y -= VELOCITY
    if keys_pressed[pygame.K_s] and left_striker.y + VELOCITY < HEIGHT - STRIKER_HEIGHT: # DOWN for left striker
        left_striker.y += VELOCITY
    if keys_pressed[pygame.K_UP] and right_striker.y - VELOCITY > 0: # UP for right striker
        right_striker.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and right_striker.y + VELOCITY < HEIGHT - STRIKER_HEIGHT: # DOWN for right striker
        right_striker.y += VELOCITY

def ball_start():
    global x_dir, y_dir
    # x and y components of unit velocity vector
    x_dir = random.choice([0.7,0.75, 0.8, 0.85, 0.9, 0.95]) * random.choice([-1,1]) # float between 0 and 1, positive x-direction
    y_dir = math.sqrt(1-(x_dir**2)) * random.choice([-1,1]) # positive y direction

def ball_restart(ball):

    ball.x = WIDTH/2
    ball.y = HEIGHT/2
    pygame.time.wait(1000)
    ball_start()

def ball_movement(ball, left_striker, right_striker):
    global x_dir, y_dir, RIGHT_POINT, LEFT_POINT

    ball.x += x_dir * BALL_VEL
    ball.y += y_dir * BALL_VEL

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        y_dir *= -1
        Top_Bottom_Collision_Sound.play()

    if ball.colliderect(left_striker) or ball.colliderect(right_striker):
        x_dir *= -1
        Striker_Collision_Sound.play()

    if ball.left <= -50:
        RIGHT_POINT += 1
        Point_Sound.play()
        ball_restart(ball)
    if ball.right >= WIDTH+50:
        LEFT_POINT += 1
        Point_Sound.play()
        ball_restart(ball)



def main():
    left_striker = pygame.Rect(STRIKER_MARGIN-(STRIKER_WIDTH)/2, (HEIGHT-STRIKER_HEIGHT)/2, STRIKER_WIDTH, STRIKER_HEIGHT)
    # normalising striker position according to screen size constants
    right_striker = pygame.Rect(WIDTH-(STRIKER_MARGIN+STRIKER_WIDTH/2), (HEIGHT-STRIKER_HEIGHT)/2, STRIKER_WIDTH, STRIKER_HEIGHT)
    # such that strikers appear symmetrical from center and even distance from sides

    ball = pygame.Rect(WIDTH/2, HEIGHT/2, BALL_RADIUS*2, BALL_RADIUS*2)
    # boundary rectangle for ball to detect collisions 
    ball_start()

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys_pressed = pygame.key.get_pressed()
        striker_movement(keys_pressed, left_striker, right_striker)
        ball_movement(ball, left_striker, right_striker)

        update_window(left_striker, right_striker, ball)

    pygame.quit()

if __name__ == "__main__":
    main()