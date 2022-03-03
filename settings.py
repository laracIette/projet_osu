import pygame

pygame.init()

class Settings :

    def __init__(self) :
        
        self.clock      = pygame.time.Clock()
        self.frequence  = 160
        self.resolution = pygame.display.Info()
        self.width      = 1920
        self.height     = 1080
        self.screen     = pygame.display.set_mode((self.width, self.height))