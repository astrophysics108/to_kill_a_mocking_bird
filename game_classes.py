import pygame
import random
pygame.mixer.init()
# Constants
WIDTH, HEIGHT = 800, 400
GROUND_HEIGHT = 80
PLAYER_JUMP = -12
RED = (255, 0, 0)
jump_sfx = pygame.mixer.Sound(r"Games\sfx\mixkit-player-jumping-in-a-video-game-2043.wav") 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img_path = r"C:\\Users\dsingh\OneDrive - The Perse School\python_2024-25\Games\4ffc7133-7f18-46cc-9c53-4f72c175d226-Recovered.png"
        self.image = pygame.image.load(img_path)
        self.image = pygame.transform.scale(self.image, (50, int(50 * (799/517))))
        self.rect = self.image.get_rect(midbottom=(100, HEIGHT - GROUND_HEIGHT))
        self.vel_y, self.on_ground = 0, True

    def update(self, keys,gravity):
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = PLAYER_JUMP
            jump_sfx.play()
            self.on_ground = False

        self.vel_y += gravity
        self.rect.y += self.vel_y

        if self.rect.bottom >= HEIGHT - GROUND_HEIGHT:
            self.rect.bottom = HEIGHT - GROUND_HEIGHT
            self.vel_y, self.on_ground = 0, True

    def reset_position(self):
        self.rect.midbottom = (100, HEIGHT - GROUND_HEIGHT)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, width, height, img=None):
        super().__init__()
        self.image = pygame.image.load(img) if img else pygame.Surface((width, height))
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, HEIGHT - GROUND_HEIGHT - height))
        self.scored = False 
    def update(self, obstacle_speed, fast=False):
        self.rect.x -= obstacle_speed

        if self.rect.right < 0:
            if not fast:
                self.rect.left = WIDTH + 300
            else:
                self.rect.left = WIDTH + 2000 + int(random.randint(0,8000))
            self.scored = False  


class Background(pygame.sprite.Sprite):
    def __init__(self, img_path, x,y,width=None, height=None):
        super().__init__()
        try:
            self.image = pygame.image.load(img_path)
        except TypeError:
            self.image = img_path
        if type(width) == int:
            self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(midbottom=(x, y))
    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect.topleft)

class Button:
    def __init__(self, x, y, width, height, img=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(img) if img else None
        if self.image:
            self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect.topleft)

    def was_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)
