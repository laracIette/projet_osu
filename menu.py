import pygame
import glob
import os
from sounds import Play

from tools import get_time

def SkinSelect(self) :

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

                pygame.quit()
                exit(0)

def SongSelect(self) :

    maps  = glob.glob('assets\\songs\\*')
    self.songs = []

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
        bg = pygame.transform.scale(bg,(self.wi,self.he)).convert()
        
        self.songs.append([bg,audio,diffs,diff_names])

        bg = pygame.image.load(bgs[1]).convert()
        bg = pygame.transform.scale(bg,(self.wi/5,self.he/5)).convert()
        self.my_settings.screen.blit(bg,(0,self.he/5*i))

    return self.songs

def MenuWrite(self) :

    with open('assets\\settings.txt','w') as settings_file :
                                            
        modifs = [self.offset,self.volume,self.volume_music,self.volume_effects]

        for a in range(len(self.lines)) :

            settings_file.write(self.lines[a].replace(self.lines[a],f'{modifs[a]}\n'))

def MenuShowVolume(self) :

    if self.show_volume :
            
        pygame.draw.rect(self.my_settings.screen,self.black,self.volume_noir)

        if get_time() >= self.volume_time + 1000 :
            self.show_volume = False
            return 0

        self.volume_rect.x = self.wi-self.volume_txt.get_width()
        self.music_rect.x = self.wi-self.music_txt.get_width()
        self.effects_rect.x = self.wi-self.effects_txt.get_width()

        self.my_settings.screen.blit(self.volume_txt,(self.volume_rect.x,self.volume_rect.y))
        self.my_settings.screen.blit(self.music_txt,(self.music_rect.x,self.music_rect.y))
        self.my_settings.screen.blit(self.effects_txt,(self.effects_rect.x,self.effects_rect.y))

def SetVolumes(self) :

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

            a += 1
                    
    self.volumes = [self.volume,self.volume_music,self.volume_effects]