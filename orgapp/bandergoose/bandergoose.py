import os
import random
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT
from pathlib import Path


HEIGHT = 700
WIDTH = 1200
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)
CURR_DIR = f'{Path(__file__).parent.resolve()}'
PLAYER_IMAGES = [f'{CURR_DIR}/1-{i}.png' for i in range(1, 6)]


def create_enemy():
    enemy = pygame.image.load(f'{CURR_DIR}/enemy.png').convert_alpha()
    enemy_size = (enemy.get_width(), enemy.get_height())
    enemy_rect = pygame.Rect(WIDTH, random.randint(enemy_size[1], HEIGHT-2*enemy_size[1]), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]


def create_bonus():
    bonus = pygame.image.load(f'{CURR_DIR}/bonus.png').convert_alpha()
    bonus_size = (bonus.get_width(), bonus.get_height())
    bonus_rect = pygame.Rect(random.randint(bonus_size[0], WIDTH-2*bonus_size[0]), -bonus_size[1], *bonus_size)
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]


def main():
    print('bi', end=' ')
    pygame.init()
    print('ai', end=' ')
    FONT = pygame.font.SysFont('Verdana', 25)
    GAME_OVER_FONT = pygame.font.SysFont('Verdana_bold', 200)
    print('af')
    main_display = pygame.display.set_mode((WIDTH, HEIGHT))
    bg_image = pygame.image.load(f'{CURR_DIR}/background.png')
    bg = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
    bg_x1, bg_x2 = 0, bg.get_width()
    bg_move = 3

    player = pygame.image.load(f'{CURR_DIR}/player.png').convert_alpha()
    player_size = (player.get_width(), player.get_height())
    player_rect = pygame.Rect(0, (HEIGHT - player_size[1]) // 2, *player_size)
    player_move_down = [0, 5]
    player_move_right = [5, 0]
    player_move_up = [0, -5]
    player_move_left = [-5, 0]

    CREATE_ENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(CREATE_ENEMY, 2500)
    CREATE_BONUS = pygame.USEREVENT + 2
    pygame.time.set_timer(CREATE_BONUS, 4000)
    CHANGE_IMAGE = pygame.USEREVENT + 3
    pygame.time.set_timer(CHANGE_IMAGE, 150)

    enemies = []
    bonuses = []
    playing = True
    quit_game = False
    score = 0
    image_index = 0

    while playing:
        FPS = pygame.time.Clock()
        FPS.tick(150)

        for event in pygame.event.get():
            if event.type == QUIT:
                playing = False
                quit_game = True
            if event.type == CREATE_ENEMY:
                enemies.append(create_enemy())
            if event.type == CREATE_BONUS:
                bonuses.append(create_bonus())
            if event.type == CHANGE_IMAGE:
                player = pygame.image.load(os.path.join(PLAYER_IMAGES[image_index]))
                image_index += 1
                if image_index >= len(PLAYER_IMAGES):
                    image_index = 0

        bg_x1 -= bg_move
        bg_x2 -= bg_move
        if bg_x1 < -bg.get_width():
            bg_x1, bg_x2 = bg_x2, bg_x2 + bg.get_width()
        main_display.blit(bg, (bg_x1, 0))
        main_display.blit(bg, (bg_x2, 0))
        main_display.blit(player, player_rect)

        keys = pygame.key.get_pressed()

        if keys[K_DOWN] and player_rect.bottom < HEIGHT:
            player_rect = player_rect.move(player_move_down)

        if keys[K_RIGHT] and player_rect.right < WIDTH:
            player_rect = player_rect.move(player_move_right)

        if keys[K_UP] and player_rect.top > 0:
            player_rect = player_rect.move(player_move_up)

        if keys[K_LEFT] and player_rect.left > 0:
            player_rect = player_rect.move(player_move_left)

        for enemy in enemies:
            enemy[1] = enemy[1].move(enemy[2])
            if player_rect.colliderect(enemy[1]):
                playing = False
                explosion = pygame.image.load(f'{CURR_DIR}/explosion.png').convert_alpha()
                enemy[1] = enemy[1].move(-150,-150)
                main_display.blit(explosion, enemy[1])
            else:
                main_display.blit(enemy[0], enemy[1])

        for bonus in bonuses:
            bonus[1] = bonus[1].move(bonus[2])
            main_display.blit(bonus[0], bonus[1])
            if player_rect.colliderect(bonus[1]):
                score += 1
                bonuses.pop(bonuses.index(bonus))
        main_display.blit(FONT.render(f'Рахунок: {score}', True, COLOR_BLACK), (WIDTH-150, 20))
        pygame.display.flip()

        for enemy in enemies:
            if enemy[1].right < 0:
                enemies.pop(enemies.index(enemy))

        for bonus in bonuses:
            if bonus[1].top > HEIGHT:
                bonuses.pop(bonuses.index(bonus))

    while not quit_game:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game = True
        main_display.blit(GAME_OVER_FONT.render('GAME OVER', True, COLOR_RED), (200, 300))
        pygame.display.flip()


if __name__ == '__main__':
    main()
