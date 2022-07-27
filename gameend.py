import pygame
from datetime import datetime

class GameEnd :

    def proposeOffset( osu ) -> int : # propose un offset au joueur si possible

        pygame.mouse.set_visible( True )

        ur_moy = 0

        if osu.total_ur != [] :

            noir = pygame.Rect( 0, 0, osu.width, osu.height )
            pygame.draw.rect( osu.screen, (0, 0, 0), noir )

            for u in osu.total_ur :
                ur_moy += u

            ur_moy /= len( osu.total_ur )
            ur_moy = round( ur_moy )

            if ur_moy < 0 :
                rep_txt = f"You are tapping {abs( ur_moy )}ms earlier, do you want to apply a negative offset of {abs( ur_moy )}ms ?"

            elif ur_moy > 0 :
                rep_txt = f"You are tapping {abs( ur_moy )}ms too late, do you want to apply a positive offset of {abs( ur_moy )}ms ?"

            rep_rect        = osu.rep_font.get_rect( rep_txt )
            rep_rect.center = (osu.width/2, osu.height/2)

            yes_txt         = "Yes"
            yes_rect        = osu.rep_font.get_rect( yes_txt )
            yes_rect.center = (osu.width/3, osu.height/3*2)

            no_txt         = "No"
            no_rect        = osu.rep_font.get_rect( no_txt )
            no_rect.center = (osu.width/3*2, osu.height/3*2)

            osu.rep_font.render_to( osu.screen, rep_rect, rep_txt,osu.white )
            osu.rep_font.render_to( osu.screen, yes_rect, yes_txt,osu.white )
            osu.rep_font.render_to( osu.screen, no_rect, no_txt,osu.white )

            pygame.display.flip()

            loop = True
            while loop :

                osu.key = pygame.key.get_pressed()
                for osu.event in pygame.event.get() :

                    osu.gameQuit()

                    if osu.event.type == pygame.KEYDOWN and osu.event.key == pygame.K_F2 :

                        osu.writeReplay()

                    if osu.event.type == pygame.MOUSEBUTTONDOWN and osu.event.button == pygame.BUTTON_LEFT :

                        pos = pygame.mouse.get_pos()

                        if yes_rect.collidepoint( pos ) :

                            offset = - ur_moy

                            return offset

                        if no_rect.collidepoint( pos ) :

                            return 0

    def showScore( osu ) -> None : # affichage de l'ecran de fin

        osu.screen.blit( osu.bg, (0, 0) )
        osu.screen.blit( osu.end_screen, (0, 0) )

        osu.score_font.render_to( osu.screen, (osu.reSize( 305 ), osu.reSize( 585 )), str(osu.t_miss), osu.white)
        osu.score_font.render_to( osu.screen, (osu.reSize( 154 ), osu.reSize( 175 )), str(osu.t_300), osu.white)
        osu.score_font.render_to( osu.screen, (osu.reSize( 154 ), osu.reSize( 307 )), str(osu.t_100), osu.white)
        osu.score_font.render_to( osu.screen, (osu.reSize( 154 ), osu.reSize( 439 )), str(osu.t_50), osu.white)

        pygame.display.flip()

        loop = True
        while loop :

            osu.key = pygame.key.get_pressed()
            for osu.event in pygame.event.get() :

                osu.gameQuit()

                if osu.event.type == pygame.KEYDOWN and osu.event.key == pygame.K_F2 :

                    osu.writeReplay()

                if osu.event.type == pygame.KEYDOWN and osu.event.key == pygame.K_q :
                    loop = False

    def writeReplay( osu ) -> None : # ecriture du replay dans un fichier .txt

        now = datetime.now()
        replay_name = now.strftime( f"{osu.map_name} [{osu.diff_name}] (%Y-%m-%d - %H.%M.%S)" )

        with open( f"assets\\replays\\{replay_name}.txt", "w" ) as replay :

            replay.write( f"{osu.score}\n" )
            replay.write( f"{osu.t_300}\n" )
            replay.write( f"{osu.t_100}\n" )
            replay.write( f"{osu.t_50}\n" )
            replay.write( f"{osu.t_miss}\n" )
            replay.write( f"{osu.accuracy}\n" )
            replay.write( f"{osu.max_combo}\n" )

            for i in osu.replay_clicks :

                replay.write( f"{i}\n" )

    def writeSettings( self ) -> None : # ecriture et modification des parametres du jeu sauvegardes dans settings.txt

        with open( "assets\\settings.txt", "w" ) as settings_file :

            modifs = [self.offset, self.volume, self.volume_music, self.volume_effects, self.skin]

            for a in range( len( self.lines ) ) :

                settings_file.write( self.lines[a].replace( self.lines[a], f"{modifs[a]}\n" ) )

    def gameQuit( self ) -> None : # quitte la partie/menu et le programme

        if self.event.type == pygame.QUIT or (self.event.type == pygame.KEYDOWN and self.event.key == pygame.K_F4 and self.key[pygame.K_LALT]) :

            self.writeSettings()

            pygame.quit()
            exit( 0 )