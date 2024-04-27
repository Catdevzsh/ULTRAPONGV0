import pygame
from array import array
import time

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Set screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("ULTRAPONG M1 MAC PORT @FlamesLLC [C] 20XX")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)

# Paddle dimensions
paddle_width = 10
paddle_height = 60

# Ball dimensions
ball_size = 10

# Paddle positions
player1_y = height // 2 - paddle_height // 2
player2_y = height // 2 - paddle_height // 2

# Ball position and velocity
ball_x = width // 2
ball_y = height // 2
ball_dx = 3
ball_dy = 3

# Scores
player1_score = 0
player2_score = 0

# Font for displaying scores
font = pygame.font.Font(None, 36)

# Clock object for controlling frame rate
clock = pygame.time.Clock()

# Sound generation function
def generate_beep_sound(frequency, duration):
    sample_rate = pygame.mixer.get_init()[0]
    max_amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    samples = int(sample_rate * duration)
    wave = [int(max_amplitude * ((i // (sample_rate // frequency)) % 2)) for i in range(samples)]
    sound = pygame.mixer.Sound(buffer=array('h', wave))
    sound.set_volume(0.1)
    return sound

paddle_hit_sound = generate_beep_sound(880, 0.05)
score_sound = generate_beep_sound(220, 0.2)

# Loading progress bar variables
loading_progress = 0
loading_bar_width = 400
loading_bar_height = 20
loading_bar_x = width // 2 - loading_bar_width // 2
loading_bar_y = height // 2 - loading_bar_height // 2

# Loading screen loop
while loading_progress < 100:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    loading_progress += 1
    time.sleep(0.01)

    screen.fill(black)
    pygame.draw.rect(screen, gray, (loading_bar_x, loading_bar_y, loading_bar_width, loading_bar_height))
    pygame.draw.rect(screen, white, (loading_bar_x, loading_bar_y, int(loading_progress / 100 * loading_bar_width), loading_bar_height))
    pygame.display.flip()

# Game loop
def game_loop():
    global player1_score, player2_score, ball_x, ball_y, ball_dx, ball_dy, player1_y, player2_y
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player1_y -= 5
        if keys[pygame.K_s]:
            player1_y += 5
        if player2_y + paddle_height // 2 < ball_y:
            player2_y += 5
        elif player2_y + paddle_height // 2 > ball_y:
            player2_y -= 5
        player1_y = max(0, min(player1_y, height - paddle_height))
        player2_y = max(0, min(player2_y, height - paddle_height))
        ball_x += ball_dx
        ball_y += ball_dy
        if ball_y <= 0 or ball_y >= height - ball_size:
            ball_dy *= -1
            paddle_hit_sound.play()
        if (ball_x <= paddle_width and player1_y <= ball_y <= player1_y + paddle_height) or (ball_x >= width - paddle_width - ball_size and player2_y <= ball_y <= player2_y + paddle_height):
            ball_dx *= -1
            paddle_hit_sound.play()
        if ball_x < 0:
            player2_score += 1
            ball_x, ball_y = width // 2, height // 2
            ball_dx, ball_dy = -3, 3
            score_sound.play()
        if ball_x > width:
            player1_score += 1
            ball_x, ball_y = width // 2, height // 2
            ball_dx, ball_dy = -3, 3
            score_sound.play()
        screen.fill(black)
        pygame.draw.rect(screen, white, (0, player1_y, paddle_width, paddle_height))
        pygame.draw.rect(screen, white, (width - paddle_width, player2_y, paddle_width, paddle_height))
        pygame.draw.circle(screen, white, (ball_x, ball_y), ball_size)
        pygame.draw.line(screen, white, (width // 2, 0), (width // 2, height), 2)
        player1_score_text = font.render(str(player1_score), True, white)
        player2_score_text = font.render(str(player2_score), True, white)
        screen.blit(player1_score_text, (width * 0.25, 50))
        screen.blit(player2_score_text, (width * 0.75, 50))
        pygame.display.flip()
        if player1_score >= 5 or player2_score >= 5:
            if player1_score >= 5:
                display_winner("YOU WON! Restart? (Y/N)")
            else:
                display_winner("YOU LOST! Restart? (Y/N)")
            running = False

def display_winner(message):
    global player1_score, player2_score
    while True:
        screen.fill(black)
        message_text = font.render(message, True, white)
        screen.blit(message_text, (width // 2 - message_text.get_width() // 2, height // 2 - 20))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    player1_score, player2_score = 0, 0
                    game_loop()
                    return
                elif event.key == pygame.K_n:
                    pygame.quit()
                    exit()

game_loop()
