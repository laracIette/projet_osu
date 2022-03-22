import time
import pygame
from settings import Settings

my_settings = Settings()
wi = my_settings.width
he = my_settings.height

def Load(name,size,smooth) :

    image = pygame.image.load(f'assets\\{name}').convert_alpha()

    if image.get_width() == size[0] and image.get_height() == size[1] :
        return image

    if smooth :
        image = pygame.transform.smoothscale(image,size).convert_alpha()
    else :
        image = pygame.transform.scale(image,size).convert_alpha()

    return image

def GetTime() :
    return int(round(time.time() * 1000))

def ReSize(number):
    return number/1920*wi