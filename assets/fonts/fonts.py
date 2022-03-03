import pygame
from settings import Settings

pygame.init()

my_settings = Settings()

fonts = pygame.font.get_fonts()

tot_width = 0
height = 0

for i in range(len(fonts)) :

    font = pygame.font.SysFont(fonts[i], 30)
    text = font.render(fonts[i],False,(255,255,255))
    if tot_width < my_settings.width - text.get_width() :
        my_settings.screen.blit(text,(tot_width,height))
    
    else:
        tot_width = 0
        height += 50
        my_settings.screen.blit(text,(tot_width,height))

    tot_width += text.get_width() + 10

pygame.display.flip()

loop = True
while loop :

    for event in pygame.event.get() :

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE :
            
            pygame.quit()
            exit()