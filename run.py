# bibliotheques systeme
import glob
import pygame
from math import inf
import pygame.freetype

# mes bibliotheques
from game import OsuGame
from menu import MenuTools
from settings import Settings
from objects import OsuObjects
from sounds import ImportSounds
from setthings import OsuSetThings
from interface import OsuInterface
from tools import GetTime, Load, ReSize
from gameend import OsuGameEnd, GameQuit

class Osu : # classe correspondante a une partie (une seule map)

    def __init__(self,menu) :

        self.my_settings = Settings()

        self.wi = self.my_settings.width
        self.he = self.my_settings.height

        self.menu = menu

        self.mod_list = menu.mod_list
        self.offset   = menu.offset
        self.songs    = menu.songs
        self.diff     = menu.diff
        self.map      = menu.map
        self.lines    = menu.lines
        self.skin     = menu.skin

        self.map_name  = menu.map_names[menu.map]
        self.diff_name = menu.diffs[menu.diff]

        self.sounds         = menu.sounds
        self.volume         = menu.volume
        self.volume_effects = menu.volume_effects
        self.volume_music   = menu.volume_music
        
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

        OsuSetThings.SetMap(self)

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

        OsuSetThings.SetMultiplier(self)

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
        self.to_menu = False

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
                
                    OsuGame.StartGame(osu)

                OsuObjects.GetSpinner(osu)
                
                OsuObjects.GetCircle(osu)

                OsuObjects.GetFollowPoint(osu)

                OsuGame.ApplyBreaks(osu)

                if GetTime() >= osu.end_time + osu.start_offset or osu.health <= 0 :

                    OsuGame.EndGame(osu)
                    pygame.mixer.music.unpause()

                    if osu.death == False :

                        OsuGameEnd.Score(osu)
        
                    Menu.MenuChoice(osu.menu,osu.mod_list)

            OsuGame.SetBreak(osu)
                
            OsuInterface.DarkenScreen(osu)
            
            OsuObjects.SetFollowPoints(osu)

            OsuObjects.SetCircles(osu)
            
            OsuInterface.UItextRenders(osu)
            
            OsuInterface.SetFps(osu)
            
            OsuInterface.SetShowOnScreen(osu)
            
            OsuObjects.SetSpinners(osu)

            osu.score_txt = osu.combo_font.render(str(osu.score),False,osu.white).convert()

            OsuInterface.ShowOnScreen(osu)

            osu.pos = pygame.mouse.get_pos()

            pygame.display.flip()
            
            osu.key = pygame.key.get_pressed()
            for osu.event in pygame.event.get() :

                if osu.waiting == False :
                    OsuGame.GetClicks(osu)

                else :
                    OsuGame.UnPause(osu)
                        
                OsuInterface.HideUI(osu)

                OsuGame.ChangeOffset(osu)

                OsuGame.GetPause(osu)

                if osu.to_menu :

                    Menu.MenuChoice(osu.menu,osu.mod_list)
                
                GameQuit(osu)

class Menu : # classe correspondante au menu du jeu

    def __init__(self) :

        pygame.mouse.set_visible(True)

        self.my_settings = Settings()

        self.wi = self.my_settings.width
        self.he = self.my_settings.height

        self.black  = (  0,  0,  0)
        self.white  = (255,255,255)

        self.noir = pygame.Rect(0,0,self.wi,self.he)
        self.font = pygame.font.Font("assets\\fonts\\shippori.ttf",round(ReSize(45)))
        
        MenuTools.SetVolumeOffsetSkinMod(self)

        self.songs  = MenuTools.SongSelect(self)
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
        
        MenuTools.GetMods(self)

        self.loop = True

    def MenuChoice(menu,mod_list) : # determine les options a prendre en compte pour le lancement d'une partie

        menu.mod_list = mod_list
        while menu.loop :

            menu.my_settings.clock.tick(menu.my_settings.frequence)
            pygame.display.flip()

            pygame.draw.rect(menu.my_settings.screen,menu.black,menu.noir)
            
            for i in range(len(menu.maps)) :

                bgs = glob.glob(f"{menu.maps[i]}\\*.jpg")
                bg  = pygame.image.load(bgs[0]).convert()
                bg  = pygame.transform.scale(bg,(menu.wi/5,menu.he/5)).convert()

                menu.my_settings.screen.blit(bg,(0,menu.he/5*i))

            if menu.choosing_diff :

                menu.diffs = menu.songs[menu.map][3]
                for i in range(len(menu.diffs)) :
            
                    diff = menu.font.render(menu.diffs[i],False,menu.white).convert()
                    menu.my_settings.screen.blit(diff,(menu.wi/5,menu.he/20*i+menu.he/5*menu.map))

                if menu.event.type == pygame.MOUSEBUTTONDOWN and menu.event.button == pygame.BUTTON_LEFT :

                    for menu.diff in range(len(menu.diffs)) :
                    
                        MenuTools.DiffSelect(menu)

                        if menu.diff_choice == True :

                            menu.diff_choice   = False
                            menu.choosing_diff = False

                            osu = Osu(menu)
                            osu.OsuRun()

            MenuTools.ShowVolume(menu)

            menu.key = pygame.key.get_pressed()
            for menu.event in pygame.event.get() :

                menu.pos = pygame.mouse.get_pos()

                if menu.event.type == pygame.MOUSEBUTTONDOWN :

                    if menu.event.button == 4 or menu.event.button == 5 :

                        MenuTools.ModifyVolumes(menu)

                    if menu.event.button == pygame.BUTTON_LEFT :

                        MenuTools.MapSelect(menu)
                    
                if menu.event.type == pygame.KEYDOWN and menu.event.key == pygame.K_s :
                    menu.skin = MenuTools.SkinSelect(menu)

                if menu.event.type == pygame.KEYDOWN and menu.event.key == pygame.K_F1 :
                    menu.mod_list = MenuTools.ModChoice(menu)

                if menu.event.type == pygame.KEYDOWN and menu.event.key == pygame.K_ESCAPE and menu.choosing_diff :
                    menu.choosing_diff = False
                    
                GameQuit(menu)