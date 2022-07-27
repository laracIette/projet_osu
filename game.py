import math
import pygame

class OsuGame :

    def setBreak( osu ) -> None : # determine les pauses manuelles dans la partie

        for g in osu.game_breaks :

            if osu.getTime() >= osu.start_time + g[0] - osu.paused_time + 1000 :
                osu.game_break = True

            if osu.getTime() >= osu.start_time + g[1] - osu.paused_time - 1000 :
                osu.game_break = False
                osu.game_breaks.pop( 0 )

    def applyBreaks( osu ) -> None : # declenche les pauses automatiques dans la partie

        if osu.getTime() >= osu.music_start - osu.start_offset/2.5 and osu.break_lock == False :
            osu.game_break = False
            osu.break_lock = True

        if osu.getTime() >= osu.end_time + osu.start_offset/2.5 :
            osu.game_break = True

    def startGame( osu ) -> None : # elements declenchants la partie

        pygame.mixer.music.play()
        osu.playing = True

    def endGame( osu ) -> None : # elements pouvants terminer une partie

        osu.running = False

        pygame.mixer.music.pause()

        if osu.health <= 0 :
            osu.playSound( "fail", 1, osu.volume_effects )
            osu.death = True

        if osu.total_ur != [] :
            osu.offset += osu.proposeOffset()

        osu.writeSettings()
        pygame.mixer.music.unpause()

        if osu.death == False :

            osu.showScore()

        osu.menu.menuChoice( osu.mod_list )

    def getpause( osu ) -> None : # captation des touches necessaires a la pause de la partie

        if osu.event.type == pygame.KEYDOWN and osu.event.key == pygame.K_ESCAPE :
            osu.running = False

            if osu.waiting :
                osu.paused_time += osu.getTime() - osu.pause_time

            osu.pause_time = osu.getTime()

            pygame.mouse.set_visible( True )
            pygame.mixer.music.pause()

            osu.screen.blit( osu.pause_screen, (0,0) )
            pygame.display.flip()

            osu.writeSettings()

            osu.pause()

    def pause( osu ) -> None : # declenche la pause manuelle

        loop = True
        while loop :

            for osu.event in pygame.event.get() :

                if osu.event.type == pygame.KEYDOWN and osu.event.key == pygame.K_ESCAPE :
                    loop = False

                    osu.running = True
                    osu.waiting = True

                    pygame.mouse.set_visible( False )

                    osu.fps_time += osu.getTime() - osu.pause_time

                if osu.event.type == pygame.KEYDOWN and osu.event.key == pygame.K_q :
                    loop = False

                    osu.menu.menuChoice( osu.mod_list )

                osu.gameQuit()

    def unpause( osu ) -> None : # verifie et si possible quitte la pause

        pos1 = pygame.mouse.get_pos()

        if (osu.event.type == pygame.KEYDOWN and osu.event.key == pygame.K_x) or (osu.event.type == pygame.KEYDOWN and osu.event.key == pygame.K_v) :

            distance1 = math.hypot( pos1[0] - osu.pos[0], pos1[1] - osu.pos[1] )

            if distance1 < 5 :

                osu.waiting = False

                pygame.mixer.music.unpause()

                osu.paused_time += osu.getTime() - osu.pause_time

    def changeOffset( osu ) -> None : # detecte si le joueur presse les touche de + ou - d'offset et l'applique

        if osu.event.type == pygame.KEYDOWN and osu.event.key == pygame.K_EQUALS :

            if osu.key[pygame.K_LSHIFT] :
                osu.offset += 1
            else :
                osu.offset += 5

            osu.offset_time = osu.getTime()
            osu.show_offset = True

        if osu.event.type == pygame.KEYDOWN and osu.event.key == pygame.K_MINUS :

            if osu.key[pygame.K_LSHIFT] :
                osu.offset -= 1
            else :
                osu.offset -= 5

            osu.offset_time = osu.getTime()
            osu.show_offset = True

    def getClicks( osu ) -> None : # capte les touches clavier pouvant interagir avec un objet de la partie

        if osu.event.type == pygame.KEYDOWN and (osu.event.key == pygame.K_x or osu.event.key == pygame.K_v) :

            osu.click_check = True

            osu.replay_clicks.append( osu.pos )

            osu.getAcc()

        if osu.event.type == pygame.KEYUP and (osu.event.key == pygame.K_x or osu.event.key == pygame.K_v) :
            osu.click_check = False

    def getAcc( osu ) -> None : # detecte et applique le changement d'accuracy du joueur dans la partie

        for v in range( len( osu.show_circles ) ) :

            if osu.acc_check == False and osu.show_circles[v].faded == False :

                distance = math.hypot( osu.show_circles[v].coor[0] - osu.pos[0], osu.show_circles[v].coor[1] - osu.pos[1] )

                if distance < osu.c_s/2*115/121 :

                    osu.acc_check = True

                    difference = osu.getTime() - (osu.start_time + osu.show_circles[v].start_time + osu.paused_time) + osu.offset
                    osu.total_ur.append( difference )

                    if abs( difference ) < osu.od_time :

                        if abs( difference ) < osu.od_time/4 :
                            osu.t_300 += 1

                            osu.hit_value = 300
                            osu.show_ur.append( [osu.blue, 278*difference/osu.od_time/2, osu.getTime(), 0] )

                        elif abs( difference ) > osu.od_time/4 and abs( difference ) < osu.od_time/2 :
                            osu.t_100 += 1

                            osu.hit_value = 100
                            osu.show_ur.append( [osu.green, 278*difference/osu.od_time/2, osu.getTime(), 0] )
                            osu.show_acc.append( [osu.acc_100, osu.show_circles[v].coor, osu.getTime(), 0] )

                        elif abs( difference ) > osu.od_time/2 :
                            osu.t_50 += 1

                            osu.hit_value = 50
                            osu.show_ur.append( [osu.orange, 278*difference/osu.od_time/2, osu.getTime(), 0] )
                            osu.show_acc.append( [osu.acc_50, osu.show_circles[v].coor, osu.getTime(), 0] )

                        osu.acc.append( round( osu.hit_value/3, 2) )
                        health_bonus = round( osu.hit_value/30, 2 )

                        if osu.health + health_bonus < osu.max_health :
                            osu.health += health_bonus
                        else :
                            osu.health = osu.max_health

                        osu.playSound( "hit", 0.5, osu.volume_effects )

                        osu.combo += 1
                        if osu.combo > osu.max_combo :
                            osu.max_combo = osu.combo

                    else :

                        osu.t_miss += 1

                        osu.hit_value = 0
                        osu.show_acc.append( [osu.acc_miss, osu.show_circles[v].coor, osu.getTime(), 0] )

                        osu.acc.append( 0 )

                        osu.health -= osu.health_minus

                        if osu.combo >= 20 :
                            osu.playSound( "miss", 1, osu.volume_effects )
                        osu.combo = 0

                    osu.show_circles[v].fade  = True
                    osu.show_circles[v].faded = True