import pygame
from tools import Load, ReSize

def ProposeOffset(self) :

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

            for event in pygame.event.get() :

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT :

                    pos = pygame.mouse.get_pos()

                    if yes_rect.collidepoint(pos) :
                        
                        offset = - ur_moy

                        return offset
                    
                    if no_rect.collidepoint(pos) :

                        return 0

def Score(self) :

    self.my_settings.screen.blit(self.bg,(0,0))
    self.my_settings.screen.blit(self.end_screen,(0,0))

    self.score_font.render_to(self.my_settings.screen,(ReSize(305),ReSize(585)),str(self.t_miss),self.white)
    self.score_font.render_to(self.my_settings.screen,(ReSize(154),ReSize(175)),str(self.t_300),self.white)
    self.score_font.render_to(self.my_settings.screen,(ReSize(154),ReSize(307)),str(self.t_100),self.white)
    self.score_font.render_to(self.my_settings.screen,(ReSize(154),ReSize(439)),str(self.t_50),self.white)

    pygame.display.flip()

    loop = True
    while loop :

        key = pygame.key.get_pressed()
        for event in pygame.event.get() :

            if event.type == pygame.KEYDOWN and event.key == pygame.K_q :
                loop = False

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and key[pygame.K_LALT]) :
                loop = False

                pygame.quit()
                exit(0)