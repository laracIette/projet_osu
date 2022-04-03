from datetime import datetime
import pygame
from tools import ReSize

def ProposeOffset(osu) : # propose un offset au joueur si possible

    pygame.mouse.set_visible(True)

    ur_moy = 0

    if osu.total_ur != [] :

        noir = pygame.Rect(0,0,osu.wi,osu.he)
        pygame.draw.rect(osu.my_settings.screen,(0,0,0),noir)
        
        for u in osu.total_ur :
            ur_moy += u

        ur_moy /= len(osu.total_ur)
        ur_moy = round(ur_moy)

        if ur_moy < 0 :
            rep_txt = f"You are tapping {abs(ur_moy)}ms earlier, do you want to apply a negative offset of {abs(ur_moy)}ms ?"
        
        if ur_moy > 0 :
            rep_txt = f"You are tapping {abs(ur_moy)}ms too late, do you want to apply a positive offset of {abs(ur_moy)}ms ?"

        rep_rect        = osu.rep_font.get_rect(rep_txt)
        rep_rect.center = (osu.wi/2,osu.he/2)

        yes_txt         = "Yes"
        yes_rect        = osu.rep_font.get_rect(yes_txt)
        yes_rect.center = (osu.wi/3,osu.he/3*2)

        no_txt         = "No"
        no_rect        = osu.rep_font.get_rect(no_txt)
        no_rect.center = (osu.wi/3*2,osu.he/3*2)
        
        osu.rep_font.render_to(osu.my_settings.screen,rep_rect,rep_txt,osu.white)
        osu.rep_font.render_to(osu.my_settings.screen,yes_rect,yes_txt,osu.white)
        osu.rep_font.render_to(osu.my_settings.screen,no_rect,no_txt,osu.white)
        
        pygame.display.flip()
        
        loop = True
        while loop :

            osu.key = pygame.key.get_pressed()
            for osu.event in pygame.event.get() :

                GameQuit(osu)

                if osu.event.type == pygame.KEYDOWN and osu.event.key == pygame.K_F2 :

                    WriteReplay(osu)

                if osu.event.type == pygame.MOUSEBUTTONDOWN and osu.event.button == pygame.BUTTON_LEFT :

                    pos = pygame.mouse.get_pos()

                    if yes_rect.collidepoint(pos) :
                        
                        offset = - ur_moy

                        return offset
                    
                    if no_rect.collidepoint(pos) :

                        return 0

def Score(osu) : # affichage de l'ecran de fin

    osu.my_settings.screen.blit(osu.bg,(0,0))
    osu.my_settings.screen.blit(osu.end_screen,(0,0))

    osu.score_font.render_to(osu.my_settings.screen,(ReSize(305),ReSize(585)),str(osu.t_miss),osu.white)
    osu.score_font.render_to(osu.my_settings.screen,(ReSize(154),ReSize(175)),str(osu.t_300),osu.white)
    osu.score_font.render_to(osu.my_settings.screen,(ReSize(154),ReSize(307)),str(osu.t_100),osu.white)
    osu.score_font.render_to(osu.my_settings.screen,(ReSize(154),ReSize(439)),str(osu.t_50),osu.white)

    pygame.display.flip()

    loop = True
    while loop :

        osu.key = pygame.key.get_pressed()
        for osu.event in pygame.event.get() :

            GameQuit(osu)

            if osu.event.type == pygame.KEYDOWN and osu.event.key == pygame.K_F2 :

                WriteReplay(osu)

            if osu.event.type == pygame.KEYDOWN and osu.event.key == pygame.K_q :
                loop = False

def WriteReplay(osu) : # ecriture du replay dans un fichier .txt

    now = datetime.now()
    replay_name = now.strftime(f"{osu.map_name} [{osu.diff_name}] (%Y-%m-%d - %H.%M.%S)")

    with open(f"assets\\replays\\{replay_name}.txt", "w") as replay :
        
        replay.write(f"{osu.score}\n")
        replay.write(f"{osu.t_300}\n")
        replay.write(f"{osu.t_100}\n")
        replay.write(f"{osu.t_50}\n")
        replay.write(f"{osu.t_miss}\n")
        replay.write(f"{osu.accuracy}\n")
        replay.write(f"{osu.max_combo}\n")

        for i in osu.replay_clicks :

            replay.write(f"{i}\n")

def Write(self) : # ecriture et modification des parametres du jeu sauvegardes dans settings.txt

    with open("assets\\settings.txt","w") as settings_file :

        modifs = [self.offset,self.volume,self.volume_music,self.volume_effects,self.skin]

        for a in range(len(self.lines)) :

            settings_file.write(self.lines[a].replace(self.lines[a],f"{modifs[a]}\n"))


def GameQuit(self) : # quitte la partie/menu et le programme

    if self.event.type == pygame.QUIT or (self.event.type == pygame.KEYDOWN and self.event.key == pygame.K_F4 and self.key[pygame.K_LALT]) :

        Write(self)
        
        pygame.quit()
        exit(0)