import pygame
import time
from settings import Settings

my_settings = Settings()
wi = my_settings.width
he = my_settings.height

def load(name,size,smooth) :

    image = pygame.image.load(f'assets\\{name}').convert_alpha()
    if smooth :
        image = pygame.transform.smoothscale(image,size).convert_alpha()
    else :
        image = pygame.transform.scale(image,size).convert_alpha()

    return image

def get_time() :
    return int(round(time.time() * 1000))

def rs(number):
    return number/1920*wi