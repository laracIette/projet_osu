import math
import pygame
from setacc import SetAcc
from settings import Settings
from math import inf
from tools import load, SkinSelect, SongSelect, Score, get_time, import_sounds, play, rs
from interface import DarkenScreen, SetFps, SetShowOnScreen, ShowOnScreen, UItextRenders
from game import ApplyBreaks, EndGame, SetBreak, SetMap, StartGame, WriteSettings
from objects import GetCircle, GetSpinner, SetSpinners, SetCircles

my_settings = Settings()

class Run :

    def __init__(self,ii,diff,songs,skin,sounds,volume,volume_music,volume_effects,offset,lines) :

        self.wi = my_settings.width
        self.he = my_settings.height

        self.offset = offset
        self.songs  = songs
        self.diff   = diff
        self.ii     = ii
        self.lines  = lines

        self.sounds         = sounds
        self.volume         = volume
        self.volume_effects = volume_effects
        self.volume_music   = volume_music
        
        self.white  = (255,255,255)
        self.grey   = ( 48, 48, 48)
        self.black  = (  0,  0,  0)
        self.orange = (218,174, 70)
        self.green  = ( 87,227, 19)
        self.blue   = ( 50,188,231)

        if self.offset != 0 :
            self.show_offset = True
        else :
            self.show_offset = False

        self.offset_time = get_time()

        SetMap(self)

        pause_screen = load('images\\pause_screen.png',(self.wi,self.he),False)
        #dim         = load('images\\noir93.png',(self.wi,self.he),False)
        self.bg           = pygame.transform.scale(self.songs[self.ii][0],(self.wi,self.he)).convert()
        self.noir         = pygame.Rect(0,0,self.wi,self.he)
        
        self.game_break = True
        self.break_lock = False
        
        self.c_s     = rs(121/self.cs*4.9)
        self.circle  = load(f'skins\\{skin}\\hitcircle.png',(self.c_s,self.c_s),True)

        self.a_c_s    = self.c_s*4
        self.a_circle = load(f'skins\\{skin}\\approachcircle.png',(self.a_c_s,self.a_c_s),True)

        self.cursor       = load(f'skins\\{skin}\\cursor.png',(self.c_s,self.c_s),True)
        t_s          = self.c_s/4
        self.cursor_trail = load(f'skins\\{skin}\\cursortrail.png',(t_s,t_s),True)
        self.trail_pos    = []
        self.trail_count  = 0

        self.spinner      = load(f'skins\\{skin}\\spinner.png',(rs(400),rs(400)),True)
        self.spin         = 0
        self.show_spinner = False
        self.spin_tot     = 0
        self.spin_tot2    = 0

        self.pos  = pygame.mouse.get_pos()
        pos1 = pygame.mouse.get_pos()
        self.pos3 = pygame.mouse.get_pos()

        self.click_check = False

        self.fpss     = []
        self.avg_fps  = 0
        self.fps_time = get_time()
        self.fps_font = pygame.font.SysFont('arial',round(rs(30)))

        self.number_font = pygame.font.Font('assets\\fonts\\LeagueSpartanBold.ttf',round(self.c_s/2))
        
        self.acc       = []
        self.acc_check = False
        self.acc_font  = pygame.font.SysFont('segoeuisemibold',round(rs(45)))

        self.show_acc = []
        self.acc_miss = load(f'skins\\{skin}\\miss.png',(self.c_s/2,self.c_s/2),True)
        self.acc_100  = load(f'skins\\{skin}\\100.png',(self.c_s/2,self.c_s/2),True)
        self.acc_50   = load(f'skins\\{skin}\\50.png',(self.c_s/2,self.c_s/2),True)

        self.fade  = False
        self.faded = False

        self.start_time  = get_time()
        self.paused_time = 0
        pause_time  = 0
        self.end_time    = inf

        cs_od_hp = self.cs + self.od + self.hp

        if cs_od_hp < 6 :
            self.difficulty_multiplier = 2
        
        elif cs_od_hp >= 6 and cs_od_hp < 13 :
            self.difficulty_multiplier = 3

        elif cs_od_hp >= 13 and cs_od_hp < 18 :
            self.difficulty_multiplier = 4
        
        elif cs_od_hp >= 18 and cs_od_hp < 25 :
            self.difficulty_multiplier = 5

        elif cs_od_hp >= 25 :
            self.difficulty_multiplier = 6

        self.mod_multiplier = 1
        self.hit_value      = 0
        self.score          = 0
        self.combo          = 0
        self.combo_font     = pygame.font.SysFont('segoeuisemibold',round(rs(90)))

        self.max_health       = 600
        self.health           = self.max_health
        self.health_minus     = 50*self.hp/6
        self.passive_health   = self.health_minus/500
        self.spin_health      = self.max_health/300
        self.spinner_fade     = False
        self.health_bar_bg    = pygame.Rect(rs(20),rs(20),rs(600),rs(20))
        self.click_time       = 0
        self.click_time_check = False
        
        self.spin_score_bonus       = 0
        self.spin_score_bonus_time  = 0
        self.spin_score_bonus_alpha = 0

        self.ur_50     = pygame.Rect(rs(821),rs(1050),rs(278),rs(8))
        self.ur_100    = pygame.Rect(rs(875),rs(1050),rs(172),rs(8))
        self.ur_300    = pygame.Rect(rs(928),rs(1050),rs(66),rs(8))
        self.ur_middle = pygame.Rect(rs(959),rs(1039),rs(4),rs(30))
        self.show_ur   = []
        self.total_ur  = []

        self.score_txt = self.combo_font.render('0',False,self.white).convert()
        self.combo_txt = self.combo_font.render('0',False,self.white).convert()
        self.acc_txt   = self.acc_font.render('100.00%',False,self.white).convert()

        self.music_start = get_time() + self.start_offset
        self.playing     = False
        self.waiting     = False

        self.death = False

        self.numbers = 0

        pygame.mixer.music.load(self.songs[self.ii][1])
        pygame.mixer.music.set_volume(self.volume*self.volume_music/100)

        self.e  = 0
        self.q  = 0
        self.UI = True

        self.running = True
        while self.running :
            
            my_settings.clock.tick(my_settings.frequence)

            if self.waiting == False :

                if get_time() - self.paused_time >= self.music_start and self.playing == False :
                
                    StartGame(self)

                GetSpinner(self)
                
                GetCircle(self)

                ApplyBreaks(self)

                if get_time() >= self.end_time + self.start_offset or self.health <= 0 :

                    EndGame(self)

                    if self.death == False :

                        Score(self.accuracy)
        
                    pygame.mixer.music.unpause()
                    menu()

            SetBreak(self)
                
            DarkenScreen(self)

            SetCircles(self)
            
            UItextRenders(self)
            
            SetFps(self)
            
            SetShowOnScreen(self)
            
            SetSpinners(self)

            self.score_txt = self.combo_font.render(str(self.score),False,self.white).convert()

            ShowOnScreen(self)

            self.pos = pygame.mouse.get_pos()

            pygame.display.flip()
            
            key = pygame.key.get_pressed()
            for event in pygame.event.get() :

                if self.waiting == False :

                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_x or event.key == pygame.K_v) :

                        if self.click_check == False :
                            self.click_check = True
                        
                        SetAcc(self)
                        
                    if event.type == pygame.KEYUP and (event.key == pygame.K_x or event.key == pygame.K_v) :
                        self.click_check = False

                else :

                    pos1 = pygame.mouse.get_pos()

                    if (event.type == pygame.KEYDOWN and event.key == pygame.K_x) or (event.type == pygame.KEYDOWN and event.key == pygame.K_v) :
                        
                        distance1 = math.hypot(pos1[0]-self.pos[0],pos1[1]-self.pos[1])

                        if distance1 < 5 :

                            self.waiting = False

                            pygame.mixer.music.unpause()
                                                        
                            self.paused_time += get_time() - pause_time
                        
                if  (event.type == pygame.KEYDOWN and event.key == pygame.K_TAB and key[pygame.K_LSHIFT]) or\
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT and key[pygame.K_TAB]) :
                    if self.UI :
                        self.UI = False
                    else :
                        self.UI = True

                if event.type == pygame.KEYDOWN and event.key == pygame.K_EQUALS :

                    if key[pygame.K_LSHIFT] :
                        self.offset += 1
                    else :
                        self.offset += 5

                    self.offset_time = get_time()
                    self.show_offset = True

                if event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS :

                    if key[pygame.K_LSHIFT] :
                        self.offset -= 1
                    else :
                        self.offset -= 5

                    self.offset_time = get_time()
                    self.show_offset = True

                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and key[pygame.K_LALT]) :
                    self.running = False

                    WriteSettings(self)

                    pygame.quit()
                    exit(0)

                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) :
                    self.running = False
                    
                    if self.waiting :
                        self.paused_time += get_time() - pause_time

                    pause_time = get_time()

                    pygame.mouse.set_visible(True)
                    pygame.mixer.music.pause()

                    my_settings.screen.blit(pause_screen,(0,0))
                    pygame.display.flip()
                    
                    WriteSettings(self)

                    loop = True
                    while loop :

                        for event in pygame.event.get() :

                            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE :
                                loop    = False
                                self.running = True
                                self.waiting = True

                                pygame.mouse.set_visible(False)

                                self.fps_time += get_time() - pause_time

                            if event.type == pygame.KEYDOWN and event.key == pygame.K_q :
                                loop  = False

                                menu()

                            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and key[pygame.K_LALT]) :
                                loop = False

                                pygame.quit()
                                exit(0)

