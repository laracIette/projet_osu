import pygame
import time
import glob
import os
from settings import Settings

my_settings = Settings()

def load(name,size) :

    image = pygame.image.load(f'assets\\{name}').convert_alpha()
    image = pygame.transform.scale(image,size).convert_alpha()

    return image

def SkinSelect(font,skin,sounds) :

    skins0 = []
    skins  = glob.glob('assets\\skins\\*')
    for i in skins :
        skins0.append(os.path.basename(i))
    
    skins = []
    for z in range(len(skins0)) :

        text = font.render(skins0[z],False,(255,255,255))
        my_settings.screen.blit(text,(0,my_settings.height/15*z))

        skins.append(text)

    pygame.display.flip()
    
    loop = True
    while loop :

        pos = pygame.mouse.get_pos()
        key = pygame.key.get_pressed()
        for event in pygame.event.get() :

            if event.type == pygame.MOUSEBUTTONDOWN :

                for w in range(len(skins)) :

                    skin1 = skins[w]

                    skin1_rect   = skin1.get_rect()
                    skin1_rect.y = my_settings.height/15*w

                    if skin1_rect.collidepoint(pos) :
                        loop = False

                        play(sounds,'click',1)
                        
                        skin = skins0[w]

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE :

                return skin

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and key[pygame.K_LALT]) :
                loop = False

                pygame.quit()
                exit()
    
    return skin

def SongSelect() :

    maps  = glob.glob('assets\\songs\\*')
    songs = []

    for i in range(len(maps)) :

        audio = glob.glob(f'{maps[i]}\\*.mp3')
        audio = audio[0]

        diffs = []
        diff = glob.glob(f'{maps[i]}\\*.txt')
        for v in range(len(diff)) :
            diffs.append(diff[v])

        diff_names = []
        for u in diffs :

            diff_names.append(os.path.basename(os.path.splitext(u)[0]))

        bgs = glob.glob(f'{maps[i]}\\*.jpg')
        bg = pygame.image.load(bgs[0]).convert()
        bg = pygame.transform.scale(bg,(my_settings.width,my_settings.height)).convert()
        
        songs.append([bg,audio,diffs,diff_names])

        bg = pygame.image.load(bgs[1]).convert()
        bg = pygame.transform.scale(bg,(my_settings.width/5,my_settings.height/5)).convert()
        my_settings.screen.blit(bg,(0,my_settings.height/5*i))

    return songs

def Score(accuracy) :

    end_screen = load('images\\end_screen.png',(my_settings.width,my_settings.height))

    my_settings.screen.blit(end_screen,(0,0))
    pygame.display.flip()

    #print('accuracy :',round(accuracy,2))

    loop = True
    while loop :

        key = pygame.key.get_pressed()
        for event in pygame.event.get() :

            if event.type == pygame.KEYDOWN and event.key == pygame.K_q :
                loop = False

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and key[pygame.K_LALT]) :
                loop = False

                pygame.quit()
                exit()

def get_time():
    return int(round(time.time() * 1000))

def import_sounds(skin) :
    sounds = {
        'click': pygame.mixer.Sound(f'assets\\skins\\{skin}\\click.ogg'),
        'fail': pygame.mixer.Sound(f'assets\\skins\\{skin}\\fail.ogg'),
        'hit': pygame.mixer.Sound(f'assets\\skins\\{skin}\\hit.ogg'),
        'miss': pygame.mixer.Sound(f'assets\\skins\\{skin}\\miss.ogg'),
        'spinnerspin': pygame.mixer.Sound(f'assets\\skins\\{skin}\\spinnerspin.ogg'),
        'spinnerbonus': pygame.mixer.Sound(f'assets\\skins\\{skin}\\spinnerbonus.ogg')
    }
    return sounds

def play(sounds,name,volume,percentage) :
    sounds[name].set_volume(volume*percentage/100)
    sounds[name].play()

def rs(number):
    return number/1920*my_settings.width