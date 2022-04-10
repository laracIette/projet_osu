# bibliotheques systeme
import pygame
from math import inf
import pygame.freetype

# mes classes

# Osu
from game import OsuGame
from objects import OsuObjects
from gameend import OsuGameEnd
from setthings import OsuSetThings
from interface import OsuInterface

# Menu
from menu import MenuTools

# general
from gameend import GameQuit
from settings import Settings
from sounds import ImportSounds
from tools import GetTime, Load, ReSize

class Osu(OsuGame,OsuObjects,OsuGameEnd,OsuInterface,OsuSetThings) : # classe correspondante a une partie

    def __init__(self,menu) :

        self.my_settings = Settings()

        self.wi = self.my_settings.width
        self.he = self.my_settings.height

        self.menu = menu

        self.mod_list = menu.mod_list
        self.offset   = menu.offset
        self.songs    = menu.songs
        self.lines    = menu.lines
        self.skin     = menu.skin
        self.diff     = menu.diff
        self.map      = menu.map

        self.map_name  = menu.map_name
        self.diff_name = menu.diff_name

        self.sounds         = menu.sounds
        self.volume         = menu.volume
        self.volume_music   = menu.volume_music
        self.volume_effects = menu.volume_effects
        
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

        self.SetMap()

        self.pause_screen = Load(f"skins\\{self.skin}\\pausescreen.png",(self.wi,self.he),False)
        self.end_screen   = Load(f"skins\\{self.skin}\\endscreen.png",(self.wi,self.he),False)
        self.dim          = Load("images\\noir93.png",(self.wi,self.he),False)
        self.bg           = pygame.transform.scale(self.songs[self.map][0],(self.wi,self.he)).convert()
        self.noir         = pygame.Rect(0,0,self.wi,self.he)

        self.game_break = True
        self.break_lock = False
        
        self.c_s     = round(ReSize(218 - self.cs*18))
        self.circle  = Load(f"skins\\{self.skin}\\hitcircle.png",(self.c_s,self.c_s),True)

        self.a_c_s    = self.c_s*4
        self.a_circle = Load(f"skins\\{self.skin}\\approachcircle.png",(self.a_c_s,self.a_c_s),True)

        self.cursor       = Load(f"skins\\{self.skin}\\cursor.png",(self.c_s,self.c_s),True)
        self.cursor_trail = Load(f"skins\\{self.skin}\\cursortrail.png",(self.c_s/3.3,self.c_s/3.3),True)
        self.trail_pos    = []
        self.trail_count  = 0

        self.spinner      = Load(f"skins\\{self.skin}\\spinner.png",(ReSize(400),ReSize(400)),True)
        self.spin         = 0
        self.show_spinner = False
        self.spin_tot     = 0
        self.spin_tot2    = 0

        self.pos = pygame.mouse.get_pos()

        self.click_check = False

        self.fpss     = []
        self.avg_fps  = 0
        self.fps_time = GetTime()
        self.fps_font = pygame.font.SysFont("arial",round(ReSize(30)))

        self.number_font = pygame.font.Font("assets\\fonts\\LeagueSpartanBold.ttf",round(self.c_s/2))
        self.score_font  = pygame.freetype.SysFont("segoeuisemibold",round(75))
        
        self.acc       = []
        self.acc_check = False
        self.acc_font  = pygame.font.SysFont("segoeuisemibold",round(ReSize(45)))

        self.rep_font = pygame.freetype.SysFont("segoeuisemibold",round(ReSize(45)))
        
        self.show_acc = []
        self.acc_miss = Load(f"skins\\{self.skin}\\miss.png",(self.c_s/2,self.c_s/2),True)
        self.acc_100  = Load(f"skins\\{self.skin}\\100.png",(self.c_s/2,self.c_s/2),True)
        self.acc_50   = Load(f"skins\\{self.skin}\\50.png",(self.c_s/2,self.c_s/2),True)

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

        self.SetMultiplier()

        self.mod_multiplier = 1
        self.hit_value      = 0
        self.score          = 0
        self.combo          = 0
        self.max_combo      = 0
        self.combo_font     = pygame.font.SysFont("segoeuisemibold",round(ReSize(90)))

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

        self.followpoint  = Load(f"skins\\{self.skin}\\followpoint.png",(ReSize(128),ReSize(20)),True)
        self.followpoints = []

        self.show_circles      = []
        self.show_spinners     = []
        self.show_followpoints = []

        self.score_txt = self.combo_font.render("0",False,self.white).convert()
        self.combo_txt = self.combo_font.render("0",False,self.white).convert()
        self.acc_txt   = self.acc_font.render("100.00%",False,self.white).convert()

        self.music_start = GetTime() + self.start_offset
        self.playing     = False
        self.waiting     = False

        self.replay_clicks = []

        self.death   = False

        self.numbers = 0

        pygame.mixer.music.load(self.songs[self.map][1])
        pygame.mixer.music.set_volume(self.volume*self.volume_music/100)

        self.UI_alpha = 255
        self.UI       = True

        self.c_num = 0
        self.s_num = 0
        self.f_num = 0

        self.running = True

    def OsuRun(osu) : # deroulement de la partie

        while osu.running :
            
            osu.my_settings.clock.tick(osu.my_settings.frequence)

            if osu.waiting == False :
    
                if GetTime() - osu.paused_time >= osu.music_start and osu.playing == False :
                
                    osu.StartGame()

                osu.GetSpinner()
                
                osu.GetCircle()

                osu.GetFollowPoint() # verifie si doit afficher un trait entre 2 cercles, si oui le cree

                osu.ApplyBreaks()

                if GetTime() >= osu.end_time + osu.start_offset or osu.health <= 0 :

                    osu.EndGame()

            osu.SetBreak()
                
            osu.DarkenScreen()
            
            osu.SetFollowPoints()

            osu.SetCircles()
            
            osu.UItextRenders()
            
            osu.SetFps()
            
            osu.SetShowOnScreen()
            
            osu.SetSpinners()

            osu.score_txt = osu.combo_font.render(str(osu.score),False,osu.white).convert()

            osu.ShowOnScreen()

            pygame.display.flip()
            
            osu.pos = pygame.mouse.get_pos()
            osu.key = pygame.key.get_pressed()
            for osu.event in pygame.event.get() :

                if osu.waiting == False :
                    osu.GetClicks()

                else :
                    osu.UnPause()
                        
                osu.HideUI()

                osu.ChangeOffset()

                osu.GetPause()
                
                GameQuit(osu)

