import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()

# Configurações
WIDTH, HEIGHT = 400, 600
GROUND_HEIGHT = 100
SPEED = 5
GRAVITY = 0.4
JUMP_STRENGTH = 10

# Cores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Carrega imagens
bird_img = pygame.image.load("bird.png")
background_img = pygame.image.load("ground.png")
ground_img = pygame.image.load("background.png")

# Redimensiona imagens
bird_img = pygame.transform.scale(bird_img, (50, 50))
ground_img = pygame.transform.scale(ground_img, (WIDTH, GROUND_HEIGHT))

# Posição inicial
bird_x = 50
bird_y = (HEIGHT - GROUND_HEIGHT) // 2
bird_vel = 0

# Obstáculos
obstacles = []

# Pontuação
score = 0
game_over = False

# Função para criar um novo obstáculo
def create_obstacle():
    obstacle_height = random.randint(100, 300)
    obstacle = pygame.Rect(WIDTH, 0, 50, obstacle_height)
    bottom_obstacle = pygame.Rect(WIDTH, obstacle_height + 200, 50, HEIGHT - GROUND_HEIGHT - obstacle_height - 200)
    return obstacle, bottom_obstacle

# Função para reiniciar o jogo
def restart_game():
    global bird_y, bird_vel, obstacles, score, game_over
    bird_y = (HEIGHT - GROUND_HEIGHT) // 2
    bird_vel = 0
    obstacles = []
    score = 0
    game_over = False

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_vel = -JUMP_STRENGTH
            elif event.key == pygame.K_r and game_over:
                restart_game()

    if not game_over:
        bird_vel += GRAVITY
        bird_y += bird_vel

        if bird_y >= HEIGHT - GROUND_HEIGHT:
            bird_y = HEIGHT - GROUND_HEIGHT
            bird_vel = 0

        if len(obstacles) == 0 or obstacles[-1][0].x < WIDTH - 200:
            obstacles.append(create_obstacle())

        for i, obstacle in enumerate(obstacles):
            obstacle[0].x -= SPEED
            obstacle[1].x -= SPEED
            if obstacle[0].x < -50:
                obstacles.pop(i)
                score += 1

        for obstacle, bottom_obstacle in obstacles:
            if bird_x + 50 > obstacle.x and bird_x < obstacle.x + 50:
                if bird_y < obstacle.height or bird_y + 50 > bottom_obstacle.y:
                    game_over = True

    screen.fill(WHITE)
    screen.blit(background_img, (0, 0))
    screen.blit(ground_img, (0, HEIGHT - GROUND_HEIGHT))
    screen.blit(bird_img, (bird_x, bird_y))
    for obstacle, bottom_obstacle in obstacles:
        pygame.draw.rect(screen, BLUE, obstacle)
        pygame.draw.rect(screen, BLUE, bottom_obstacle)

    font = pygame.font.Font(None, 36)
    text = font.render("Pontuação: " + str(score), True, BLUE)
    screen.blit(text, (10, 10))

    if game_over:
        text = font.render("Você perdeu! Pontuação: " + str(score), True, BLUE)
        screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
        restart_text = font.render("Pressione 'R' para recomeçar", True, BLUE)
        screen.blit(restart_text, (WIDTH // 2 - 180, HEIGHT // 2 + 50))

    pygame.display.update()
    pygame.time.delay(30)

pygame.quit()
sys.exit()
