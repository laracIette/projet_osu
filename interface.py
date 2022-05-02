import pygame

class OsuInterface :

    def darkenScreen( osu: classmethod ) -> None : # assombri/eclairci l'ecran en fonction des pauses

        if osu.game_break == False :
            pygame.draw.rect( osu.screen, (0, 0, 0), osu.noir )
            #osu.UI = True

        else :
            osu.screen.blit( osu.bg, (0, 0) )
            osu.screen.blit( osu.dim, (0, 0) )
            #osu.UI = False

    def setShowOnScreen( osu: classmethod ) -> None : # determine des elements a afficher pendant une partie

        if osu.waiting == False :

            osu.trail_count += round( 5000/osu.fps )
            if osu.trail_count > 100 :

                osu.trail_pos.append( [osu.pos, osu.cursor_trail, 255] )
                osu.trail_count = 0

            if len(osu.trail_pos) > 8 :
                osu.trail_pos.pop( 0 )

            osu.health    -= osu.passive_health*160/osu.fps
            osu.health_bar = pygame.Rect( osu.reSize( 20 ), osu.reSize( 20 ), osu.reSize( 600*osu.health/600 ), osu.reSize( 20 ) )

        for s in osu.show_ur :
            s[3] = osu.getTime() - s[2] - osu.paused_time

        if osu.show_ur != [] and (len( osu.show_ur ) > 20 or osu.show_ur[0][3] >= 8000) :
            osu.show_ur.pop(0)

        for s in range( len ( osu.show_acc ) ) :

            showed_time = osu.getTime() - osu.show_acc[s][2]

            if showed_time < 300 :

                osu.show_acc[s][3] += 255/300*1000/osu.fps

            elif showed_time > 400 :

                osu.show_acc[s][3] -= 255/100*1000/osu.fps

            if showed_time >= 300 :

                osu.show_acc[s][1][1] += 0.5*160/osu.fps

            osu.show_acc[s][0].set_alpha( osu.show_acc[s][3] )
            osu.show_acc[s][0].convert_alpha()

            if showed_time > 500 :

                osu.show_acc.pop( 0 )
                break

        if osu.show_offset :

            if osu.offset < 0 :
                osu.offset_txt = osu.fps_font.render( f"Local offset : {osu.offset}ms", False, osu.white ).convert()
            else :
                osu.offset_txt = osu.fps_font.render( f"Local offset : +{osu.offset}ms", False, osu.white ).convert()

            if osu.getTime() - osu.offset_time - osu.paused_time >= 1000 :
                osu.show_offset = False

    def showOnScreen( osu: classmethod ) -> None : # affichage des elements de la partie

        if osu.UI == False and osu.UI_alpha > 0 :

            osu.UI_alpha -= 20*160/osu.fps

        if osu.UI_alpha > 0 :

            osu.combo_txt.set_alpha( osu.UI_alpha )
            osu.score_txt.set_alpha( osu.UI_alpha )
            osu.acc_txt.set_alpha( osu.UI_alpha )
            osu.fps_txt.set_alpha( osu.UI_alpha )

            osu.screen.blit( osu.combo_txt, (osu.reSize( 20 ), osu.reSize( 960 )) )
            osu.screen.blit( osu.score_txt, (osu.reSize( 1910 ) - osu.score_txt.get_width(), osu.reSize( -20 )) )
            osu.screen.blit( osu.acc_txt, (osu.reSize( 1910 ) - osu.acc_txt.get_width(), osu.reSize( 80 )) )
            osu.screen.blit( osu.fps_txt, (osu.reSize( 1910 ) - osu.fps_txt.get_width(), osu.reSize( 1075 ) - osu.fps_txt.get_height()) )

            pygame.draw.rect( osu.screen, osu.grey, osu.health_bar_bg )
            pygame.draw.rect( osu.screen, osu.white, osu.health_bar )

        pygame.draw.rect( osu.screen, osu.orange, osu.ur_50 )
        pygame.draw.rect( osu.screen, osu.green, osu.ur_100 )
        pygame.draw.rect( osu.screen, osu.blue, osu.ur_300 )
        pygame.draw.rect( osu.screen, osu.white, osu.ur_middle )

        for u in osu.show_ur :

            ur_hit = pygame.Rect( osu.reSize( 961 + u[1] ), osu.reSize( 1039 ), osu.reSize( 2 ), osu.reSize( 30 ) )
            pygame.draw.rect( osu.screen, u[0], ur_hit )

        for s in osu.show_acc :

            show_acc_rect = s[0].get_rect( center = (s[1][0], s[1][1] - osu.reSize( 60 )) )
            osu.screen.blit( s[0], show_acc_rect )

        if osu.show_offset :

            offset_txt_rect = osu.offset_txt.get_rect( center = (osu.width/2, osu.reSize( 20 )) )
            osu.screen.blit( osu.offset_txt, offset_txt_rect )

        if osu.spin_score_bonus_alpha > 0 :

            spin_score_rect = osu.spin_score.get_rect( center = (osu.width/2, osu.height/4*3) )
            osu.screen.blit( osu.spin_score, spin_score_rect )

        for t in osu.trail_pos :

            if osu.waiting == False :

                t[2] -= 7*160/osu.fps
            t[1].set_alpha( t[2] )

            trail_rect = t[1].get_rect( center = t[0] )
            osu.screen.blit( t[1], trail_rect )

        if osu.waiting == False :
            osu.pos3 = pygame.mouse.get_pos()

        cursor_rect = osu.cursor.get_rect( center = osu.pos3 )
        osu.screen.blit( osu.cursor, cursor_rect )

        if osu.waiting :

            waiting_cursor_rect = osu.cursor.get_rect( center = osu.pos )
            osu.screen.blit( osu.cursor, waiting_cursor_rect )

    def setFps( osu: classmethod ) -> None : # calcule et affiche les fps

        osu.fps = round( 1000 / (osu.getTime() - osu.fps_time), 2 )

        osu.fpss.append( osu.fps )
        if len(osu.fpss) > 40 :
            osu.fpss.pop( 0 )

        for i in osu.fpss :
            osu.avg_fps += i

        osu.fps_time = osu.getTime()
        osu.avg_fps /= len( osu.fpss )
        osu.fps_txt  = osu.fps_font.render( f"{round(osu.avg_fps)}fps", False, osu.white ).convert()
        osu.avg_fps  = 0

    def UItextRenders( osu: classmethod ) -> None : # affiche les elements texte de la partie

        if osu.acc_check :

            osu.accuracy = 0

            if len(osu.acc) != 0 :

                for w in osu.acc :
                    osu.accuracy += w

                osu.accuracy /= len( osu.acc )

            if osu.combo > 2 :
                combo_multiplier = osu.combo - 2
            else :
                combo_multiplier = 0

            osu.score += round( osu.hit_value + (osu.hit_value * ((combo_multiplier * osu.difficulty_multiplier * osu.mod_multiplier) / 25)) )

            osu.acc_txt   = osu.acc_font.render( f"{round(osu.accuracy,2)}%", False, osu.white ).convert()
            osu.combo_txt = osu.combo_font.render( f"{osu.combo}x", False, osu.white ).convert()
            osu.score_txt = osu.combo_font.render( str(osu.score), False, osu.white ).convert()

            osu.acc_check = False

    def hideUI( osu: classmethod ) -> None : # cache/montre l'interface

        if (osu.event.type == pygame.KEYDOWN and osu.event.key == pygame.K_TAB and osu.key[pygame.K_LSHIFT]) or\
           (osu.event.type == pygame.KEYDOWN and osu.event.key == pygame.K_LSHIFT and osu.key[pygame.K_TAB]) :

            if osu.UI :
                osu.UI = False
            else :
                osu.UI       = True
                osu.UI_alpha = 255