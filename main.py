import os
import pickle
import sys

import pygame

if not os.path.isfile("classes/savefile.dat"):
    with open("classes/savefile.dat", "wb") as f:
        pickle.dump(0, f)

if not os.path.isfile("classes/user.dat"):
    initial_data = {"click_reward": 1, "click_variance": 1}
    with open("classes/user.dat", "wb") as f:
        pickle.dump(initial_data, f)


pygame.init()

WIDTH, HEIGHT = 400, 600
BLACK = (0, 0, 0)
DARK_GREEN = (0, 100, 0)
LIGHT_GREEN = (144, 238, 144)

with open("classes/savefile.dat", "rb") as f:
    clover_count = pickle.load(f)
with open("classes/user.dat", "rb") as uf:
    data = pickle.load(uf)
    frst = int(10 * data['click_reward'])
    scnd = int(10 * data["click_variance"])
    upgrade_prices = [frst, scnd]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FortunaClicker")

clock = pygame.time.Clock()

button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)
button_pressed = False


def save_clovers(count):
    with open("classes/savefile.dat", "wb") as file:
        pickle.dump(count, file)


def draw_background():
    for y in range(HEIGHT):
        shade = int(255 - (y / HEIGHT) * 255)
        color = (shade, shade, shade)
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))


def draw_ui():
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 50))
    font = pygame.font.Font(None, 36)
    text = font.render(f"Обед", True, LIGHT_GREEN)
    text_rect = text.get_rect(center=(WIDTH // 2, 25))
    screen.blit(text, text_rect)

    pygame.draw.rect(screen, BLACK, (0, HEIGHT - 100, WIDTH, 100))
    pygame.draw.rect(screen, DARK_GREEN, button_rect.inflate(-5, -5) if button_pressed else button_rect)
    pygame.draw.rect(screen, LIGHT_GREEN, button_rect.inflate(-5, -5) if button_pressed else button_rect, 3)


def draw_header(offset):
    header_rect = pygame.Rect(0, 0, WIDTH, 50)
    header_gradient = pygame.Surface((WIDTH, 50))
    header_gradient.fill((0, 0, 0))
    for x in range(WIDTH):
        shade = int(255 - ((x + offset) / WIDTH) * 255)
        color = (shade, shade, shade)
        pygame.draw.line(header_gradient, shade, (x, 0), (x, 50))
    screen.blit(header_gradient, (0, 0))
    font = pygame.font.Font(None, 36)
    text = font.render(f"FortunaClicker | {clover_count}", True, LIGHT_GREEN)
    text_rect = text.get_rect(center=(WIDTH // 2, 25))
    screen.blit(text, text_rect)


def draw_bottom(offset):
    bottom_rect = pygame.Rect(0, HEIGHT - 200, WIDTH, 200)
    bottom_gradient = pygame.Surface((WIDTH, 200))
    bottom_gradient.fill((0, 0, 0))
    with open("classes/user.dat", "rb") as f:
        data = pickle.load(f)
    for x in range(WIDTH):
        shade = int(255 - ((x + offset) / WIDTH) * 255)
        color = (shade, shade, shade)
        pygame.draw.line(bottom_gradient, shade, (x, 0), (x, 50))
    screen.blit(bottom_gradient, (0, HEIGHT - 200))
    upgrade_font = pygame.font.Font(None, 24)
    upgrade_texts = [
        f"Увеличить награду за клик ({data['click_reward']} / {int(10 * data['click_reward'])})",
        f"Увеличить разброс кликов ({data['click_variance']} / {10 * data['click_variance']} )"
    ]
    for obed, text in enumerate(upgrade_texts):
        upgrg_rct = pygame.Rect(50, HEIGHT - 150 + obed * 50, 300, 40)
        pygame.draw.rect(screen, DARK_GREEN, upgrg_rct)
        pygame.draw.rect(screen, LIGHT_GREEN, upgrg_rct, 3)
        upgrade_text = upgrade_font.render(text, True, LIGHT_GREEN)
        upgrade_text_rect = upgrade_text.get_rect(center=(250, HEIGHT - 130 + obed * 50))
        screen.blit(upgrade_text, upgrade_text_rect)


def draw_game(offset):
    draw_background()
    draw_ui()
    draw_header(offset)
    draw_bottom(offset)
    pygame.display.flip()


def buy_upgrade(index):
    global clover_count, upgrade_prices
    print(clover_count, upgrade_prices[index])
    if clover_count >= upgrade_prices[index]:
        clover_count -= upgrade_prices[index]
        save_clovers(clover_count)
        try:
            with open("classes/user.dat", "rb") as dat:
                udata = pickle.load(dat)
        except FileNotFoundError:
            udata = {"click_reward": 1}
        if index == 0:
            udata["click_reward"] += 1
            upgrade_prices[0] *= 2
        elif index == 1:
            udata["click_variance"] += 1
            upgrade_prices[1] *= 2
        with open("classes/user.dat", "wb") as dat:
            pickle.dump(udata, dat)


running = True
offset = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            try:
                with open("classes/user.dat", "rb") as f:
                    user_data = pickle.load(f)
            except FileNotFoundError:
                user_data = {"click_reward": 1}
            if button_rect.collidepoint(event.pos):
                button_pressed = True
                clover_count += int(user_data['click_reward'])
                save_clovers(clover_count)
            for i in range(len(upgrade_prices)):
                upgrade_rect = pygame.Rect(50, HEIGHT - 150 + i * 50, 300, 40)
                if upgrade_rect.collidepoint(event.pos):
                    buy_upgrade(i)
        elif event.type == pygame.MOUSEBUTTONUP:
            button_pressed = False

    draw_game(offset)
    offset += 1
    offset %= WIDTH
    clock.tick(60)

pygame.quit()
sys.exit()
