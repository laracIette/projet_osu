# bibliotheques systeme
import pygame
from math import inf
import pygame.freetype

# mes classes

# Osu
from game import OsuGame
from objects import OsuObjects
from setthings import OsuSetThings
from interface import OsuInterface

# Menu
from mods import MenuMods
from menu import MenuTools

# general
from tools import Tools
from sounds import Sounds
from gameend import GameEnd
from settings import Settings

class Osu( OsuGame, OsuObjects, GameEnd, OsuInterface, OsuSetThings, Settings, Tools, Sounds ) : # classe correspondante a une partie

    def __init__( self, menu ) -> None :

        super().__init__()

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

        self.black  = (  0,   0,   0)
        self.white  = (255, 255, 255)
        self.grey   = ( 48,  48,  48)
        self.orange = (218, 174,  70)
        self.green  = ( 87, 227,  19)
        self.blue   = ( 50, 188, 231)

        if self.offset != 0 :
            self.show_offset = True
        else :
            self.show_offset = False

        self.offset_time = self.getTime() # temps actuel en millisecondes

        self.setMap()         # determine et classe dans des tableau les elements a afficher pendant une partie
        self.setMultiplier()  # multiplicateur pris en compte lors du calcul du score
        self.setMods()        # active les mods necessaires

        self.pause_screen = self.load( f"skins\\{self.skin}\\pausescreen.png", (self.width, self.height), False )
        self.end_screen   = self.load( f"skins\\{self.skin}\\endscreen.png", (self.width, self.height), False )
        self.dim          = self.load( "images\\noir93.png", (self.width, self.height), False )
        self.bg           = pygame.transform.scale( self.songs[self.map][0], (self.width, self.height) ).convert()
        self.noir         = pygame.Rect( 0, 0, self.width, self.height )

        self.game_break = True
        self.break_lock = False

        self.c_s     = round( self.reSize( 218 - self.cs*18 ) )
        self.circle  = self.load( f"skins\\{self.skin}\\hitcircle.png", (self.c_s, self.c_s), True )

        self.a_c_s    = self.c_s*4
        self.a_circle = self.load( f"skins\\{self.skin}\\approachcircle.png", (self.a_c_s, self.a_c_s), True )

        self.cursor       = self.load( f"skins\\{self.skin}\\cursor.png", (self.c_s, self.c_s), True )
        self.cursor_trail = self.load( f"skins\\{self.skin}\\cursortrail.png", (self.c_s/3.3, self.c_s/3.3), True )
        self.trail_pos    = []
        self.trail_count  = 0

        self.spinner      = self.load( f"skins\\{self.skin}\\spinner.png", (self.reSize( 400 ), self.reSize( 400 )), True )
        self.spin         = 0
        self.show_spinner = False
        self.spin_tot     = 0
        self.spin_tot2    = 0

        self.pos = pygame.mouse.get_pos()

        self.click_check = False

        self.fpss     = []
        self.avg_fps  = 0
        self.fps_time = self.getTime()
        self.fps_font = pygame.font.SysFont( "arial", round( self.reSize( 30 ) ) )

        self.number_font = pygame.font.Font( "assets\\fonts\\LeagueSpartanBold.ttf", round( self.c_s/2 ) )
        self.score_font  = pygame.freetype.SysFont( "segoeuisemibold", round( 75 ) )

        self.acc       = []
        self.acc_check = False
        self.acc_font  = pygame.font.SysFont( "segoeuisemibold", round( self.reSize( 45 ) ) )

        self.rep_font = pygame.freetype.SysFont( "segoeuisemibold", round( self.reSize( 45 ) ) )

        self.show_acc = []
        self.acc_miss = self.load( f"skins\\{self.skin}\\miss.png", (self.c_s/2, self.c_s/2), True )
        self.acc_100  = self.load( f"skins\\{self.skin}\\100.png", (self.c_s/2, self.c_s/2), True )
        self.acc_50   = self.load( f"skins\\{self.skin}\\50.png", (self.c_s/2, self.c_s/2), True )

        self.t_miss = 0
        self.t_300  = 0
        self.t_100  = 0
        self.t_50   = 0

        self.fade  = False
        self.faded = False

        self.start_time  = self.getTime()
        self.paused_time = 0
        self.pause_time  = 0
        self.end_time    = inf

        self.mod_multiplier = 1
        self.hit_value      = 0
        self.score          = 0
        self.combo          = 0
        self.max_combo      = 0
        self.combo_font     = pygame.font.SysFont( "segoeuisemibold", round( self.reSize( 90 ) ) )

        self.max_health       = 600
        self.health           = self.max_health
        self.health_minus     = 50*self.hp/6
        self.passive_health   = self.health_minus/500
        self.spin_health      = self.max_health/300
        self.spinner_fade     = False
        self.health_bar_bg    = pygame.Rect( self.reSize( 20 ), self.reSize( 20 ), self.reSize( 600 ), self.reSize( 20 ) )
        self.click_time       = 0
        self.click_time_check = False

        self.spin_score_bonus       = 0
        self.spin_score_bonus_time  = 0
        self.spin_score_bonus_alpha = 0

        self.ur_50     = pygame.Rect( self.reSize( 821 ), self.reSize( 1050 ), self.reSize( 278 ), self.reSize( 8 ) )
        self.ur_100    = pygame.Rect( self.reSize( 875 ), self.reSize( 1050 ), self.reSize( 172 ), self.reSize( 8 ) )
        self.ur_300    = pygame.Rect( self.reSize( 928 ), self.reSize( 1050 ), self.reSize( 66 ),  self.reSize( 8 ) )
        self.ur_middle = pygame.Rect( self.reSize( 959 ), self.reSize( 1039 ), self.reSize( 4 ),   self.reSize( 30 ) )
        self.show_ur   = []
        self.total_ur  = []

        self.followpoint  = self.load( f"skins\\{self.skin}\\followpoint.png", (self.reSize( 128 ), self.reSize( 20 ) ), True )
        self.followpoints = []

        self.show_circles      = []
        self.show_spinners     = []
        self.show_followpoints = []

        self.score_txt = self.combo_font.render( "0", False, self.white ).convert()
        self.combo_txt = self.combo_font.render( "0", False, self.white ).convert()
        self.acc_txt   = self.acc_font.render( "100.00%", False, self.white ).convert()

        self.music_start = self.getTime() + self.start_offset
        self.playing     = False
        self.waiting     = False

        self.replay_clicks = []

        self.death = False

        self.numbers = 0

        pygame.mixer.music.load( self.songs[self.map][1] )
        pygame.mixer.music.set_volume( self.volume*self.volume_music/100 )

        self.UI_alpha = 255
        self.UI       = True

        self.c_num = 0
        self.s_num = 0
        self.f_num = 0

        self.running = True

    def osuRun( osu ) -> None : # deroulement de la partie, osu est l'instance de la classe Osu

        while osu.running :

            osu.clock.tick( osu.frequence )

            if osu.waiting == False :

                if osu.getTime() - osu.paused_time >= osu.music_start and osu.playing == False :

                    osu.startGame()    # demarrage de la partie

                osu.getSpinner()       # verifie si doit afficher un spinner, si oui le cree

                osu.getCircle()        # verifie si doit afficher un cercle, si oui le cree

                osu.getFollowPoint()   # verifie si doit afficher un followpoint, si oui le cree
                                       # un followpoint est un element reliant 2 cercles

                osu.applyBreaks()      # declenche les pauses automatiques dans la partie

                if osu.getTime() >= osu.end_time + osu.start_offset or osu.health <= 0 :

                    osu.endGame()      # terminer la partie

            osu.setBreak()             # determine les pauses manuelles dans la partie

            osu.darkenScreen()         # assombri/eclairci l'ecran en fonction des pauses

            osu.setFollowPoints()      # affiche et modifie le/les followpoints

            osu.setCircles()           # affiche et modifie le/les cercles

            osu.UItextRenders()        # affiche les elements texte de la partie

            osu.setFps()               # calcule et affiche les fps

            osu.setShowOnScreen()      # determine des elements a afficher pendant une partie

            osu.setSpinners()          # affiche et modifie le/les spinners si mouvement

            osu.score_txt = osu.combo_font.render(str(osu.score),False,osu.white).convert()

            osu.showOnScreen()         # affichage des elements de la partie

            pygame.display.flip()      # met a jour les elements affiches sur l'ecran

            osu.pos = pygame.mouse.get_pos()
            osu.key = pygame.key.get_pressed()
            for osu.event in pygame.event.get() :

                if osu.waiting == False :
                    osu.getClicks()    # capte les touches clavier pouvant interagir avec un objet de la partie
                else :
                    osu.unpause()      # verifie et si possible quitte la pause

                osu.hideUI()           # cache/montre l'interface

                osu.changeOffset()     # detecte si le joueur presse les touche de + ou - d'offset et l'applique

                osu.getpause()         # captation des touches necessaires a la pause de la partie

                osu.gameQuit()         # quitte la partie et le programme

