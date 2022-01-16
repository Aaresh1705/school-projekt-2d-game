# ------ libraries ------
import pygame
from pygame import mixer
import config

# ------ initialize modules ------
pygame.init()      
pygame.font.init()
pygame.mixer.init()

# ------ player class ------
class Player(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()

        width, height = 40, 60 #dimensions on player

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()

        self.change_x = 0
        self.change_y = 0

        self.jump_sound = mixer.Sound('assets/Jump.wav')

    # ------ gravity function ------
    def grav(self):
        if self.change_y == 0:
            self.change_y = 1   #players have a start velocity of 1 when falling
        else:
            self.change_y += 0.5

        if self.rect.y >= config.HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = config.HEIGHT - self.rect.height
            self.health = 0

    # ------ jump function ------
    def jump(self, player):
        self.rect.y += 2
        platform_hit = pygame.sprite.spritecollide(self, self.map.platform, False)
        player_hit = self.rect.colliderect(player.rect)
        self.rect.y -= 2

        if (len(platform_hit) > 0) or player_hit:
            self.change_y = -12
            self.jump_sound.stop()
            self.jump_sound.play()

    # ------ movement ------
    def go_left(self):
        self.change_x = -6

    def go_right(self):
        self.change_x = 6

    def stop(self):
        self.change_x = 0

    # ------ the things that gets updated in the class ------
    def update(self, player):

        self.health = 1

        self.grav()

        if self.change_y == 7:
            pygame.mixer.unpause()

        # ------ collision ------
        self.rect.x += self.change_x

        block_hit = pygame.sprite.spritecollide(self, self.map.platform, False)
        for block in block_hit:
            if self.change_x < 0:
                self.rect.left = block.rect.right
            elif self.change_x > 0:
                self.rect.right = block.rect.left

        spike_hit = pygame.sprite.spritecollide(self, self.map.spike, False)
        if spike_hit:
            self.health = 0
            for spike in spike_hit:
                if self.change_x < 0:
                    self.rect.left = spike.rect.right
                elif self.change_x > 0:
                    self.rect.right = spike.rect.left

        self.rect.x += 1
        goomba_hit = pygame.sprite.spritecollide(self, self.map.goomba, False)
        self.rect.x -= 1
        if goomba_hit:
            self.health = 0
            for goomba in goomba_hit:
                if self.change_x < 0:
                    self.rect.left = goomba.rect.right
                elif self.change_x > 0:
                    self.rect.right = goomba.rect.left

        self.rect.x -= 1
        goomba_hit = pygame.sprite.spritecollide(self, self.map.goomba, False)
        self.rect.x += 1
        if goomba_hit:
            self.health = 0
            for goomba in goomba_hit:
                if self.change_x < 0:
                    self.rect.left = goomba.rect.right
                elif self.change_x > 0:
                    self.rect.right = goomba.rect.left

        player_hit = self.rect.colliderect(player.rect)
        if player_hit:
            if self.change_x < 0:
                self.rect.left = player.rect.right
            elif self.change_x > 0:
                self.rect.right = player.rect.left

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

        self.rect.y += 1      
        goomba_hit = pygame.sprite.spritecollide(self, self.map.goomba, False)
        self.rect.y -= 1  
        if goomba_hit:
            self.health = 0 
            for goomba in goomba_hit:
                if self.change_y < 0:
                    self.rect.top = goomba.rect.bottom
                elif self.change_y > 0:
                    self.rect.bottom = goomba.rect.top
                
                self.change_y = 0

        self.rect.y -= 1 
        goomba_hit = pygame.sprite.spritecollide(self, self.map.goomba, False)
        self.rect.y += 1 
        if goomba_hit:
            self.health = 0 
            for goomba in goomba_hit:
                if self.change_y < 0:
                    self.rect.top = goomba.rect.bottom
                elif self.change_y > 0:
                    self.rect.bottom = goomba.rect.top
                
                self.change_y = 0

        player_hit = self.rect.colliderect(player.rect)
        if player_hit:
            if self.change_y < 0:
                self.rect.top = player.rect.bottom
            elif self.change_y > 0:
                self.rect.bottom = player.rect.top

            self.change_y = 0