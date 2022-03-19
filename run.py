import math
import pygame
from math import inf
from gameend import Score
from menu import MenuShowVolume, MenuWrite, SetVolumes, SkinSelect, SongSelect
from settings import Settings
from setacc import SetAcc
from sounds import ImportSounds, Play
from tools import load, get_time, rs
from interface import DarkenScreen, SetFps, SetShowOnScreen, ShowOnScreen, UItextRenders
from game import ApplyBreaks, EndGame, SetBreak, SetMap, StartGame, GameWrite
from objects import GetCircle, GetSpinner, SetSpinners, SetCircles

class Run :

    def __init__(self,ii,diff,songs,skin,sounds,volume,volume_music,volume_effects,offset,lines) :

        self.my_settings = Settings()

        self.wi = self.my_settings.width
        self.he = self.my_settings.height

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
        self.bg      = pygame.transform.scale(self.songs[self.ii][0],(self.wi,self.he)).convert()
        self.noir    = pygame.Rect(0,0,self.wi,self.he)
        
        self.game_break = True
        self.break_lock = False
        
        self.c_s     = rs(121/self.cs*4.9)
        self.circle  = load(f'skins\\{skin}\\hitcircle.png',(self.c_s,self.c_s),True)

        self.a_c_s    = self.c_s*4
        self.a_circle = load(f'skins\\{skin}\\approachcircle.png',(self.a_c_s,self.a_c_s),True)

        self.cursor       = load(f'skins\\{skin}\\cursor.png',(self.c_s,self.c_s),True)
        self.cursor_trail = load(f'skins\\{skin}\\cursortrail.png',(self.c_s/4,self.c_s/4),True)
        self.trail_pos    = []
        self.trail_count  = 0

        self.spinner      = load(f'skins\\{skin}\\spinner.png',(rs(400),rs(400)),True)
        self.spin         = 0
        self.show_spinner = False
        self.spin_tot     = 0
        self.spin_tot2    = 0

        self.pos  = pygame.mouse.get_pos()
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
        pause_time       = 0
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
            
            self.my_settings.clock.tick(self.my_settings.frequence)

            if self.waiting == False :

                if get_time() - self.paused_time >= self.music_start and self.playing == False :
                
                    StartGame(self)

                GetSpinner(self)
                
                GetCircle(self)

                ApplyBreaks(self)

                if get_time() >= self.end_time + self.start_offset or self.health <= 0 :

                    EndGame(self)

                    if self.death == False :

                        Score(self)
        
                    pygame.mixer.music.unpause()
                    Menu()

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

                    GameWrite(self)

                    pygame.quit()
                    exit(0)

                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) :
                    self.running = False
                    
                    if self.waiting :
                        self.paused_time += get_time() - pause_time

                    pause_time = get_time()

                    pygame.mouse.set_visible(True)
                    pygame.mixer.music.pause()

                    self.my_settings.screen.blit(pause_screen,(0,0))
                    pygame.display.flip()
                    
                    GameWrite(self)

                    loop = True
                    while loop :

                        for event in pygame.event.get() :

                            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE :
                                loop = False

                                self.running = True
                                self.waiting = True

                                pygame.mouse.set_visible(False)

                                self.fps_time += get_time() - pause_time

                            if event.type == pygame.KEYDOWN and event.key == pygame.K_q :
                                loop  = False

                                Menu()

                            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and key[pygame.K_LALT]) :
                                loop = False

                                pygame.quit()
                                exit(0)

