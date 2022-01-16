"""
This is a 2 player 2D side scroller platform game made in python.
By Jacob, Hector and Marcus
With Sofus 2.y, Lauge 2.y and Joachim 2.y as playtesters

Get the code on githup: https://

------ CONTROLLS ------
W, A & D    - player one
arrow keys  - player two
"""

# ------ libraries ------
import pygame
from pygame import mixer
import time

import config
from player import Player
from world import Map


# ------ initialize modules ------
pygame.init()      
pygame.font.init()
pygame.mixer.init()


screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))  

# ------ on death function ------
def taunt():
    font = pygame.font.SysFont('freesansbold.ttf', 30)
    text = font.render("LOL you died + ratio", True, config.RED)
    screen.blit(text, (config.WIDTH/2 - text.get_rect().width/2, config.HEIGHT/2 - text.get_rect().height/2))
    pygame.display.update()

    time.sleep(1)

# ------ "function setup" ------
def main():
    running = True
    pygame.display.set_caption('Epic gaming game')

    player1 = Player(config.PLAYER1_COLOR)
    player2 = Player(config.PLAYER2_COLOR)

    death_counter = 0
    impossible_jump = 550

    door1 = True
    door1_x_1 = 10
    door1_y_1 = 250
    door1_x_2 = 10
    door1_y_2 = 480
    
    current_map = Map(impossible_jump, door1_x_1, door1_y_1, door1_x_2, door1_y_2)
    player1_sprite = pygame.sprite.Group()
    player2_sprite = pygame.sprite.Group()
    player1.map, player2.map = current_map, current_map
    
    player1.rect.x = 340
    player1.rect.y = config.HEIGHT - player1.rect.height - 100
    player1_sprite.add(player1)

    player2.rect.x = 440
    player2.rect.y = config.HEIGHT - player2.rect.height - 100
    player2_sprite.add(player2)

    left_dist = config.WIDTH-200
    right_dist = 200

    font = pygame.font.SysFont('freesansbold.ttf', 30)
    Img = pygame.image.load('assets/Troll.png')
    clock = pygame.time.Clock()

    shift = 0
    diff = 0

    background_music = mixer.Sound('assets/Background.wav')
    background_music.play(-1)
    pygame.mixer.Sound.set_volume(background_music, 0.25)

    # ------ "function draw" ------
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # ------ movement ------
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player1.go_left()
                if event.key == pygame.K_LEFT:
                    player2.go_left()
                
                if event.key == pygame.K_d:
                    player1.go_right()
                if event.key == pygame.K_RIGHT:
                    player2.go_right()

                if event.key == pygame.K_w:
                    player1.jump(player2)
                if event.key == pygame.K_UP:
                    player2.jump(player1)
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player1.change_x < 0:
                    player1.stop()
                if event.key == pygame.K_LEFT and player2.change_x < 0:
                    player2.stop()
                
                if event.key == pygame.K_d and player1.change_x > 0:
                    player1.stop()
                if event.key == pygame.K_RIGHT and player2.change_x > 0:
                    player2.stop()
            
        # ------ update ------
        current_map.update(current_map, player1, player2)
        player1_sprite.update(player2)
        player2_sprite.update(player1)

        # ------ side scrolling shift ------
        shift += diff
        if player1.rect.right >= left_dist:
            diff = -(player1.rect.right - left_dist)
            if player2.rect.left <= right_dist:
                diff = 0
            player1.rect.right = left_dist
            current_map.shift_world(diff)
            shift += diff
            player2.rect.x += diff
            diff = 0 
        
        if player2.rect.right >= left_dist:
            diff = -(player2.rect.right - left_dist)
            if player1.rect.left <= right_dist:
                diff = 0
            player2.rect.right = left_dist
            current_map.shift_world(diff)
            shift += diff
            player1.rect.x += diff
            diff = 0 

        if player1.rect.left <= right_dist:
            diff = right_dist - player1.rect.left
            if player2.rect.right >= left_dist:
                diff = 0
            player1.rect.left = right_dist
            current_map.shift_world(diff)
            shift += diff
            player2.rect.x += diff
            diff = 0  
        
        if player2.rect.left <= right_dist:
            diff = right_dist - player2.rect.left
            if player1.rect.right >= left_dist:
                diff = 0
            player2.rect.left = right_dist
            current_map.shift_world(diff)
            shift += diff
            player1.rect.x += diff
            diff = 0  

        # ------ draw ------
        current_map.draw(screen)

        death_text = font.render("Death Count: " + str(death_counter), True, config.BLACK)
        screen.blit(death_text, (20, 20))

        screen.blit(Img, (-500+shift, 50))

        jump_text = font.render("Jump here!", True, config.BLACK)
        if door1 == True:
            screen.blit(jump_text, (2575+shift, 75))

        player1_sprite.draw(screen)
        player2_sprite.draw(screen)

        # ------ if dead ------
        if player1.health == 0 or player2.health == 0:
            player1.jump_sound.stop()
            player2.jump_sound.stop()
            pygame.mixer.pause()
            dead_sound = mixer.Sound('assets/Death.wav')
            dead_sound.stop()        
            dead_sound.play()
            current_map = Map(impossible_jump, door1_x_1, door1_y_1, door1_x_2, door1_y_2)
            player1.map, player2.map = current_map, current_map
            player1_sprite.update(player2)
            player2_sprite.update(player1)
            current_map.update(current_map, player1, player2)
            taunt()
            player1.rect.x = 340
            player1.rect.y = config.HEIGHT - player1.rect.height - 100
            player2.rect.x = 440
            player2.rect.y = config.HEIGHT - player2.rect.height - 100

            if(impossible_jump > 410):
                impossible_jump -= 10
            else:
                impossible_jump = 407

            death_counter += 1
            diff = 0
            shift = 0
            player1.change_y, player2.change_y = 0, 0

        # ------ door 1 open ------
        if ((shift <= -2050 and shift >= -2100 and player1.rect.bottom <= 180 ) or (shift <= -2050 and shift >= -2100 and player2.rect.bottom <= 180 )) and (door1 == True):
            door1_x_1, door1_y_1, door1_x_1, door1_y_1 = 0, 0, 0, 0

            impossible_jump = 550
            current_map = Map(impossible_jump, door1_x_1, door1_y_1, door1_x_2, door1_y_2)
            player1.map, player2.map = current_map, current_map
            player1_sprite.update(player2)
            player2_sprite.update(player1)
            current_map.update(current_map, player1, player2)

            font = pygame.font.SysFont('freesansbold.ttf', 30)
            text = font.render("Door 1 unlocked", True, config.RED)
            screen.blit(text, (config.WIDTH/2 - text.get_rect().width/2, config.HEIGHT/2 - text.get_rect().height/2))
            pygame.display.update()

            time.sleep(2)

            player1.rect.x = 340
            player1.rect.y = config.HEIGHT - player1.rect.height - 100
            player2.rect.x = 440
            player2.rect.y = config.HEIGHT - player2.rect.height - 100
            player1.change_y, player2.change_y = 0, 0
            door1 = False

            diff = 0
            shift = 0

        clock.tick(60)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()