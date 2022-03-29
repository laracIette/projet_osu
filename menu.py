import os
import glob
import pygame
from sounds import Play
from gameend import GameQuit, Write
from tools import GetTime, Load, ReSize

def SkinSelect(menu) : # selection du skin

    pygame.draw.rect(menu.my_settings.screen,menu.black,menu.noir)

    skins0 = []
    skins  = glob.glob('assets\\skins\\*')
    for i in skins :
        skins0.append(os.path.basename(i))
    
    skins = []
    for z in range(len(skins0)) :

        text = menu.font.render(skins0[z],False,menu.white)
        menu.my_settings.screen.blit(text,(0,menu.he/15*z))

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
                    skin1_rect.y = menu.he/15*w

                    if skin1_rect.collidepoint(pos) :
                        loop = False

                        Play(menu.sounds,'click',1,menu.volume,menu.volume_effects)
                        
                        menu.skin = skins0[w]

                return menu.skin

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE :

                return menu.skin

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and key[pygame.K_LALT]) :
                loop = False

                Write(menu)

                pygame.quit()
                exit(0)

def SongSelect(menu) : # definition des maps possibles

    menu.maps  = glob.glob('assets\\songs\\*')
    menu.songs = []

    for i in range(len(menu.maps)) :

        audio = glob.glob(f'{menu.maps[i]}\\*.mp3')
        audio = audio[0]
        
        menu.map_names = []
        for j in menu.maps :

            menu.map_names.append(os.path.basename(j))

        diffs = []
        diff  = glob.glob(f'{menu.maps[i]}\\*.txt')
        for v in range(len(diff)) :
            diffs.append(diff[v])

        diff_names = []
        for u in diffs :

            diff_names.append(os.path.basename(os.path.splitext(u)[0]))

        bgs = glob.glob(f'{menu.maps[i]}\\*.jpg')
        bg  = pygame.image.load(bgs[0]).convert()
        bg  = pygame.transform.scale(bg,(menu.wi,menu.he)).convert()
        
        menu.songs.append([bg,audio,diffs,diff_names])

    return menu.songs

def MenuShowVolume(menu) : # affiche le volume dans le menu

    if menu.show_volume :
            
        pygame.draw.rect(menu.my_settings.screen,menu.black,menu.volume_noir)

        if GetTime() >= menu.volume_time + 1000 :
            menu.show_volume = False
            return 0

        menu.volume_rect.x  = menu.wi-menu.volume_txt.get_width()
        menu.music_rect.x   = menu.wi-menu.music_txt.get_width()
        menu.effects_rect.x = menu.wi-menu.effects_txt.get_width()

        menu.my_settings.screen.blit(menu.volume_txt,(menu.volume_rect.x,menu.volume_rect.y))
        menu.my_settings.screen.blit(menu.music_txt,(menu.music_rect.x,menu.music_rect.y))
        menu.my_settings.screen.blit(menu.effects_txt,(menu.effects_rect.x,menu.effects_rect.y))

def SetVolumeOffsetSkinMod(menu) : # recupere et attribut les donnees de settings.txt

    with open('assets\\settings.txt','r') as settings_file :

        a = 0

        menu.lines = settings_file.readlines()
        for i in menu.lines :

            if a == 0 :

                menu.offset = int(i)
            
            if a == 1 :

                menu.volume = int(i)
            
            if a == 2 :

                menu.volume_music = int(i)

            if a == 3 :

                menu.volume_effects = int(i)

            if a == 4 :

                skin_t = []
                for s in menu.lines[a] :
                    if s != '\n' :
                        skin_t.append(s)
                menu.skin = ''.join(skin_t)

            a += 1
                    
    menu.volumes = [menu.volume,menu.volume_music,menu.volume_effects]

def ModifyVolumes(menu) : # detecte si besoin et applique changement de volume

    rects = [menu.volume_rect,menu.music_rect,menu.effects_rect]

    for i in range(len(rects)) :

        if rects[i].collidepoint(menu.pos) :
        
            if menu.event.button == 4 :

                if menu.volumes[i] < 100 :

                    menu.volumes[i] += 1

            if menu.event.button == 5 :

                if menu.volumes[i] > 0 :

                    menu.volumes[i] -= 1

    menu.show_volume = True

    menu.volume         = menu.volumes[0]
    menu.volume_music   = menu.volumes[1]
    menu.volume_effects = menu.volumes[2]

    menu.volume_txt  = menu.volume_font.render(f'main : {menu.volume}%',False,menu.white).convert()
    menu.music_txt   = menu.music_font.render(f'music : {menu.volume_music}%',False,menu.white).convert()
    menu.effects_txt = menu.music_font.render(f'effects : {menu.volume_effects}%',False,menu.white).convert()
    
    menu.volume_time = GetTime()

