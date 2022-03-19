import pygame

from tools import load

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
            rep = self.acc_font.render(f'You are tapping {abs(ur_moy)}ms earlier, do you want to apply a negative offset of {abs(ur_moy)}ms ?',False,self.white).convert()
        
        if ur_moy > 0 :
            rep = self.acc_font.render(f'You are tapping {abs(ur_moy)}ms too late, do you want to apply a positive offset of {abs(ur_moy)}ms ?',False,self.white).convert()

        rep_rect = rep.get_rect(center = (self.wi/2,self.he/2))

        yes      = self.acc_font.render(f'Yes',False,self.white).convert()
        yes_rect = yes.get_rect(center = (self.wi/3,self.he/3*2))

        no      = self.acc_font.render(f'No',False,self.white).convert()
        no_rect = no.get_rect(center = (self.wi/3*2,self.he/3*2))
        
        self.my_settings.screen.blit(rep,rep_rect)
        self.my_settings.screen.blit(yes,yes_rect)
        self.my_settings.screen.blit(no,no_rect)
        
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

    end_screen = load('images\\end_screen.png',(self.wi,self.he),False)

    self.my_settings.screen.blit(end_screen,(0,0))
    pygame.display.flip()

    #print('accuracy :',round(self.accuracy,2))

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