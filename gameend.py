from datetime import datetime
import pygame
from tools import ReSize

def ProposeOffset(self) : # propose un offset au joueur si possible

    pygame.mouse.set_visible(True)

    ur_moy = 0

    if self.total_ur != [] :

        noir = pygame.Rect(0,0,self.wi,self.he)
        pygame.draw.rect(self.my_settings.screen,(0,0,0),noir)
        
        for u in self.total_ur :
            ur_moy += u

        ur_moy /= len(self.total_ur)
        ur_moy = round(ur_moy)

        if ur_moy < 0 :
            rep_txt = f'You are tapping {abs(ur_moy)}ms earlier, do you want to apply a negative offset of {abs(ur_moy)}ms ?'
        
        if ur_moy > 0 :
            rep_txt = f'You are tapping {abs(ur_moy)}ms too late, do you want to apply a positive offset of {abs(ur_moy)}ms ?'

        rep_rect        = self.rep_font.get_rect(rep_txt)
        rep_rect.center = (self.wi/2,self.he/2)

        yes_txt         = 'Yes'
        yes_rect        = self.rep_font.get_rect(yes_txt)
        yes_rect.center = (self.wi/3,self.he/3*2)

        no_txt         = 'No'
        no_rect        = self.rep_font.get_rect(no_txt)
        no_rect.center = (self.wi/3*2,self.he/3*2)
        
        self.rep_font.render_to(self.my_settings.screen,rep_rect,rep_txt,self.white)
        self.rep_font.render_to(self.my_settings.screen,yes_rect,yes_txt,self.white)
        self.rep_font.render_to(self.my_settings.screen,no_rect,no_txt,self.white)
        
        pygame.display.flip()
        
        loop = True
        while loop :

            self.key = pygame.key.get_pressed()
            for self.event in pygame.event.get() :

                GameQuit(self)

                if self.event.type == pygame.KEYDOWN and self.event.key == pygame.K_F2 :

                    WriteReplay(self)

                if self.event.type == pygame.MOUSEBUTTONDOWN and self.event.button == pygame.BUTTON_LEFT :

                    pos = pygame.mouse.get_pos()

                    if yes_rect.collidepoint(pos) :
                        
                        offset = - ur_moy

                        return offset
                    
                    if no_rect.collidepoint(pos) :

                        return 0

def Score(self) : # affichage de l'ecran de fin

    self.my_settings.screen.blit(self.bg,(0,0))
    self.my_settings.screen.blit(self.end_screen,(0,0))

    self.score_font.render_to(self.my_settings.screen,(ReSize(305),ReSize(585)),str(self.t_miss),self.white)
    self.score_font.render_to(self.my_settings.screen,(ReSize(154),ReSize(175)),str(self.t_300),self.white)
    self.score_font.render_to(self.my_settings.screen,(ReSize(154),ReSize(307)),str(self.t_100),self.white)
    self.score_font.render_to(self.my_settings.screen,(ReSize(154),ReSize(439)),str(self.t_50),self.white)

    pygame.display.flip()

    loop = True
    while loop :

        self.key = pygame.key.get_pressed()
        for self.event in pygame.event.get() :

            GameQuit(self)

            if self.event.type == pygame.KEYDOWN and self.event.key == pygame.K_F2 :

                WriteReplay(self)

            if self.event.type == pygame.KEYDOWN and self.event.key == pygame.K_q :
                loop = False

def WriteReplay(self) : # ecriture du replay dans un fichier .txt

    now = datetime.now()
    replay_name = now.strftime(f'{self.map_name} [{self.diff_name}] (%Y-%m-%d - %H.%M.%S)')

    with open(f'assets\\replays\\{replay_name}.txt', 'w') as replay :
        
        replay.write(f'{self.score}\n')
        replay.write(f'{self.t_300}\n')
        replay.write(f'{self.t_100}\n')
        replay.write(f'{self.t_50}\n')
        replay.write(f'{self.t_miss}\n')
        replay.write(f'{self.accuracy}\n')
        replay.write(f'{self.max_combo}\n')

        for i in self.replay_clicks :

            replay.write(f'{i}\n')

def Write(self) : # ecriture et modification des parametres du jeu sauvegardes dans settings.txt

    with open('assets\\settings.txt','w') as settings_file :

        modifs = [self.offset,self.volume,self.volume_music,self.volume_effects,self.skin]

        for a in range(len(self.lines)) :

            settings_file.write(self.lines[a].replace(self.lines[a],f'{modifs[a]}\n'))


def GameQuit(self) : # quitte la partie/menu et le programme

    if self.event.type == pygame.QUIT or (self.event.type == pygame.KEYDOWN and self.event.key == pygame.K_F4 and self.key[pygame.K_LALT]) :

        Write(self)
        
        pygame.quit()
        exit(0)