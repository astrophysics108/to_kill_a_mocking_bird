import pygame
from game_classes import *
import time

# Constants
pygame.mixer.init()
BLUE = (0, 0, 255)

WIDTH, HEIGHT = 800, 400
PLAYER_JUMP = -12
PLAYER_SPEED = 5
obstacle_speed = 5
gravity = obstacle_speed / 10
max_speed = 10
GROUND_HEIGHT = 80
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (5, 5, 5)
inventory = {}
obtain_sfx = pygame.mixer.Sound("sfx/rupee-collect.mp3")
lives = 10
money = 0
shop_items = {
    "1life.png": 20,
    "3lives.png": 35,
    "5lives.png": 55,
    "10lives.png": 100
}

def get_money(num, screen):
    global money
    money += num
    popup(f"You have just gained\n {num} coins!", screen)
    print(money)

def popup(text, screen):
    popup = Background(load_scaled_image("notif.png", 300, 300), WIDTH // 2, HEIGHT // 1.5)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    open_inventory(screen)
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_s:
                    open_shop(money, screen)
        popup.draw(screen)
        draw_text(
            text,
            (WIDTH // 2, HEIGHT // 2.3),
            pygame.font.Font(None, 30),
            screen,
            color=BLACK,
            mid=(len(text.splitlines())) / 2 if len(text.splitlines()) % 2 == 0 else (len(text.splitlines()) - 1) / 2
        )
        pygame.display.flip()

def houses(score, screen):
    global lives
    x = -1
    if score == 25:
        x = 0
        pygame.mixer.music.pause()
        if popup_house("Miss Maudie's House", screen):
            lines = [
                "missmaudie/pixel-speech-bubble (1).png",
                "missmaudie/pixel-speech-bubble (2).png",
                "missmaudie/pixel-speech-bubble (3).png",
                "missmaudie/pixel-speech-bubble.png",
                "missmaudie/pixel-speech-bubble (8).png"
            ]
            if "Mushroom for Miss Maudie" in inventory:
                lines.pop(4)
                del inventory["Mushroom for Miss Maudie"]
                x = 5
            else:
                lines.pop(3)
            run_voice_basic(
                inventory,
                lines,
                WIDTH // 3.5,
                HEIGHT // 3.5,
                "missmaudie.png",
                screen,
                max_width=300,
                max_height=300,
                voice=True
            )
        pygame.mixer.music.load("sfx/mainrunning.mp3")
        pygame.mixer.music.play()
        return x
    if score == 50:
        x = 0
        if popup_house("The Radley House", screen):
            pygame.mixer.music.pause()
            cutscene("radleyhouse.png", "sfx/mixkit-crickets-at-night-in-nature-2475.wav", 5, screen)
            popup("You have found a little\n pouch of coins in\n a tree nook", screen)
            get_money(50, screen)
            pygame.mixer.music.unpause()
        return x
    return x

def cutscene(image, sfx, t, screen):
    img = Background(load_scaled_image(image, WIDTH * 10000, HEIGHT), WIDTH // 2, HEIGHT)
    sfx = pygame.mixer.Sound(sfx)
    sfx.play()
    tx = time.time()
    while True:
        nx = time.time() - tx
        if nx >= t:
            sfx.stop()
            return
        img.draw(screen)
        pygame.display.flip()

def popup_house(text, screen):
    popup = Background(load_scaled_image("popup.png", 300, 300), WIDTH // 2, HEIGHT // 1.5)
    c = 591 / 130
    yes = Button(WIDTH // 15, HEIGHT // 1.5, c * 50, 50, img="yes.png")
    no = Button(WIDTH // 1.5, HEIGHT // 1.5, c * 50, 50, img="no.png")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    open_inventory(screen)
                if event.key == pygame.K_s:
                    open_shop(money, screen)
            if yes.was_clicked(event):
                return True
            if no.was_clicked(event):
                return False
        popup.draw(screen)
        yes.draw(screen)
        no.draw(screen)
        draw_text(
            text,
            (WIDTH // 2, HEIGHT // 2.3),
            pygame.font.Font(None, 30),
            screen,
            color=BLACK,
            mid=(len(text.splitlines())) / 2 if len(text.splitlines()) % 2 == 0 else (len(text.splitlines()) - 1) / 2
        )
        pygame.display.flip()

def open_inventory(screen):
    invent = Background(load_scaled_image("invent2.png", 300, 300), WIDTH // 2, HEIGHT // 1.2)
    W_MARGIN = 100
    H_MARGIN = 100
    els = []
    for i, el in enumerate(inventory.values()):
        els.append(Background(load_scaled_image(el, 30, 30), WIDTH // 2.3 + W_MARGIN * (i % 4), HEIGHT // 2.55 + H_MARGIN * (i // 4)))
    while True:
        invent.draw(screen)
        [el.draw(screen) for el in els]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    return
                if event.key == pygame.K_s:
                    popup("Cannot open shop\n at this moment", screen)
        pygame.display.flip()

def open_shop(coins, screen):
    shop = Background(load_scaled_image("shop.png", 300, 300), WIDTH // 2, HEIGHT // 1.2)
    W_MARGIN = 70
    H_MARGIN = 70
    els = []
    for i, el in enumerate(shop_items.keys()):
        els.append(Button(WIDTH // 2.4 - 20 + W_MARGIN * (i % 3), HEIGHT // 2.55 - 20 + H_MARGIN * (i // 3), 50, 50, img=el))
    while True:
        shop.draw(screen)
        draw_text(str(coins), (WIDTH // 1.75, HEIGHT // 1.45), pygame.font.Font(None, 40), screen, color=BLACK)
        [el.draw(screen) for el in els]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return
                if event.key == pygame.K_w:
                    popup("Cannot open inventory\n at this moment", screen)
        pygame.display.flip()

def draw_text(text, position, font, screen, color=BLUE, move=True, mid=0):
    y = 32
    text = text.splitlines()
    for i, t in enumerate(text):
        text_surface = font.render(t, True, color)
        screen.blit(text_surface, (int(position[0] - (WIDTH * len(t)) / 160) if move else position[0], position[1] + (int(i - mid) * y)))

def load_scaled_image(image_path, max_w, max_h):
    image = pygame.image.load(image_path)
    original_w, original_h = image.get_size()
    scale_factor = min(max_w / original_w, max_h / original_h)
    new_w, new_h = int(original_w * scale_factor), int(original_h * scale_factor)
    return pygame.transform.scale(image, (new_w, new_h))

def add_to_inventory(obj, description, screen):
    invent = Background(load_scaled_image("shop.png", 300, 300), WIDTH // 2, HEIGHT // 1.2)
    obj = Background(load_scaled_image(obj, 100, 100), WIDTH // 2, HEIGHT // 1.5)
    r = True
    obtain_sfx.play()
    while r:
        invent.draw(screen)
        obj.draw(screen)
        draw_text(description, (WIDTH // 2 - (WIDTH * len(description) // 180), HEIGHT // 3.25), pygame.font.Font(None, 23), screen, color=BLACK, mid=False, move=False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return 1
                if event.key == pygame.K_w:
                    open_inventory(screen)
                if event.key == pygame.K_s:
                    open_shop(money, screen)
        pygame.display.flip()

def pose_question(line, bg, screen, x, y, invent=None):
    c = 591 / 130
    yes = Button(WIDTH // 15, HEIGHT // 1.5, c * 50, 50, img="yes.png")
    no = Button(WIDTH // 1.5, HEIGHT // 1.5, c * 50, 50, img="no.png")
    speech_rect = line.get_rect(center=(x, y))
    while True:
        screen.fill(WHITE)
        bg.draw(screen)
        screen.blit(line, speech_rect.topleft)
        yes.draw(screen)
        no.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    open_inventory(screen)
                if event.key == pygame.K_s:
                    open_shop(money, screen)
            if yes.was_clicked(event):
                if invent:
                    inventory[invent[0]] = invent[1]
                    print(inventory)
                    if add_to_inventory(invent[1], invent[0], screen) == -1:
                        return False
                return True
            elif no.was_clicked(event):
                return False
        pygame.display.flip()

def run_voice_basic(
    inventory,
    lines,
    x,
    y,
    bg_path,
    screen,
    max_width=WIDTH // 2,
    max_height=HEIGHT // 3,
    question_indexes=[],
    invent=None,
    voice=False
):
    bg = Background(bg_path, WIDTH // 2, HEIGHT, width=WIDTH, height=HEIGHT)
    ind = 0
    speech_bubble = load_scaled_image(lines[ind], max_width, max_height)
    speech_rect = speech_bubble.get_rect(center=(x, y))
    pygame.mixer.music.load("sfx/talking.mp3")
    running = True
    if voice:
        pygame.mixer.music.play(-1)
    while running:
        if ind in question_indexes:
            pygame.mixer.music.pause()
            if pose_question(speech_bubble, bg, screen, x, y, invent=[invent[0], invent[1]] if invent is not None else None):
                ind += 1
                speech_bubble = load_scaled_image(lines[ind], max_width, max_height)
                speech_rect = speech_bubble.get_rect(center=(x, y))
                del lines[ind + 1]
            else:
                ind += 2
                speech_bubble = load_scaled_image(lines[ind], max_width, max_height)
                speech_rect = speech_bubble.get_rect(center=(x, y))
            pygame.mixer.music.unpause()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return -1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                ind += 1
                if ind >= len(lines):
                    pygame.mixer.music.stop()
                    return 1
                speech_bubble = load_scaled_image(lines[ind], max_width, max_height)
                speech_rect = speech_bubble.get_rect(center=(x, y))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    pygame.mixer.music.pause()
                    open_inventory(screen)
                    pygame.mixer.music.unpause()
                if event.key == pygame.K_s:
                    pygame.mixer.music.pause()
                    open_shop(money, screen)
                    pygame.mixer.music.unpause()
        screen.fill(WHITE)
        bg.draw(screen)
        screen.blit(speech_bubble, speech_rect.topleft)
        pygame.display.flip()

def render_bg(all_sprites, day=True):
    sky_img = "day_sky.png" if day else "night_sky.png"
    all_sprites.add(
        Background("grass.png", WIDTH / 2, HEIGHT, width=WIDTH, height=GROUND_HEIGHT),
        Background(sky_img, WIDTH / 2, HEIGHT - GROUND_HEIGHT, width=WIDTH, height=HEIGHT - GROUND_HEIGHT)
    )

def start_screen(screen):
    all_sprites = pygame.sprite.Group()
    background = Background("startscreen.png", WIDTH // 2, HEIGHT, width=WIDTH, height=HEIGHT)
    all_sprites.add(background)
    button = Button(WIDTH // 2 - (WIDTH // 10), HEIGHT // 2 + (HEIGHT // 10), 100, 50, img="start.png")
    running = True
    while running:
        screen.fill(WHITE)
        all_sprites.draw(screen)
        button.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            if button.was_clicked(event):
                lines = [
                    "tutorial/1.png",
                    "tutorial/2.png",
                    "tutorial/3.png",
                    "tutorial/4.png",
                    "tutorial/5.png",
                    "tutorial/6.png",
                    "tutorial/7.png",
                    "tutorial/8.png"
                ]
                run_voice_basic(inventory, lines, WIDTH // 2, HEIGHT // 2, "tutorial/1.png", screen, max_width=WIDTH, max_height=HEIGHT)
                return 1
        pygame.display.flip()

def game_over(screen, all_sprites):
    all_sprites.empty()
    all_sprites.add(Background("gameover.png", WIDTH / 2, HEIGHT, width=WIDTH, height=HEIGHT))
    while True:
        screen.fill(WHITE)
        all_sprites.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1