class Menu(MenuTools) : # classe correspondante au menu du jeu

    def __init__(self) :

        self.my_settings = Settings()

        self.wi = self.my_settings.width
        self.he = self.my_settings.height

        self.black  = (  0,  0,  0)
        self.white  = (255,255,255)

        self.noir = pygame.Rect(0,0,self.wi,self.he)
        self.font = pygame.font.Font("assets\\fonts\\shippori.ttf",round(ReSize(45)))
        
        self.SetVolumeOffsetSkinMod()

        self.songs  = self.SongSelect()
        self.sounds = ImportSounds(self.skin)

        self.show_volume = True

        self.volume_font = pygame.font.SysFont("arial",round(ReSize(60)))
        self.music_font  = pygame.font.SysFont("arial",round(ReSize(40)))

        self.volume_txt    = self.volume_font.render(f"main : {self.volume}%",False,self.white).convert()
        self.volume_rect   = self.volume_txt.get_rect()
        self.volume_rect.y = self.he-2*self.volume_txt.get_height()-ReSize(15)

        self.music_txt    = self.music_font.render(f"music : {self.volume_music}%",False,self.white).convert()
        self.music_rect   = self.music_txt.get_rect()
        self.music_rect.y = self.he-2*self.music_txt.get_height()

        self.effects_txt    = self.music_font.render(f"effects : {self.volume_effects}%",False,self.white).convert()
        self.effects_rect   = self.effects_txt.get_rect()
        self.effects_rect.y = self.he-self.effects_txt.get_height()

        self.volume_noir = pygame.Rect(self.wi/3*2,self.he/3*2,self.wi/3,self.he/3)
        
        self.volume_time = GetTime()
        
        self.diff_choice   = False
        self.choosing_diff = False
        
        self.GetMods()

        self.loop = True

    def MenuChoice(menu,mod_list) : # determine les options a prendre en compte pour le lancement d'une partie

        pygame.mouse.set_visible(True)

        menu.mod_list = mod_list
        
        while menu.loop :

            menu.my_settings.clock.tick(menu.my_settings.frequence)

            menu.ShowOnScreen()
                
            if menu.choosing_diff :

                menu.DiffSelect()

                if menu.diff_choice :
                    menu.diff_choice = False

                    Osu(menu).OsuRun()
                    
            pygame.display.flip()

            menu.key = pygame.key.get_pressed()
            for menu.event in pygame.event.get() :

                menu.pos = pygame.mouse.get_pos()

                if menu.event.type == pygame.MOUSEBUTTONDOWN :

                    if menu.event.button == 4 or menu.event.button == 5 :

                        menu.ModifyVolumes()

                    if menu.event.button == pygame.BUTTON_LEFT :

                        menu.MapSelect()
                    
                if menu.event.type == pygame.KEYDOWN and menu.event.key == pygame.K_s :
                    menu.skin = menu.SkinSelect()

                if menu.event.type == pygame.KEYDOWN and menu.event.key == pygame.K_F1 :
                    menu.mod_list = menu.ModChoice()

                if menu.event.type == pygame.KEYDOWN and menu.event.key == pygame.K_ESCAPE and menu.choosing_diff :
                    menu.choosing_diff = False
                    
                GameQuit(menu)