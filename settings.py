import pygame

pygame.init()

class Settings : # classe contenant les parametres systemes du programme

    def __init__(self) :
        
        self.clock      = pygame.time.Clock()
        self.frequence  = 160
        self.resolution = pygame.display.Info()
        self.width      = self.resolution.current_w
        self.height     = self.resolution.current_h
        flags           = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        self.screen     = pygame.display.set_mode((self.width, self.height),flags)