# ------ libraries ------
import pygame
import config
import random


# ------ enemy class ------
class Goomba(pygame.sprite.Sprite):
    def __init__(self, speed, change_direction):
        super().__init__()

        width, height = 30, 30 #dimensions on enemy

        self.image = pygame.Surface([width, height])
        self.image.fill(config.GOOMBA_COLOR)

        self.rect = self.image.get_rect()

        self.change_x = speed
        self.change_y = 0

        self.health = 1

        self.direction = change_direction
    
    # ------ gravity function ------
    def grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.5

        if self.rect.y >= config.HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = config.HEIGHT - self.rect.height
            self.health = 0

    # ------ jump function ------
    def jump(self):
        self.rect.y += 1
        platform_hit = pygame.sprite.spritecollide(self, self.map.platform, False)
        self.rect.y -= 1

        if len(platform_hit) > 0:
            self.change_y = -8

    # ------ the things that gets updated in the class ------
    def update(self, update, player1, player2):

        self.map = update

        self.grav()

        if random.randrange(1000) >= 990:
            self.jump()  

        if self.health == 0: # deletes the instace of the class if its health is 0
            self.kill()

        # ------ collision ------
        self.rect.x += self.change_x

        block_hit = pygame.sprite.spritecollide(self, self.map.platform, False)
        for block in block_hit:
            if self.change_x < 0:
                self.rect.left = block.rect.right
                if self.direction == True:
                    self.change_x = -(self.change_x)
            elif self.change_x > 0:
                self.rect.right = block.rect.left
                if self.direction == True:
                    self.change_x = -(self.change_x)

        spike_hit = pygame.sprite.spritecollide(self, self.map.spike, False)
        if spike_hit:
            self.health = 0
            for spike in spike_hit:
                if self.change_x < 0:
                    self.rect.left = spike.rect.right
                elif self.change_x > 0:
                    self.rect.right = spike.rect.left

        player_hit = self.rect.colliderect(player1.rect)
        if player_hit:
            if self.change_x < 0:
                self.rect.left = player1.rect.right-0.01
            elif self.change_x > 0:
                self.rect.right = player1.rect.left+0.01

        player_hit = self.rect.colliderect(player2.rect)
        if player_hit:
            if self.change_x < 0:
                self.rect.left = player2.rect.right-0.01
            elif self.change_x > 0:
                self.rect.right = player2.rect.left+0.01

        self.rect.y += self.change_y

        block_hit = pygame.sprite.spritecollide(self, self.map.platform, False)
        for block in block_hit:
            if self.change_y < 0:
                self.rect.top = block.rect.bottom
            elif self.change_y > 0:
                self.rect.bottom = block.rect.top
                
            self.change_y = 0

        spike_hit = pygame.sprite.spritecollide(self, self.map.spike, False)
        if spike_hit:
            self.health = 0 
            for spike in spike_hit:
                if self.change_y < 0:
                    self.rect.top = spike.rect.bottom
                elif self.change_y > 0:
                    self.rect.bottom = spike.rect.top
                
                self.change_y = 0

        player_hit = self.rect.colliderect(player1.rect)
        if player_hit:
            if self.change_y < 0:
                self.rect.top = player1.rect.bottom
            elif self.change_y > 0:
                self.rect.bottom = player1.rect.top

            self.change_y = 0
        
        player_hit = self.rect.colliderect(player2.rect)
        if player_hit:
            if self.change_y < 0:
                self.rect.top = player2.rect.bottom
            elif self.change_y > 0:
                self.rect.bottom = player2.rect.top

            self.change_y = 0


# ------ platform class ------
class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height, color):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()


# ------ spike class ------
class Spike(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(config.SPIKE_COLOR)
        self.rect = self.image.get_rect()


# ------ world class ------
class World():
    def __init__(self):
        self.spike = pygame.sprite.Group()
        self.platform = pygame.sprite.Group()
        self.goomba = pygame.sprite.Group()

    # ------ update function ------
    def update(self, map, player1, player2):
        self.spike.update()
        self.platform.update() 
        self.goomba.update(map, player1, player2)

    # ------ draw function ------
    def draw(self, screen):
        screen.fill(config.BACKGROUND_COLOR)
        self.spike.draw(screen)
        self.platform.draw(screen)
        self.goomba.draw(screen)

    # ------ side scrolling function ------
    def shift_world(self, shift_x):
        for square in self.platform:
            square.rect.x += shift_x

        for square in self.spike:
            square.rect.x += shift_x

        for square in self.goomba:
            square.rect.x += shift_x

# ------ map class ------
class Map(World):
    def __init__(self, hard_jump, door_one_x_1, door_one_y_1, door_one_x_2, door_one_y_2):
        World.__init__(self)
        # ------ makes spikes ------
        spikes = [
            [25, 25, 550, 450],
            [25, 15, 1945, 435],
            [20, 15, 2435, 445],
            [20, 15, 2730, 465],
            [20, 20, 2200, 230],
            [20, 20, 2300, 230],
            [20, 20, 2395, 230],
            [20, 20, 2485, 230],
            [20, 20, 2575, 230],
        ]
        for spike in spikes:
            block = Spike(spike[0], spike[1])
            block.rect.x = spike[2]
            block.rect.y = spike[3]
            self.spike.add(block)
            
        # ------ makes platforms ------
        platforms = [
            [500, 50, 150, 550, config.PLATFORM_COLOR1], #starter  #max jump hight = 550-406 = 144
            [10, 300, 200, 406, config.PLATFORM_COLOR1],
            [210, 30, 838.5, hard_jump, config.PLATFORM_COLOR1], #tæt på pixel perfect
            [210, 70, 1000, 460, config.PLATFORM_COLOR1],
            [100, 20, 1100, 330, config.PLATFORM_COLOR1],
            [100, 50, -250, 550, config.PLATFORM_COLOR1], #border
            [210, 70, 1120, 280, config.PLATFORM_COLOR1],
            [210, 50, 1400, 370, config.PLATFORM_COLOR1],
            [300, 100, 1400, 20, config.PLATFORM_COLOR1],
            [260, 40, 1800, 100, config.PLATFORM_COLOR1],
            [120, 120, 1900, 450, config.PLATFORM_COLOR1],
            [400, 30, 2004, 540, config.PLATFORM_COLOR1],
            [100, 110, 2400, 460, config.PLATFORM_COLOR1],
            [550, 70, 2150, 250, config.PLATFORM_COLOR1],
            [door_one_x_1, door_one_y_1, 2690, 0, config.BORDER_COLOR],
            [door_one_x_2, door_one_y_2, 3000, 0, config.BORDER_COLOR],
            [600, 40, 2670, 480, config.PLATFORM_COLOR1],
        ]
        
        for platform in platforms:
            block = Platform(platform[0], platform[1], platform[4])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            self.platform.add(block)

        # ------ makes enemies ------
        goombas = [
            [-1, False, 1120, 100],
            [-1, True, 2150, 480],
            [2, True, 2250, 480],
        ]
        for goomba in goombas:
            block = Goomba(goomba[0], goomba[1])
            block.rect.x = goomba[2]
            block.rect.y = goomba[3]
            self.goomba.add(block)