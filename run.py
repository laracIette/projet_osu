import glob
import pygame
from math import inf
import pygame.freetype
from gameend import Score
from settings import Settings
from sounds import ImportSounds
from tools import GetTime, Load, ReSize
from setthings import SetMultiplier, SetMap
from interface import DarkenScreen, HideUI, SetFps, SetShowOnScreen, ShowOnScreen, UItextRenders
from objects import GetCircle, GetFollowPoint, GetSpinner, SetCircles, SetFollowPoints, SetSpinners
from game import ApplyBreaks, ChangeOffset, EndGame, GameQuit, GetClicks, GetPause, SetBreak, StartGame, UnPause
from menu import DiffSelect, MapSelect, ModifyVolumes, MenuShowVolume, SetVolumeOffsetSkin, SkinSelect, SongSelect

class Run :

    def __init__(self,map,diff,songs,skin,sounds,volume,volume_music,volume_effects,offset,lines) :

        self.my_settings = Settings()

        self.wi = self.my_settings.width
        self.he = self.my_settings.height

        self.offset = offset
        self.songs  = songs
        self.diff   = diff
        self.map    = map
        self.lines  = lines
        self.skin   = skin

        self.sounds         = sounds
        self.volume         = volume
        self.volume_effects = volume_effects
        self.volume_music   = volume_music
        
        self.black  = (  0,  0,  0)
        self.white  = (255,255,255)
        self.grey   = ( 48, 48, 48)
        self.orange = (218,174, 70)
        self.green  = ( 87,227, 19)
        self.blue   = ( 50,188,231)

        if self.offset != 0 :
            self.show_offset = True
        else :
            self.show_offset = False

        self.offset_time = GetTime()

        SetMap(self)

        self.pause_screen = Load(f'skins\\{self.skin}\\pausescreen.png',(self.wi,self.he),False)
        self.end_screen   = Load(f'skins\\{self.skin}\\endscreen.png',(self.wi,self.he),False)
        self.bg           = pygame.transform.scale(self.songs[self.map][0],(self.wi,self.he)).convert()
        self.noir         = pygame.Rect(0,0,self.wi,self.he)
        #self.dim         = Load('images\\noir93.png',(self.wi,self.he),False)

        self.game_break = True
        self.break_lock = False
        
        self.c_s     = ReSize(121/self.cs*4.9)
        self.circle  = Load(f'skins\\{self.skin}\\hitcircle.png',(self.c_s,self.c_s),True)

        self.a_c_s    = self.c_s*4
        self.a_circle = Load(f'skins\\{self.skin}\\approachcircle.png',(self.a_c_s,self.a_c_s),True)

        self.cursor       = Load(f'skins\\{self.skin}\\cursor.png',(self.c_s,self.c_s),True)
        self.cursor_trail = Load(f'skins\\{self.skin}\\cursortrail.png',(self.c_s/4,self.c_s/4),True)
        self.trail_pos    = []
        self.trail_count  = 0

        self.spinner      = Load(f'skins\\{self.skin}\\spinner.png',(ReSize(400),ReSize(400)),True)
        self.spin         = 0
        self.show_spinner = False
        self.spin_tot     = 0
        self.spin_tot2    = 0

        self.pos  = pygame.mouse.get_pos()
        self.pos3 = pygame.mouse.get_pos()

        self.click_check = False

        self.fpss     = []
        self.avg_fps  = 0
        self.fps_time = GetTime()
        self.fps_font = pygame.font.SysFont('arial',round(ReSize(30)))

        self.number_font = pygame.font.Font('assets\\fonts\\LeagueSpartanBold.ttf',round(self.c_s/2))
        self.score_font  = pygame.freetype.SysFont('segoeuisemibold',round(75))
        
        self.acc       = []
        self.acc_check = False
        self.acc_font  = pygame.font.SysFont('segoeuisemibold',round(ReSize(45)))

        self.rep_font = pygame.freetype.SysFont('segoeuisemibold',round(ReSize(45)))
        
        self.show_acc = []
        self.acc_miss = Load(f'skins\\{self.skin}\\miss.png',(self.c_s/2,self.c_s/2),True)
        self.acc_100  = Load(f'skins\\{self.skin}\\100.png',(self.c_s/2,self.c_s/2),True)
        self.acc_50   = Load(f'skins\\{self.skin}\\50.png',(self.c_s/2,self.c_s/2),True)

        self.t_miss = 0
        self.t_300  = 0
        self.t_100  = 0
        self.t_50   = 0

        self.fade  = False
        self.faded = False

        self.start_time  = GetTime()
        self.paused_time = 0
        self.pause_time  = 0
        self.end_time    = inf

        self.cs_od_hp = self.cs + self.od + self.hp

        SetMultiplier(self)

        self.mod_multiplier = 1
        self.hit_value      = 0
        self.score          = 0
        self.combo          = 0
        self.combo_font     = pygame.font.SysFont('segoeuisemibold',round(ReSize(90)))

        self.max_health       = 600
        self.health           = self.max_health
        self.health_minus     = 50*self.hp/6
        self.passive_health   = self.health_minus/500
        self.spin_health      = self.max_health/300
        self.spinner_fade     = False
        self.health_bar_bg    = pygame.Rect(ReSize(20),ReSize(20),ReSize(600),ReSize(20))
        self.click_time       = 0
        self.click_time_check = False
        
        self.spin_score_bonus       = 0
        self.spin_score_bonus_time  = 0
        self.spin_score_bonus_alpha = 0

        self.ur_50     = pygame.Rect(ReSize(821),ReSize(1050),ReSize(278),ReSize(8))
        self.ur_100    = pygame.Rect(ReSize(875),ReSize(1050),ReSize(172),ReSize(8))
        self.ur_300    = pygame.Rect(ReSize(928),ReSize(1050),ReSize(66),ReSize(8))
        self.ur_middle = pygame.Rect(ReSize(959),ReSize(1039),ReSize(4),ReSize(30))
        self.show_ur   = []
        self.total_ur  = []

        self.followpoint  = Load(f'skins\\{self.skin}\\followpoint.png',(ReSize(128),ReSize(20)),True)
        self.followpoints = []

        self.show_circles      = []
        self.show_spinners     = []
        self.show_followpoints = []

        self.score_txt = self.combo_font.render('0',False,self.white).convert()
        self.combo_txt = self.combo_font.render('0',False,self.white).convert()
        self.acc_txt   = self.acc_font.render('100.00%',False,self.white).convert()

        self.music_start = GetTime() + self.start_offset
        self.playing     = False
        self.waiting     = False

        self.death   = False
        self.to_menu = False

        self.numbers = 0

        pygame.mixer.music.load(self.songs[self.map][1])
        pygame.mixer.music.set_volume(self.volume*self.volume_music/100)

        self.UI_alpha = 255
        self.UI       = True

        self.e = 0
        self.q = 0
        self.f = 0

        self.running = True
        while self.running :
            
            self.my_settings.clock.tick(self.my_settings.frequence)

            if self.waiting == False :

                if GetTime() - self.paused_time >= self.music_start and self.playing == False :
                
                    StartGame(self)

                GetSpinner(self)
                
                GetCircle(self)

                GetFollowPoint(self)

                ApplyBreaks(self)

                if GetTime() >= self.end_time + self.start_offset or self.health <= 0 :

                    EndGame(self)

                    if self.death == False :

                        Score(self)
        
                    pygame.mixer.music.unpause()
                    Menu()

            SetBreak(self)
                
            DarkenScreen(self)

            SetFollowPoints(self)

            SetCircles(self)
            
            UItextRenders(self)
            
            SetFps(self)
            
            SetShowOnScreen(self)
            
            SetSpinners(self)

            self.score_txt = self.combo_font.render(str(self.score),False,self.white).convert()

            ShowOnScreen(self)

            self.pos = pygame.mouse.get_pos()

            pygame.display.flip()
            
            self.key = pygame.key.get_pressed()
            for self.event in pygame.event.get() :

                if self.waiting == False :
                    GetClicks(self)

                else :
                    UnPause(self)
                        
                HideUI(self)

                ChangeOffset(self)

                GetPause(self)

                if self.to_menu :

                    Menu()
                
                GameQuit(self)