def MapSelect(menu) : # selection de la map

    for menu.ii in range(len(menu.songs)) :

        song = menu.songs[menu.ii][0]
        song = pygame.transform.scale(song,(menu.wi/5,menu.he/5)).convert()

        song_rect   = song.get_rect()
        song_rect.y = menu.my_settings.height/5*menu.ii

        if song_rect.collidepoint(menu.pos) :

            menu.choosing_diff = True
            menu.map = menu.ii

            Play(menu.sounds,'click',1,menu.volume,menu.volume_effects)

def DiffSelect(menu) : # selection de la difficulte

    diff = menu.font.render(menu.diffs[menu.diff],False,menu.white).convert()

    diff_rect   = diff.get_rect()
    diff_rect.x = menu.wi/5
    diff_rect.y = menu.he/20*menu.diff+menu.he/5*menu.map

    if diff_rect.collidepoint(menu.pos) :
        menu.diff_choice = True

        Play(menu.sounds,'click',1,menu.volume,menu.volume_effects)
        pygame.mouse.set_visible(False)

def GetMods(menu) : # definir les modes de jeu

    menu.mods = ['easy',    'nofail',     'halftime',
                'hardrock','suddendeath','doubletime','hidden',  'flashlight',
                'relax',   'autopilot',  'spunout',   'autoplay','scorev2']
    
    w = 0
    h = 0
    menu.mods_icons = []
    for i in range(len(menu.mods)) :
    
        center_rect = (ReSize(505+220*w),ReSize(305+220*h))
        mod_icon    = Load(f'skins\\{menu.skin}\\mods\\{menu.mods[i]}.png',(ReSize(180),ReSize(180)),False)
        mod_rect    = mod_icon.get_rect(center = center_rect)

        w += 1

        if i == 2 or i == 7 :
            h += 1
            w  = 0

        menu.mods_icons.append([mod_icon,mod_rect,center_rect,False])

def ModChoice(menu) : # choisir un mode de jeu

    for mod in menu.mods_icons :

        mod_icon = mod[0]

        if mod[3] :
            mod_icon = pygame.transform.rotate(mod[0],-15).convert()

        mod_rect = mod_icon.get_rect(center = mod[2])

        menu.my_settings.screen.blit(mod_icon,mod_rect)

    loop = True
    while loop :

        menu.my_settings.clock.tick(menu.my_settings.frequence)

        menu.pos = pygame.mouse.get_pos()
        for menu.event in pygame.event.get() :
                
            if menu.event.type == pygame.MOUSEBUTTONDOWN and menu.event.button == pygame.BUTTON_LEFT :

                ModSelect(menu)

            if menu.event.type == pygame.KEYDOWN and (menu.event.key == pygame.K_F1 or menu.event.key == pygame.K_ESCAPE) :

                loop = False

                return menu.mod_list

            GameQuit(menu)

        pygame.display.flip()

def ModSelect(menu) :

    mod_lock = False

    for i in range(len(menu.mods_icons)) :

        mod_rect = menu.mods_icons[i][1]

        if mod_rect.collidepoint(menu.pos) :

            for m in range(len(menu.mod_list)) :

                if menu.mod_list[m] == menu.mods[i] :
                    
                    menu.mod_list.pop(m)
                    mod_lock = True

                    break
            
            if mod_lock == False :
                menu.mod_list.append(menu.mods[i])

            if menu.mods_icons[i][3] == False :
                menu.mods_icons[i][3] = True
            else :
                menu.mods_icons[i][3] = False

            for e in range(15) :

                if menu.mods_icons[i][3] :
                    mod_icon = pygame.transform.rotate(menu.mods_icons[i][0],-e).convert()
                else :
                    mod_icon = pygame.transform.rotate(menu.mods_icons[i][0],0).convert()

                mod_rect = mod_icon.get_rect(center = menu.mods_icons[i][2])

                menu.my_settings.screen.blit(mod_icon,mod_rect)
                pygame.display.flip()