class Menu( MenuTools, Settings, Tools, Sounds, GameEnd, MenuMods ) : # classe correspondante au menu du jeu

    def __init__( self ) -> None :

        super().__init__()

        self.black  = (  0,   0,   0)
        self.white  = (255, 255, 255)

        self.noir = pygame.Rect( 0, 0, self.width, self.height )
        self.font = pygame.font.Font( "assets\\fonts\\shippori.ttf", round( self.reSize( 45 ) ) )

        self.setVolumeOffsetSkinMod()     # recupere et attribut les donnees de settings.txt
        self.songSelect()                 # definition des maps possibles
        self.importSounds()               # importe les sons selon le skin

        self.show_volume = True

        self.volume_font = pygame.font.SysFont( "arial", round( self.reSize( 60 ) ) )
        self.music_font  = pygame.font.SysFont( "arial", round( self.reSize( 40 ) ) )

        self.volume_txt    = self.volume_font.render( f"main : {self.volume}%", False, self.white ).convert()
        self.volume_rect   = self.volume_txt.get_rect()
        self.volume_rect.y = self.height - 2*self.volume_txt.get_height() - self.reSize( 15 )

        self.music_txt    = self.music_font.render( f"music : {self.volume_music}%", False, self.white ).convert()
        self.music_rect   = self.music_txt.get_rect()
        self.music_rect.y = self.height - 2*self.music_txt.get_height()

        self.effects_txt    = self.music_font.render( f"effects : {self.volume_effects}%", False, self.white ).convert()
        self.effects_rect   = self.effects_txt.get_rect()
        self.effects_rect.y = self.height - self.effects_txt.get_height()

        self.volume_noir = pygame.Rect( self.width/3*2, self.height/3*2, self.width/3, self.height/3 )

        self.volume_time = self.getTime() # temps actuel en millisecondes

        self.diff_choice   = False
        self.choosing_diff = False

        self.getMods() # definit les modes de jeu

        self.running = True

    def menuChoice( menu, mod_list = [] ) -> None : # determine les options a prendre en compte pour le lancement d'une partie
                                                    # menu est l'instance de la classe Menu

        pygame.mouse.set_visible( True )

        menu.mod_list = mod_list

        while menu.running :

            menu.clock.tick( menu.frequence )

            menu.showOnScreen()   # affichage des elements du menu

            if menu.choosing_diff :

                menu.diffSelect() # selection de la difficulte

                if menu.diff_choice :
                    menu.diff_choice = False

                    menu.setModList()

                    Osu( menu ).osuRun() # lance la partie en envoyant les elements de l'instance de Menu

            pygame.display.flip()

            menu.key = pygame.key.get_pressed()
            for menu.event in pygame.event.get() :

                menu.pos = pygame.mouse.get_pos()

                if menu.event.type == pygame.MOUSEBUTTONDOWN :

                    if menu.event.button == 4 or menu.event.button == 5 :

                        menu.modifyVolumes()           # detecte si besoin et applique changement de volume

                    if menu.event.button == pygame.BUTTON_LEFT :

                        menu.mapSelect()               # selection de la map

                if menu.event.type == pygame.KEYDOWN and menu.event.key == pygame.K_s :

                    menu.skin = menu.skinSelect()      # selection du skin

                if menu.event.type == pygame.KEYDOWN and menu.event.key == pygame.K_F1 :

                    menu.mod_list = menu.modChoice()   # choisir un mode de jeu

                if menu.event.type == pygame.KEYDOWN and menu.event.key == pygame.K_ESCAPE and menu.choosing_diff :

                    menu.choosing_diff = False

                menu.gameQuit() # quitte le menu et le programme