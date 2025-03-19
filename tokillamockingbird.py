import pygame
import time
from game_classes import *
from game_functions import *
import threading

print("Loading...")
pygame.init()
pygame.mixer.init()

# Pygame Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("To Kill A Mockingbird")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Main Game
def main():
    global gravity, obstacle_speed,lives,score
    running = start_screen(screen) != -1
    lines = [r"C:\Users\dsingh\OneDrive - The Perse School\python_2024-25\Games\atticus\spacetoadvance.png",r"C:\\Users\dsingh\OneDrive - The Perse School\python_2024-25\Games\atticus\pixel-speech-bubble.png",r"C:\\Users\dsingh\OneDrive - The Perse School\python_2024-25\Games\atticus\pixel-speech-bubble (1).png", r"C:\\Users\dsingh\OneDrive - The Perse School\python_2024-25\Games\atticus\pixel-speech-bubble (2).png",r"C:\Users\dsingh\OneDrive - The Perse School\python_2024-25\Games\atticus\pixel-speech-bubble (3).png"]
    if running:
        running = run_voice_basic(inventory,lines, WIDTH//1.5,HEIGHT//4, r"C:\\Users\dsingh\OneDrive - The Perse School\python_2024-25\Games\atticusfinch.png", screen,question_indexes=[2],invent=["Mushroom for Miss Maudie", r"C:\Users\dsingh\OneDrive - The Perse School\python_2024-25\Games\mushroom.png"],voice=True) != -1
    all_sprites = pygame.sprite.Group()
    render_bg(all_sprites)

    player = Player()
    obstacles = pygame.sprite.Group()
    
    for i in range(3):
        obstacle = Obstacle(WIDTH + i * 400, 50, 50 * (350/700), 
                            img=r"C:\\Users\dsingh\OneDrive - The Perse School\python_2024-25\Games\rock.png")
        obstacles.add(obstacle)
    fast = pygame.sprite.Group()
    fast.add(Obstacle(WIDTH + 2200, 50, 50, 
                            img=r"Games\squirrel.png"))

    all_sprites.add(player, obstacles, fast)
    score,obs, immunity_timer, immune = 0,0,0, False
    pygame.mixer.music.load(r"Games\sfx\mainrunning.mp3")
    pygame.mixer.music.play(-1) 
    pygame.mixer.music.set_volume(0.5) 
    t = 0
    while running:
        clock.tick(60)
        obstacle_speed += 0.001
        gravity += 0.0001
        immunity_timer += 1
        if immunity_timer >= 30:
            immune = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:  # Detect key press
                if event.key == pygame.K_w:  # Check if it's the "W" key
                    open_inventory(screen)
                if event.key == pygame.K_s:  
                    open_shop(money, screen)

        keys = pygame.key.get_pressed()
        player.update(keys,gravity)
        obstacles.update(obstacle_speed)
        fast.update(20 ,fast=True)

        # Increase score
        for obstacle in obstacles:
            if not obstacle.scored and obstacle.rect.right < player.rect.left:
                score += 1
                obs += 50
                obstacle.scored = True  
        for obstacle in fast:
            if not obstacle.scored and obstacle.rect.right < player.rect.left:
                score += 3
                obs += 0
                obstacle.scored = True  


        # Collision Detection
        if not immune and (pygame.sprite.spritecollide(player, obstacles, False) or pygame.sprite.spritecollide(player, fast, False)):
            lives -= 1
            immune, immunity_timer = True, 0
            if lives == 0:
                pygame.mixer.music.pause()
                sfx = pygame.mixer.Sound(r"Games\sfx\game-over_rNHDd5K.mp3") 
                sfx.play()
                game_over(screen, all_sprites)
                running = False
            else:
                player.reset_position()
        
        x = houses(obs,screen)
        if x >= 0:
            obs +=1
            lives += x
                

        # Draw Everything
        screen.fill(WHITE)
        all_sprites.draw(screen)
        draw_text(f"Score: {score}", (WIDTH - 150, 10), font, screen, move = False)
        draw_text(f"Lives: {lives}", (20, 10), font, screen, RED, move = False)
        pygame.display.flip()

    pygame.quit()
    exit()


if __name__ == "__main__":
    # running quit in bg
    main()
    print(inventory)