class Menu :

    def __init__(self) :

        pygame.mouse.set_visible(True)

        self.my_settings = Settings()

        self.wi = self.my_settings.width
        self.he = self.my_settings.height

        self.black  = (  0,  0,  0)
        self.white  = (255,255,255)

        self.noir = pygame.Rect(0,0,self.wi,self.he)
        self.font = pygame.font.Font('assets\\fonts\\shippori.ttf',round(ReSize(45)))
        
        SetVolumeOffsetSkin(self)

        self.songs  = SongSelect(self)
        self.sounds = ImportSounds(self.skin)

        self.show_volume = True

        self.volume_font = pygame.font.SysFont('arial',round(ReSize(60)))
        self.music_font  = pygame.font.SysFont('arial',round(ReSize(40)))

        self.volume_txt    = self.volume_font.render(f'main : {self.volume}%',False,self.white).convert()
        self.volume_rect   = self.volume_txt.get_rect()
        self.volume_rect.y = self.he-2*self.volume_txt.get_height()-ReSize(15)

        self.music_txt    = self.music_font.render(f'music : {self.volume_music}%',False,self.white).convert()
        self.music_rect   = self.music_txt.get_rect()
        self.music_rect.y = self.he-2*self.music_txt.get_height()

        self.effects_txt    = self.music_font.render(f'effects : {self.volume_effects}%',False,self.white).convert()
        self.effects_rect   = self.effects_txt.get_rect()
        self.effects_rect.y = self.he-self.effects_txt.get_height()

        self.volume_noir = pygame.Rect(self.wi/3*2,self.he/3*2,self.wi/3,self.he/3)
        
        self.volume_time = GetTime()

        self.diff_choice   = False
        self.choosing_diff = False

        loop = True
        while loop :

            self.my_settings.clock.tick(self.my_settings.frequence)
            
            pygame.display.flip()

            pygame.draw.rect(self.my_settings.screen,self.black,self.noir)
            
            for i in range(len(self.maps)) :

                bgs = glob.glob(f'{self.maps[i]}\\*.jpg')
                bg  = pygame.image.load(bgs[1]).convert()
                bg  = pygame.transform.scale(bg,(self.wi/5,self.he/5)).convert()

                self.my_settings.screen.blit(bg,(0,self.he/5*i))

            if self.choosing_diff :

                self.diffs = self.songs[self.map][3]
                for i in range(len(self.diffs)) :
            
                    diff = self.font.render(self.diffs[i],False,self.white).convert()
                    self.my_settings.screen.blit(diff,(self.wi/5,self.he/20*i+self.he/5*self.map))

                if self.event.type == pygame.MOUSEBUTTONDOWN and self.event.button == pygame.BUTTON_LEFT :

                    for self.diff in range(len(self.diffs)) :
                    
                        DiffSelect(self)

                        if self.diff_choice == True :
                            Run(self.map,self.diff,self.songs,self.skin,self.sounds,self.volume,self.volume_music,self.volume_effects,self.offset,self.lines)          

            MenuShowVolume(self)

            self.key = pygame.key.get_pressed()
            for self.event in pygame.event.get() :

                self.pos = pygame.mouse.get_pos()

                if self.event.type == pygame.MOUSEBUTTONDOWN :

                    if self.event.button == 4 or self.event.button == 5 :

                        ModifyVolumes(self)

                    if self.event.button == pygame.BUTTON_LEFT :

                        MapSelect(self)
                    
                if self.event.type == pygame.KEYDOWN and self.event.key == pygame.K_s :
                    self.skin = SkinSelect(self)

                if self.event.type == pygame.KEYDOWN and self.event.key == pygame.K_ESCAPE and self.choosing_diff :
                    self.choosing_diff = False
                    
                GameQuit(self)