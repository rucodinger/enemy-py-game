import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Игровая стрелялка')

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#enemies
enemy_size = 40
enemy_speed = 5
enemies = []

# Загрузка изображения персонажа
player_image_right = pygame.image.load('player.png')
player_image_right = pygame.transform.scale(player_image_right, (175, 130))  # Масштабируем

# Создаём зеркальное изображение для направления влево
player_image_left = pygame.transform.flip(player_image_right, True, False)

# Начальное направление персонажа — вправо
facing_right = True
player_image = player_image_right

player_rect = player_image.get_rect(center=(WIDTH // 2, 500))

# Функция для создания нового врага
def create_enemy():
    enemy_x = random.randint(0, WIDTH - enemy_size)
    direction = random.choice(['down', 'd-left', 'd-right'])
    enemies.append([enemy_x, 1, direction])
    print(direction)

# Параметры пуль
bullets = []
bullet_speed = 10

# Звук выстрела
bullet_sound = pygame.mixer.Sound('bullet.mp3')

# Основной игровой цикл
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Стрельба при нажатии пробела
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                # Пули летят вверх, не зависимо от направления персонажа
                bullet_rect = pygame.Rect(player_rect.centerx, player_rect.top, 5, 10)
                # Загрузка изображения персонажа
                bullet_image = pygame.image.load('bullet.png')
                bullet_image = pygame.transform.scale(bullet_image, (14.83, 90.66))  # Масштабируем
                bullets.append([bullet_image, bullet_rect])
                bullet_sound.play()

    # Перемещение персонажа и смена направления
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player_rect.left > 0:
        player_rect.x -= 5
        if facing_right:
            facing_right = False
            player_image = player_image_left
    if keys[pygame.K_d] and player_rect.right < WIDTH:
        player_rect.x += 5
        if not facing_right:
            facing_right = True
            player_image = player_image_right

    ###############
    # Создание врагов (с интервалом)
    if random.random() < 0.015:  # Шанс появления врага
        create_enemy()

    # Обновление позиции врагов
        c = 0

    # движение
    for i, enemy in enumerate(enemies):
        if enemy[2] == 'down':
             enemy[1] += enemy_speed
        elif enemy[2] == 'd-right':
            enemy[0] += enemy_speed
            enemy[1] += enemy_speed
        elif enemy[2] == 'd-left':
            enemy[0] -= enemy_speed
            enemy[1] += enemy_speed

    # отскок
    for i, enemy in enumerate(enemies):
        if enemy[0] <= 0 and enemy[2] == 'd-left':
            enemy[2] = 'd-right'
        elif enemy[0] >= WIDTH and enemy[2] == 'd-right':
            enemy[2] = 'd-left'

    # Удаление врагов, ушедших за экран
    for i in reversed(range(len(enemies))):  # Итерируемся в обратном порядке, чтобы правильно удалять элементы
        if enemies[i][1] > HEIGHT:
            del enemies[i]

    # Проверка столкновения с игроком
    # player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    for i in reversed(range(len(enemies))):
        enemy_rect = pygame.Rect(enemies[i][0], enemies[i][1], enemy_size, enemy_size)
        for i in reversed(range(len(bullets))):
            if bullets[i][1].colliderect(enemy_rect):
                print("collision")
                del bullets[i]
                del enemies[i]
                break  # Выходим из цикла, т.к. столкновение уже зафиксировано
    ###############################

    # Обновление позиции пуль
    for bullet in bullets[:]:
        bullet[1].y -= bullet_speed
        if bullet[1].bottom < 0:
            bullets.remove(bullet)

    # Отображение на экране
    screen.fill(WHITE)
    screen.blit(player_image, player_rect)
    for enemy in enemies:
        pygame.draw.rect(screen, (255,0,0), (enemy[0], enemy[1], enemy_size, enemy_size))
    for bullet in bullets:
        # pygame.draw.rect(screen, BLACK, bullet)
        screen.blit(bullet[0], bullet[1])

    pygame.display.flip()
    clock.tick(60)

# Завершение Pygame
pygame.quit()
sys.exit()