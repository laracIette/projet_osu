import os
import glob
import pygame
from sounds import Play
from gameend import Write
from tools import GetTime

def SkinSelect(self) : # selection du skin

    pygame.draw.rect(self.my_settings.screen,self.black,self.noir)

    skins0 = []
    skins  = glob.glob('assets\\skins\\*')
    for i in skins :
        skins0.append(os.path.basename(i))
    
    skins = []
    for z in range(len(skins0)) :

        text = self.font.render(skins0[z],False,self.white)
        self.my_settings.screen.blit(text,(0,self.he/15*z))

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
                    skin1_rect.y = self.he/15*w

                    if skin1_rect.collidepoint(pos) :
                        loop = False

                        Play(self.sounds,'click',1,self.volume,self.volume_effects)
                        
                        self.skin = skins0[w]

                return self.skin

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE :

                return self.skin

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and key[pygame.K_LALT]) :
                loop = False

                Write(self)

                pygame.quit()
                exit(0)

def SongSelect(self) : # definition des maps possibles

    self.maps  = glob.glob('assets\\songs\\*')
    self.songs = []

    for i in range(len(self.maps)) :

        audio = glob.glob(f'{self.maps[i]}\\*.mp3')
        audio = audio[0]
        
        self.map_names = []
        for j in self.maps :

            self.map_names.append(os.path.basename(j))

        diffs = []
        diff  = glob.glob(f'{self.maps[i]}\\*.txt')
        for v in range(len(diff)) :
            diffs.append(diff[v])

        diff_names = []
        for u in diffs :

            diff_names.append(os.path.basename(os.path.splitext(u)[0]))

        bgs = glob.glob(f'{self.maps[i]}\\*.jpg')
        bg  = pygame.image.load(bgs[0]).convert()
        bg  = pygame.transform.scale(bg,(self.wi,self.he)).convert()
        
        self.songs.append([bg,audio,diffs,diff_names])

    return self.songs

def MenuShowVolume(self) : # affiche le volume dans le menu

    if self.show_volume :
            
        pygame.draw.rect(self.my_settings.screen,self.black,self.volume_noir)

        if GetTime() >= self.volume_time + 1000 :
            self.show_volume = False
            return 0

        self.volume_rect.x  = self.wi-self.volume_txt.get_width()
        self.music_rect.x   = self.wi-self.music_txt.get_width()
        self.effects_rect.x = self.wi-self.effects_txt.get_width()

        self.my_settings.screen.blit(self.volume_txt,(self.volume_rect.x,self.volume_rect.y))
        self.my_settings.screen.blit(self.music_txt,(self.music_rect.x,self.music_rect.y))
        self.my_settings.screen.blit(self.effects_txt,(self.effects_rect.x,self.effects_rect.y))

def SetVolumeOffsetSkin(self) : # recupere et attribut les donnees de settings.txt

    with open('assets\\settings.txt','r') as settings_file :

        a = 0

        self.lines = settings_file.readlines()
        for i in self.lines :

            if a == 0 :

                self.offset = int(i)
            
            if a == 1 :

                self.volume = int(i)
            
            if a == 2 :

                self.volume_music = int(i)

            if a == 3 :

                self.volume_effects = int(i)

            if a == 4 :

                skin_t = []
                for s in self.lines[a] :
                    if s != '\n' :
                        skin_t.append(s)
                self.skin = ''.join(skin_t)

            a += 1
                    
    self.volumes = [self.volume,self.volume_music,self.volume_effects]

def ModifyVolumes(self) : # detecte si besoin et applique changement de volume

    rects = [self.volume_rect,self.music_rect,self.effects_rect]

    for i in range(len(rects)) :

        if rects[i].collidepoint(self.pos) :
        
            if self.event.button == 4 :

                if self.volumes[i] < 100 :

                    self.volumes[i] += 1

            if self.event.button == 5 :

                if self.volumes[i] > 0 :

                    self.volumes[i] -= 1

    self.show_volume = True

    self.volume         = self.volumes[0]
    self.volume_music   = self.volumes[1]
    self.volume_effects = self.volumes[2]

    self.volume_txt  = self.volume_font.render(f'main : {self.volume}%',False,self.white).convert()
    self.music_txt   = self.music_font.render(f'music : {self.volume_music}%',False,self.white).convert()
    self.effects_txt = self.music_font.render(f'effects : {self.volume_effects}%',False,self.white).convert()
    
    self.volume_time = GetTime()

def MapSelect(self) : # selection de la map

    for self.ii in range(len(self.songs)) :

        song = self.songs[self.ii][0]
        song = pygame.transform.scale(song,(self.wi/5,self.he/5)).convert()

        song_rect   = song.get_rect()
        song_rect.y = self.my_settings.height/5*self.ii

        if song_rect.collidepoint(self.pos) :

            self.choosing_diff = True
            self.map = self.ii

            Play(self.sounds,'click',1,self.volume,self.volume_effects)

def DiffSelect(self) : # selection de la difficulte

    diff = self.font.render(self.diffs[self.diff],False,self.white).convert()

    diff_rect   = diff.get_rect()
    diff_rect.x = self.wi/5
    diff_rect.y = self.he/20*self.diff+self.he/5*self.map

    if diff_rect.collidepoint(self.pos) :
        self.diff_choice = True

        Play(self.sounds,'click',1,self.volume,self.volume_effects)
        pygame.mouse.set_visible(False)