class Menu() :

    def __init__(self) :

        pygame.mouse.set_visible(True)

        self.my_settings = Settings()

        self.wi = self.my_settings.width
        self.he = self.my_settings.height

        self.black  = (  0,  0,  0)
        self.white  = (255,255,255)

        noir = pygame.Rect(0,0,self.wi,self.he)
        self.font = pygame.font.Font('assets\\fonts\\shippori.ttf',round(rs(45)))

        pygame.draw.rect(self.my_settings.screen,self.black,noir)
        
        self.skin   = 'whitecat'
        self.songs  = SongSelect(self)
        self.sounds = ImportSounds(self.skin)

        SetVolumes(self)

        self.show_volume = True

        volume_font = pygame.font.SysFont('arial',round(rs(60)))
        music_font  = pygame.font.SysFont('arial',round(rs(40)))

        self.volume_txt    = volume_font.render(f'main : {self.volume}%',False,self.white).convert()
        self.volume_rect   = self.volume_txt.get_rect()
        self.volume_rect.y = self.he-2*self.volume_txt.get_height()-rs(15)

        self.music_txt    = music_font.render(f'music : {self.volume_music}%',False,self.white).convert()
        self.music_rect   = self.music_txt.get_rect()
        self.music_rect.y = self.he-2*self.music_txt.get_height()

        self.effects_txt    = music_font.render(f'effects : {self.volume_effects}%',False,self.white).convert()
        self.effects_rect   = self.effects_txt.get_rect()
        self.effects_rect.y = self.he-self.effects_txt.get_height()

        self.volume_noir = pygame.Rect(self.wi/3*2,self.he/3*2,self.wi/3,self.he/3)
        
        self.volume_time = get_time()

        loop = True
        while loop :

            self.my_settings.clock.tick(self.my_settings.frequence)

            MenuShowVolume(self)
            
            pygame.display.flip()

            key = pygame.key.get_pressed()
            for event in pygame.event.get() :

                pos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN :

                    if event.button == pygame.BUTTON_LEFT :

                        for ii in range(len(self.songs)) :

                            song = self.songs[ii][0]
                            song = pygame.transform.scale(song,(self.wi/5,self.he/5)).convert()

                            song_rect   = song.get_rect()
                            song_rect.y = self.my_settings.height/5*ii

                            if song_rect.collidepoint(pos) :
                                loop = False

                                Play(self.sounds,'click',1,self.volume,self.volume_effects)

                                diffs = self.songs[ii][3]
                                for i in range(len(diffs)) :
                            
                                    diff = self.font.render(diffs[i],False,self.white).convert()
                                    self.my_settings.screen.blit(diff,(self.wi/5,self.he/20*i+self.he/5*ii))
                                
                                loop2 = True
                                while loop2 :
                                    
                                    self.my_settings.clock.tick(self.my_settings.frequence)
                                    pygame.display.flip()
                                    
                                    key = pygame.key.get_pressed()
                                    for event in pygame.event.get() :

                                        if event.type == pygame.MOUSEBUTTONDOWN :
                                            pos = pygame.mouse.get_pos()
                                        
                                            for i in range(len(diffs)) :
                                        
                                                diff = self.font.render(diffs[i],False,self.white).convert()

                                                diff_rect   = diff.get_rect()
                                                diff_rect.x = self.wi/5
                                                diff_rect.y = self.he/20*i+self.he/5*ii

                                                if diff_rect.collidepoint(pos) :
                                                    loop2 = False

                                                    Play(self.sounds,'click',1,self.volume,self.volume_effects)

                                                    pygame.mouse.set_visible(False)
                                                    Run(ii,i,self.songs,self.skin,self.sounds,self.volume,self.volume_music,self.volume_effects,self.offset,self.lines)

                                        if event.type == pygame.KEYDOWN and event.key == pygame.K_s :
                                            loop2 = False

                                            pygame.draw.rect(self.my_settings.screen,self.black,noir)

                                            self.skin   = SkinSelect(self)
                                            self.songs  = SongSelect(self)
                                            self.sounds = ImportSounds(self.skin)

                                            loop = True

                                        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE :
                                            loop2 = False

                                            MenuWrite(self)
                                            
                                            Menu()

                                        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and key[pygame.K_LALT]) :
                                            loop2 = False

                                            MenuWrite(self)

                                            pygame.quit()
                                            exit(0)

                    if event.button == 4 or event.button == 5 :

                        rects = [self.volume_rect,self.music_rect,self.effects_rect]

                        for i in range(len(rects)) :

                            if rects[i].collidepoint(pos) :
                            
                                if event.button == 4 :

                                    if self.volumes[i] < 100 :

                                        self.volumes[i] += 1
                    
                                if event.button == 5 :

                                    if self.volumes[i] > 0 :

                                        self.volumes[i] -= 1

                        self.show_volume = True

                        self.volume         = self.volumes[0]
                        self.volume_music   = self.volumes[1]
                        self.volume_effects = self.volumes[2]

                        self.volume_txt  = volume_font.render(f'main : {self.volume}%',False,self.white).convert()
                        self.music_txt   = music_font.render(f'music : {self.volume_music}%',False,self.white).convert()
                        self.effects_txt = music_font.render(f'effects : {self.volume_effects}%',False,self.white).convert()
                        
                        self.volume_time = get_time()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_s :

                    pygame.draw.rect(self.my_settings.screen,self.black,noir)

                    self.skin   = SkinSelect(self)
                    self.songs  = SongSelect(self)
                    self.sounds = ImportSounds(self.skin)
                    
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and key[pygame.K_LALT]) :
                    loop = False

                    MenuWrite(self)

                    pygame.quit()
                    exit(0)
