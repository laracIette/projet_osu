import math
import pygame

class OsuObjects :
        
    def GetSpinner(osu) : # verifie si doit afficher un spinner, si oui le cree

        if osu.s_num < len(osu.spinners) :

            if osu.GetTime() - osu.paused_time  >=  osu.start_time + osu.spinners[osu.s_num][0] - osu.ar_time :

                osu.show_spinners.append([osu.GetTime()-osu.paused_time,0,osu.spinners[osu.s_num][1]-osu.spinners[osu.s_num][0],osu.spinner,0])

                osu.show_spinner     = True
                osu.spinner_fade     = True
                osu.click_time_check = False
                osu.spin_score_bonus = 0

                osu.s_num += 1

    def SetSpinners(osu) : # affiche et modifie le/les spinners si mouvement

        if osu.waiting == False :

            if osu.show_spinner :
                
                for p in osu.show_spinners :

                    p[1] = osu.GetTime() - p[0] - osu.paused_time
                    if p[1] >= p[2] :

                        osu.spinner_fade = True

                        if p[4] > 0 :

                            p[4] -= 0.6/osu.fps
                            p[3].set_alpha(p[4]*255)

                        else :
                            
                            osu.show_spinner = False
                            osu.show_spinners.pop(0)

                    if p[4] < 1 and osu.spinner_fade == False :
                        
                        p[3].set_alpha(p[4]*255)
                        p[4] += 0.6/osu.fps

                if osu.click_check :

                    if osu.click_time_check == False :
                        osu.click_time_check = True

                        osu.click_time = osu.GetTime()

                    osu.pos2 = pygame.mouse.get_pos()

                    spin_center = math.hypot(osu.width/2-osu.pos[0],osu.height/2-osu.pos[1])
                    osu.spin_x = (osu.pos[0]-osu.pos2[0])/spin_center*60
                    osu.spin_y = (osu.pos[1]-osu.pos2[1])/spin_center*60
                    
                    osu.spin = osu.Spinning()
                    
                    for p in osu.show_spinners :

                        if osu.GetTime() - osu.click_time >= p[2] / 2 :

                            if abs(osu.spin - osu.spin_tot2) > 66 :
                                osu.spin_tot2 = osu.spin
                                osu.score    += 10

                                if osu.health < osu.max_health - osu.spin_health :
                                    osu.health += osu.spin_health
                                else :
                                    osu.health = osu.max_health
                                
                                osu.PlaySound("spinnerspin",0.5,osu.volume_effects)
                                
                            if abs(osu.spin - osu.spin_tot) > 330 :

                                osu.spin_tot = osu.spin
                                osu.score   += 950
                                
                                osu.PlaySound("spinnerbonus",1,osu.volume_effects)

                                osu.spin_score_bonus_time = osu.GetTime()
                                osu.spin_score_bonus     += 1

                                osu.spin_score = osu.combo_font.render(str(osu.spin_score_bonus*1000),False,osu.white).convert()

            if osu.GetTime() < osu.spin_score_bonus_time + 1000 :

                if osu.spin_score_bonus_alpha < 1 :

                    osu.spin_score_bonus_alpha += 6/osu.fps
                    osu.spin_score.set_alpha(osu.spin_score_bonus_alpha*255)

            elif osu.spin_score_bonus_alpha > 0 :

                osu.spin_score_bonus_alpha -= 6/osu.fps
                osu.spin_score.set_alpha(osu.spin_score_bonus_alpha*255)

        for p in osu.show_spinners :

            spinner_spin = pygame.transform.rotate(p[3],osu.spin).convert_alpha()
            spinner_rect = spinner_spin.get_rect(center = (osu.width/2,osu.height/2))
            
            osu.screen.blit(spinner_spin,spinner_rect)

    def Spinning(osu) : # mouvement de rotation du spinner
        
        if osu.spin_x >= 0 and osu.spin_y >= 0 :

            if osu.pos2[0] < osu.width/2 and osu.pos2[1] >= osu.height/2 :
                osu.spin -= math.hypot(osu.spin_x,osu.spin_y)
            if osu.pos2[0] >= osu.width/2 and osu.pos2[1] < osu.height/2 :
                osu.spin += math.hypot(osu.spin_x,osu.spin_y)

        if osu.spin_x >= 0 and osu.spin_y < 0 :

            if osu.pos2[0] < osu.width/2 and osu.pos2[1] < osu.height/2 :
                osu.spin += math.hypot(osu.spin_x,osu.spin_y)
            if osu.pos2[0] >= osu.width/2 and osu.pos2[1] >= osu.height/2 :
                osu.spin -= math.hypot(osu.spin_x,osu.spin_y)

        if osu.spin_x < 0 and osu.spin_y >= 0 :

            if osu.pos2[0] < osu.width/2 and osu.pos2[1] < osu.height/2 :
                osu.spin -= math.hypot(osu.spin_x,osu.spin_y)
            if osu.pos2[0] >= osu.width/2 and osu.pos2[1] >= osu.height/2 :
                osu.spin += math.hypot(osu.spin_x,osu.spin_y)

        if osu.spin_x < 0 and osu.spin_y < 0 :

            if osu.pos2[0] < osu.width/2 and osu.pos2[1] >= osu.height/2 :
                osu.spin += math.hypot(osu.spin_x,osu.spin_y)
            if osu.pos2[0] >= osu.width/2 and osu.pos2[1] < osu.height/2 :
                osu.spin -= math.hypot(osu.spin_x,osu.spin_y)

        return osu.spin

    def GetCircle(osu) : # verifie si doit afficher un cercle, si oui le cree

        if osu.c_num < len(osu.circles) :

            if osu.GetTime() - osu.paused_time  >=  osu.start_time + osu.circles[osu.c_num][2] - osu.ar_time :

                coor = [round(osu.circles[osu.c_num][0] / 512 * osu.width * 3/4 * 0.86 + osu.ReSize(360),2),
                        round(osu.circles[osu.c_num][1] / 384 * osu.height      * 0.86 + osu.ReSize(75), 2)]

                if osu.circles[osu.c_num][3] == 1 :
                    osu.numbers = 1
                else :
                    osu.numbers += 1

                number = osu.number_font.render(f"{osu.numbers}",False,osu.white).convert()

                osu.show_circles.append([osu.GetTime()-osu.paused_time,0,1,osu.a_circle,coor,osu.circles[osu.c_num][2],number,osu.circle,osu.fade,1,osu.acc_check,osu.faded,1])

                osu.c_num += 1

        elif osu.c_num == len(osu.circles) :

            osu.end_time = osu.GetTime()

            osu.c_num += 1

    def SetCircles(osu) : # affiche et modifie le/les cercles

        for u in osu.show_circles :

            if osu.waiting == False :
            
                u[1] = osu.GetTime() - u[0] - osu.paused_time

                if u[1] >= osu.ar_time and u[8] == False :
                    u[8] = True

                if u[2] < 4 :

                    a_c_rescale = osu.a_c_s/u[2]
                    u[3]        = pygame.transform.smoothscale(osu.a_circle,(a_c_rescale,a_c_rescale)).convert_alpha()
                
                if u[8] == False :

                    u[3].set_alpha(255*u[2]/2-255/2)
                    u[7].set_alpha(255*u[2]-255)
                    u[6].set_alpha(255*u[2]-255)
                    
                    u[2] += 6*450/osu.ar_time/osu.fps
                    u[2]  = round(u[2],2)
                
                else :

                    u[12]    += 1/osu.fps
                    c_rescale = osu.c_s*u[12]
                    u[7]      = pygame.transform.smoothscale(osu.circle,(c_rescale,c_rescale)).convert_alpha()

                    u[3].set_alpha(255*u[9])
                    u[7].set_alpha(255*u[9])
                    u[6].set_alpha(255*u[9])

                    u[9] -= 18/osu.fps
                    u[9]  = round(u[9],2)

            a_c_rect    = u[3].get_rect(center = u[4])
            circle_rect = u[7].get_rect(center = u[4])
            number_rect = u[6].get_rect(center = u[4])

            osu.screen.blit(u[3],a_c_rect)
            osu.screen.blit(u[7],circle_rect)
            osu.screen.blit(u[6],(number_rect[0]+osu.ReSize(1),number_rect[1]+osu.ReSize(8)))
        
            if u[1] >= osu.ar_time + osu.od_time :
                osu.show_circles.pop(0)
                
                if u[11] == False :

                    osu.t_miss += 1

                    osu.acc.append(0)
                    osu.show_acc.append([osu.acc_miss,u[4],osu.GetTime(),0])

                    osu.acc_check = True

                    osu.health -= osu.health_minus

                    if osu.combo >= 20 :
                        osu.PlaySound("miss",1,osu.volume_effects)
                    osu.combo = 0

    def GetFollowPoint(osu) : # verifie si doit afficher un followpoint, si oui le cree

        if osu.f_num < len(osu.circles) - 1 :

            if osu.GetTime() - osu.paused_time  >=  osu.start_time + osu.circles[osu.f_num][2] - osu.ar_time :

                coor1 = [round(osu.circles[osu.f_num][0]   / 512 * osu.width * 3/4 * 0.86 + osu.ReSize(360),2),
                        round(osu.circles[osu.f_num][1]   / 384 * osu.height       * 0.86 + osu.ReSize(75), 2)]
                coor2 = [round(osu.circles[osu.f_num+1][0] / 512 * osu.width * 3/4 * 0.86 + osu.ReSize(360),2),
                        round(osu.circles[osu.f_num+1][1] / 384 * osu.height       * 0.86 + osu.ReSize(75), 2)]

                if coor1 != coor2 and osu.circles[osu.f_num+1][3] != 1 :

                    hypot = math.hypot(coor2[0]-coor1[0],coor2[1]-coor1[1])
                    tan   = abs(coor2[0]-coor1[0])

                    if tan == 0 :
                        followpoint_angle = 90

                    else :
                        
                        if (coor1[0] < coor2[0] and coor1[1] < coor2[1]) or (coor1[0] > coor2[0] and coor1[1] > coor2[1]) :
                            followpoint_angle = -math.degrees(math.acos(tan/hypot))

                        else :
                            followpoint_angle = math.degrees(math.acos(tan/hypot))

                    followpoint = pygame.transform.smoothscale(osu.followpoint,(hypot*0.9,osu.followpoint.get_height())).convert_alpha()
                    followpoint = pygame.transform.rotate(followpoint,followpoint_angle).convert_alpha()

                    if coor1[0] >= coor2[0] : x = coor2[0]
                    if coor1[1] >= coor2[1] : y = coor2[1]
                    if coor1[0] <  coor2[0] : x = coor1[0]
                    if coor1[1] <  coor2[1] : y = coor1[1]

                    center_rect      = (abs((coor2[0]-coor1[0])/2) + x,
                                        abs((coor2[1]-coor1[1])/2) + y)

                    followpoint_rect = followpoint.get_rect(center = center_rect)
                
                    osu.show_followpoints.append([osu.GetTime()-osu.paused_time,0,followpoint_rect,followpoint,0,osu.circles[osu.f_num+1][2]-osu.circles[osu.f_num][2]])

                osu.f_num += 1

    def SetFollowPoints(osu) : # affiche et modifie le/les followpoints

        for f in osu.show_followpoints :

            if osu.waiting == False :
            
                f[1] = osu.GetTime() - f[0] - osu.paused_time

                if f[4] < 1 and f[1] < f[5] :

                    f[4] += 6/osu.fps
                    f[4]  = round(f[4],2)

                f[3].set_alpha(f[4]*255)

                if f[1] > f[5] + osu.ar_time or osu.acc_check :

                    f[4] -= 6/osu.fps
                    f[4]  = round(f[4],2)

                    if f[1] > f[5] + osu.ar_time + osu.od_time :
                        osu.show_followpoints.pop(0)

            osu.screen.blit(f[3],f[2])