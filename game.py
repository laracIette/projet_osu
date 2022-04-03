import math
import pygame
from sounds import Play
from tools import GetTime
from gameend import Write, GameQuit

class OsuGame :

    def SetBreak(osu) : # determine les pauses dans la partie (pas manuelles)

        for g in osu.game_breaks :

            if GetTime() >= osu.start_time + g[0] - osu.paused_time + 1000 :
                osu.game_break = True
            
            if GetTime() >= osu.start_time + g[1] - osu.paused_time - 1000 :
                osu.game_break = False
                osu.game_breaks.pop(0)

    def ApplyBreaks(osu) : # declenche les pauses dans la partie (pas manuelles)
        
        if GetTime() >= osu.music_start - osu.start_offset/2.5 and osu.break_lock == False :
            osu.game_break = False
            osu.break_lock = True

        if GetTime() >= osu.end_time + osu.start_offset/2.5 :
            osu.game_break = True

    def StartGame(osu) : # elements declenchants la partie
        
        pygame.mixer.music.play()
        osu.playing = True
        
    def EndGame(osu) : # elements pouvants terminer une partie

        osu.running = False

        pygame.mixer.music.pause()

        if osu.health <= 0 :
            Play(osu.sounds,"fail",1,osu.volume,osu.volume_effects)
            osu.death = True

        if osu.total_ur != [] :
            osu.offset += osu.ProposeOffset()

        Write(osu)

    def GetPause(osu) : # captation des touches necessaires a la pause de la partie
        
        if (osu.event.type == pygame.KEYDOWN and osu.event.key == pygame.K_ESCAPE) :
            osu.running = False
            
            if osu.waiting :
                osu.paused_time += GetTime() - osu.pause_time

            osu.pause_time = GetTime()

            pygame.mouse.set_visible(True)
            pygame.mixer.music.pause()

            osu.my_settings.screen.blit(osu.pause_screen,(0,0))
            pygame.display.flip()
            
            Write(osu)

            osu.Pause()

    def Pause(osu) : # declenche la pause manuelle

        loop = True
        while loop :

            for osu.event in pygame.event.get() :

                if osu.event.type == pygame.KEYDOWN and osu.event.key == pygame.K_ESCAPE :
                    loop = False

                    osu.running = True
                    osu.waiting = True

                    pygame.mouse.set_visible(False)

                    osu.fps_time += GetTime() - osu.pause_time

                if osu.event.type == pygame.KEYDOWN and osu.event.key == pygame.K_q :
                    loop = False

                    osu.to_menu = True

                GameQuit(osu)

    def UnPause(osu) : # verifie et si possible quitte la pause

        pos1 = pygame.mouse.get_pos()

        if (osu.event.type == pygame.KEYDOWN and osu.event.key == pygame.K_x) or (osu.event.type == pygame.KEYDOWN and osu.event.key == pygame.K_v) :
            
            distance1 = math.hypot(pos1[0]-osu.pos[0],pos1[1]-osu.pos[1])

            if distance1 < 5 :

                osu.waiting = False

                pygame.mixer.music.unpause()
                                            
                osu.paused_time += GetTime() - osu.pause_time

    def ChangeOffset(osu) : # detecte si le joueur presse les touche de + ou - d'offset et l'applique

        if osu.event.type == pygame.KEYDOWN and osu.event.key == pygame.K_EQUALS :

            if osu.key[pygame.K_LSHIFT] :
                osu.offset += 1
            else :
                osu.offset += 5

            osu.offset_time = GetTime()
            osu.show_offset = True

        if osu.event.type == pygame.KEYDOWN and osu.event.key == pygame.K_MINUS :

            if osu.key[pygame.K_LSHIFT] :
                osu.offset -= 1
            else :
                osu.offset -= 5

            osu.offset_time = GetTime()
            osu.show_offset = True

    def GetClicks(osu) : # capte les touches clavier pouvant interagir avec un objet de la partie

        if osu.event.type == pygame.KEYDOWN and (osu.event.key == pygame.K_x or osu.event.key == pygame.K_v) :
            
            osu.click_check = True
            
            osu.replay_clicks.append(osu.pos)
            
            osu.GetAcc()
            
        if osu.event.type == pygame.KEYUP and (osu.event.key == pygame.K_x or osu.event.key == pygame.K_v) :
            osu.click_check = False

    def GetAcc(osu) : # detecte et applique le changement d'accuracy du joueur dans la partie

        for v in range(len(osu.show_circles)) :

            if osu.acc_check == False and osu.show_circles[v][11] == False :

                distance = math.hypot(osu.show_circles[v][4][0]-osu.pos[0],osu.show_circles[v][4][1]-osu.pos[1])

                if distance < osu.c_s/2*115/121 :

                    osu.acc_check = True

                    difference = GetTime() - (osu.start_time + osu.show_circles[v][5] + osu.paused_time) + osu.offset
                    osu.total_ur.append(difference)

                    if abs(difference) < osu.od_time :

                        if abs(difference) < osu.od_time/4 :
                            osu.t_300 += 1

                            osu.hit_value = 300
                            osu.show_ur.append([osu.blue,278*difference/osu.od_time/2,GetTime(),0])

                        if abs(difference) > osu.od_time/4 and abs(difference) < osu.od_time/2 :
                            osu.t_100 += 1

                            osu.hit_value = 100
                            osu.show_ur.append([osu.green,278*difference/osu.od_time/2,GetTime(),0])
                            osu.show_acc.append([osu.acc_100,osu.show_circles[v][4],GetTime(),0])
                        
                        if abs(difference) > osu.od_time/2 :
                            osu.t_50 += 1

                            osu.hit_value = 50
                            osu.show_ur.append([osu.orange,278*difference/osu.od_time/2,GetTime(),0])
                            osu.show_acc.append([osu.acc_50,osu.show_circles[v][4],GetTime(),0])

                        osu.acc.append(round(osu.hit_value/3,2))
                        health_bonus = round(osu.hit_value/30,2)

                        if osu.health + health_bonus < osu.max_health :
                            osu.health += health_bonus
                        else :
                            osu.health = osu.max_health

                        Play(osu.sounds,"hit",0.5,osu.volume,osu.volume_effects)
                        
                        osu.combo += 1
                        if osu.combo > osu.max_combo : osu.max_combo = osu.combo

                    else :
                        
                        osu.t_miss += 1

                        osu.hit_value = 0
                        osu.show_acc.append([osu.acc_miss,osu.show_circles[v][4],GetTime(),0])

                        osu.acc.append(0)

                        osu.health -= osu.health_minus

                        if osu.combo >= 20 :
                            Play(osu.sounds,"miss",1,osu.volume,osu.volume_effects)
                        osu.combo = 0

                    osu.show_circles[v][8]  = True
                    osu.show_circles[v][11] = True