def menu() :

    pygame.mouse.set_visible(True)

    wi = my_settings.width
    he = my_settings.height

    black  = (  0,  0,  0)
    white  = (255,255,255)

    noir = pygame.Rect(0,0,wi,he)
    font = pygame.font.Font('assets\\fonts\\shippori.ttf',round(rs(45)))

    pygame.draw.rect(my_settings.screen,black,noir)
    
    skin   = 'whitecat'
    songs  = SongSelect()
    sounds = import_sounds(skin)

    with open('assets\\settings.txt','r') as settings_file :

            a = 0

            lines = settings_file.readlines()
            for i in lines :

                if a == 0 :

                    offset = int(i)
                
                if a == 1 :

                    volume = int(i)
                
                if a == 2 :

                    volume_music = int(i)

                if a == 3 :

                    volume_effects = int(i)

                a += 1
                
    volumes = [volume,volume_music,volume_effects]

    show_volume = True

    volume_font = pygame.font.SysFont('arial',round(rs(60)))
    music_font  = pygame.font.SysFont('arial',round(rs(40)))

    volume_txt    = volume_font.render(f'main : {volume}%',False,white).convert()
    volume_rect   = volume_txt.get_rect()
    volume_rect.y = he-2*volume_txt.get_height()-rs(15)

    music_txt    = music_font.render(f'music : {volume_music}%',False,white).convert()
    music_rect   = music_txt.get_rect()
    music_rect.y = he-2*music_txt.get_height()

    effects_txt    = music_font.render(f'effects : {volume_effects}%',False,white).convert()
    effects_rect   = effects_txt.get_rect()
    effects_rect.y = he-effects_txt.get_height()

    volume_noir = pygame.Rect(wi/3*2,he/3*2,wi/3,he/3)
    
    volume_time = get_time()

    loop = True
    while loop :

        my_settings.clock.tick(my_settings.frequence)

        if show_volume :
            
            pygame.draw.rect(my_settings.screen,black,volume_noir)

            if get_time() >= volume_time + 1000 :
                show_volume = False
                continue

            volume_rect.x = wi-volume_txt.get_width()
            music_rect.x = wi-music_txt.get_width()
            effects_rect.x = wi-effects_txt.get_width()

            my_settings.screen.blit(volume_txt,(volume_rect.x,volume_rect.y))
            my_settings.screen.blit(music_txt,(music_rect.x,music_rect.y))
            my_settings.screen.blit(effects_txt,(effects_rect.x,effects_rect.y))
        
        pygame.display.flip()

        key = pygame.key.get_pressed()
        for event in pygame.event.get() :

            pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN :

                if event.button == pygame.BUTTON_LEFT :

                    for ii in range(len(songs)) :

                        song = songs[ii][0]
                        song = pygame.transform.scale(song,(wi/5,he/5)).convert()

                        song_rect   = song.get_rect()
                        song_rect.y = my_settings.height/5*ii

                        if song_rect.collidepoint(pos) :
                            loop = False

                            play(sounds,'click',1,volume,volume_effects)

                            diffs = songs[ii][3]
                            for i in range(len(diffs)) :
                        
                                diff = font.render(diffs[i],False,white).convert()
                                my_settings.screen.blit(diff,(wi/5,he/20*i+he/5*ii))
                            
                            loop2 = True
                            while loop2 :
                                
                                my_settings.clock.tick(my_settings.frequence)
                                pygame.display.flip()
                                
                                key = pygame.key.get_pressed()
                                for event in pygame.event.get() :

                                    if event.type == pygame.MOUSEBUTTONDOWN :
                                        pos = pygame.mouse.get_pos()
                                    
                                        for i in range(len(diffs)) :
                                    
                                            diff = font.render(diffs[i],False,white).convert()

                                            diff_rect   = diff.get_rect()
                                            diff_rect.x = wi/5
                                            diff_rect.y = he/20*i+he/5*ii

                                            if diff_rect.collidepoint(pos) :
                                                loop2 = False

                                                play(sounds,'click',1,volume,volume_effects)

                                                pygame.mouse.set_visible(False)
                                                Run(ii,i,songs,skin,sounds,volume,volume_music,volume_effects,offset,lines)

                                    if event.type == pygame.KEYDOWN and event.key == pygame.K_s :
                                        loop2 = False

                                        pygame.draw.rect(my_settings.screen,black,noir)

                                        skin   = SkinSelect(font,skin,sounds,volume,volume_effects)
                                        songs  = SongSelect()
                                        sounds = import_sounds(skin)

                                        loop = True

                                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE :
                                        loop2 = False

                                        with open('assets\\settings.txt','w') as settings_file :
                                            
                                            modifs = [offset,volume,volume_music,volume_effects]

                                            for a in range(len(lines)) :

                                                settings_file.write(lines[a].replace(lines[a],f'{modifs[a]}\n'))
                                        
                                        menu()

                                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and key[pygame.K_LALT]) :
                                        loop2 = False

                                        with open('assets\\settings.txt','w') as settings_file :
                                            
                                            modifs = [offset,volume,volume_music,volume_effects]

                                            for a in range(len(lines)) :

                                                settings_file.write(lines[a].replace(lines[a],f'{modifs[a]}\n'))

                                        pygame.quit()
                                        exit(0)

                if event.button == 4 or event.button == 5 :

                    rects   = [volume_rect,music_rect,effects_rect]

                    for i in range(len(rects)) :

                        if rects[i].collidepoint(pos) :
                        
                            if event.button == 4 :

                                if volumes[i] < 100 :

                                    volumes[i] += 1
                
                            if event.button == 5 :

                                if volumes[i] > 0 :

                                    volumes[i] -= 1

                    show_volume = True

                    volume         = volumes[0]
                    volume_music   = volumes[1]
                    volume_effects = volumes[2]

                    volume_txt  = volume_font.render(f'main : {volume}%',False,white).convert()
                    music_txt   = music_font.render(f'music : {volume_music}%',False,white).convert()
                    effects_txt = music_font.render(f'effects : {volume_effects}%',False,white).convert()
                    
                    volume_time = get_time()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_s :

                pygame.draw.rect(my_settings.screen,black,noir)

                skin   = SkinSelect(font,skin,sounds,volume,volume_effects)
                songs  = SongSelect()
                sounds = import_sounds(skin)
                
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and key[pygame.K_LALT]) :
                loop = False

                with open('assets\\settings.txt','w') as settings_file :
                                            
                    modifs = [offset,volume,volume_music,volume_effects]

                    for a in range(len(lines)) :

                        settings_file.write(lines[a].replace(lines[a],f'{modifs[a]}\n'))

                pygame.quit()
                exit(0)