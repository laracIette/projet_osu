import pygame
import time
import glob
import os
import math
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

def SkinSelect(font,skin,sounds,volume,volume_effects) :

    skins0 = []
    skins  = glob.glob('assets\\skins\\*')
    for i in skins :
        skins0.append(os.path.basename(i))
    
    skins = []
    for z in range(len(skins0)) :

        text = font.render(skins0[z],False,(255,255,255))
        my_settings.screen.blit(text,(0,he/15*z))

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
                    skin1_rect.y = he/15*w

                    if skin1_rect.collidepoint(pos) :
                        loop = False

                        play(sounds,'click',1,volume,volume_effects)
                        
                        skin = skins0[w]

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE :

                return skin

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and key[pygame.K_LALT]) :
                loop = False

                pygame.quit()
                exit(0)
    
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
        bg = pygame.transform.scale(bg,(wi,he)).convert()
        
        songs.append([bg,audio,diffs,diff_names])

        bg = pygame.image.load(bgs[1]).convert()
        bg = pygame.transform.scale(bg,(wi/5,he/5)).convert()
        my_settings.screen.blit(bg,(0,he/5*i))

    return songs

def Score(accuracy) :

    end_screen = load('images\\end_screen.png',(wi,he),False)

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
                exit(0)

def get_time() :
    return int(round(time.time() * 1000))

def import_sounds(skin) :
    sounds = {
               'click' : pygame.mixer.Sound(f'assets\\skins\\{skin}\\click.ogg'),
                'fail' : pygame.mixer.Sound(f'assets\\skins\\{skin}\\fail.ogg'),
                 'hit' : pygame.mixer.Sound(f'assets\\skins\\{skin}\\hit.ogg'),
                'miss' : pygame.mixer.Sound(f'assets\\skins\\{skin}\\miss.ogg'),
         'spinnerspin' : pygame.mixer.Sound(f'assets\\skins\\{skin}\\spinnerspin.ogg'),
        'spinnerbonus' : pygame.mixer.Sound(f'assets\\skins\\{skin}\\spinnerbonus.ogg')
    }
    return sounds

def play(sounds,name,volume,percentage,type) :
    sounds[name].set_volume(volume*percentage/100*type/100)
    sounds[name].play()

def rs(number):
    return number/1920*wi

def spinning(spin,pos2,spin_x,spin_y) :
    
    if spin_x >= 0 and spin_y >= 0 :

        if pos2[0] < wi/2 and pos2[1] >= he/2 :
            spin -= math.hypot(spin_x,spin_y)
        if pos2[0] >= wi/2 and pos2[1] < he/2 :
            spin += math.hypot(spin_x,spin_y)

    if spin_x >= 0 and spin_y < 0 :

        if pos2[0] < wi/2 and pos2[1] < he/2 :
            spin += math.hypot(spin_x,spin_y)
        if pos2[0] >= wi/2 and pos2[1] >= he/2 :
            spin -= math.hypot(spin_x,spin_y)

    if spin_x < 0 and spin_y >= 0 :

        if pos2[0] < wi/2 and pos2[1] < he/2 :
            spin -= math.hypot(spin_x,spin_y)
        if pos2[0] >= wi/2 and pos2[1] >= he/2 :
            spin += math.hypot(spin_x,spin_y)

    if spin_x < 0 and spin_y < 0 :

        if pos2[0] < wi/2 and pos2[1] >= he/2 :
            spin += math.hypot(spin_x,spin_y)
        if pos2[0] >= wi/2 and pos2[1] < he/2 :
            spin -= math.hypot(spin_x,spin_y)

    return spin

def propose_offset(total_ur,font) :

    pygame.mouse.set_visible(True)

    ur_moy = 0

    if total_ur != [] :

        noir = pygame.Rect(0,0,wi,he)
        pygame.draw.rect(my_settings.screen,(0,0,0),noir)
        
        for u in total_ur :
            ur_moy += u

        ur_moy /= len(total_ur)
        ur_moy = round(ur_moy)

        if ur_moy < 0 :
            rep = font.render(f'You are tapping {abs(ur_moy)}ms earlier, do you want to apply a negative offset of {abs(ur_moy)}ms ?',False,(255,255,255)).convert()
        
        if ur_moy > 0 :
            rep = font.render(f'You are tapping {abs(ur_moy)}ms too late, do you want to apply a positive offset of {abs(ur_moy)}ms ?',False,(255,255,255)).convert()

        rep_rect = rep.get_rect(center = (wi/2,he/2))

        yes      = font.render(f'Yes',False,(255,255,255)).convert()
        yes_rect = yes.get_rect(center = (wi/3,he/3*2))

        no      = font.render(f'No',False,(255,255,255)).convert()
        no_rect = no.get_rect(center = (wi/3*2,he/3*2))
        
        my_settings.screen.blit(rep,rep_rect) ; my_settings.screen.blit(yes,yes_rect) ; my_settings.screen.blit(no,no_rect)
        
        pygame.display.flip()
        
        loop = True
        while loop :

            for event in pygame.event.get() :

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT :

                    pos = pygame.mouse.get_pos()

                    if yes_rect.collidepoint(pos) :
                        
                        offset = - ur_moy

                        return offset
                    
                    if no_rect.collidepoint(pos) :

                        return 0