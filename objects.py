import math
import pygame
from sounds import Play
from tools import GetTime, ReSize

def GetSpinner(self) :

    if self.q < len(self.spinners) :

        if GetTime() - self.paused_time  >=  self.start_time + self.spinners[self.q][0] - self.ar_time :

            self.show_spinners.append([GetTime()-self.paused_time,0,self.spinners[self.q][1]-self.spinners[self.q][0],self.spinner,0])

            self.show_spinner     = True
            self.spinner_fade     = True
            self.click_time_check = False
            self.spin_score_bonus = 0

            self.q += 1

def SetSpinners(self) :

    if self.waiting == False :

        if self.show_spinner :
            
            for p in self.show_spinners :

                p[1] = GetTime() - p[0] - self.paused_time
                if p[1] >= p[2] :

                    self.spinner_fade = True

                    if p[4] > 0 :

                        p[4] -= 0.6/self.fps
                        p[3].set_alpha(p[4]*255)

                    else :
                        
                        self.show_spinner = False
                        self.show_spinners.pop(0)

                if p[4] < 1 and self.spinner_fade == False :
                    
                    p[3].set_alpha(p[4]*255)
                    p[4] += 0.6/self.fps

            if self.click_check :

                if self.click_time_check == False :
                    self.click_time_check = True

                    self.click_time = GetTime()

                self.pos2 = pygame.mouse.get_pos()

                spin_center = math.hypot(self.wi/2-self.pos[0],self.he/2-self.pos[1])
                self.spin_x = (self.pos[0]-self.pos2[0])/spin_center*60
                self.spin_y = (self.pos[1]-self.pos2[1])/spin_center*60
                
                self.spin = Spinning(self)
                
                for p in self.show_spinners :

                    if GetTime() - self.click_time >= p[2] / 2 :

                        if abs(self.spin - self.spin_tot2) > 66 :
                            self.spin_tot2 = self.spin
                            self.score    += 10

                            if self.health < self.max_health - self.spin_health :
                                self.health += self.spin_health
                            else :
                                self.health = self.max_health
                            
                            Play(self.sounds,'spinnerspin',0.5,self.volume,self.volume_effects)
                            
                        if abs(self.spin - self.spin_tot) > 330 :

                            self.spin_tot = self.spin
                            self.score   += 950
                            
                            Play(self.sounds,'spinnerbonus',1,self.volume,self.volume_effects)

                            self.spin_score_bonus_time = GetTime()
                            self.spin_score_bonus     += 1

                            self.spin_score = self.combo_font.render(str(self.spin_score_bonus*1000),False,self.white).convert()

        if GetTime() < self.spin_score_bonus_time + 1000 :

            if self.spin_score_bonus_alpha < 1 :

                self.spin_score_bonus_alpha += 6/self.fps
                self.spin_score.set_alpha(self.spin_score_bonus_alpha*255)

        elif self.spin_score_bonus_alpha > 0 :

            self.spin_score_bonus_alpha -= 6/self.fps
            self.spin_score.set_alpha(self.spin_score_bonus_alpha*255)

    for p in self.show_spinners :

        spinner_spin = pygame.transform.rotate(p[3],self.spin).convert_alpha()
        spinner_rect = spinner_spin.get_rect(center = (self.wi/2,self.he/2))
        
        self.my_settings.screen.blit(spinner_spin,spinner_rect)

def Spinning(self) :
    
    if self.spin_x >= 0 and self.spin_y >= 0 :

        if self.pos2[0] < self.wi/2 and self.pos2[1] >= self.he/2 :
            self.spin -= math.hypot(self.spin_x,self.spin_y)
        if self.pos2[0] >= self.wi/2 and self.pos2[1] < self.he/2 :
            self.spin += math.hypot(self.spin_x,self.spin_y)

    if self.spin_x >= 0 and self.spin_y < 0 :

        if self.pos2[0] < self.wi/2 and self.pos2[1] < self.he/2 :
            self.spin += math.hypot(self.spin_x,self.spin_y)
        if self.pos2[0] >= self.wi/2 and self.pos2[1] >= self.he/2 :
            self.spin -= math.hypot(self.spin_x,self.spin_y)

    if self.spin_x < 0 and self.spin_y >= 0 :

        if self.pos2[0] < self.wi/2 and self.pos2[1] < self.he/2 :
            self.spin -= math.hypot(self.spin_x,self.spin_y)
        if self.pos2[0] >= self.wi/2 and self.pos2[1] >= self.he/2 :
            self.spin += math.hypot(self.spin_x,self.spin_y)

    if self.spin_x < 0 and self.spin_y < 0 :

        if self.pos2[0] < self.wi/2 and self.pos2[1] >= self.he/2 :
            self.spin += math.hypot(self.spin_x,self.spin_y)
        if self.pos2[0] >= self.wi/2 and self.pos2[1] < self.he/2 :
            self.spin -= math.hypot(self.spin_x,self.spin_y)

    return self.spin

def GetCircle(self) :

    if self.e < len(self.circles) :

        if GetTime() - self.paused_time  >=  self.start_time + self.circles[self.e][2] - self.ar_time :

            coor = [round(self.circles[self.e][0] / 512 * self.wi * 3/4 * 0.86 + ReSize(360),2),
                    round(self.circles[self.e][1] / 384 * self.he       * 0.86 + ReSize(75), 2)]

            if self.circles[self.e][3] == 1 :
                self.numbers = 1
            else :
                self.numbers += 1

            number = self.number_font.render(f'{self.numbers}',False,self.white).convert()

            self.show_circles.append([GetTime()-self.paused_time,0,1,self.a_circle,coor,self.circles[self.e][2],number,self.circle,self.fade,1,self.acc_check,self.faded])

            self.e += 1

    elif self.e == len(self.circles) :

        self.end_time = GetTime()

        self.e += 1

def SetCircles(self) :

    for u in self.show_circles :

        if self.waiting == False :
        
            u[1] = GetTime() - u[0] - self.paused_time

            if u[1] >= self.ar_time and u[8] == False :
                u[8] = True

            if u[2] < 4 :

                a_c_rescale = self.a_c_s/u[2]
                u[3]        = pygame.transform.smoothscale(self.a_circle,(a_c_rescale,a_c_rescale)).convert_alpha()
            
            if u[8] == False :

                u[3].set_alpha(255*u[2]/2-255/2)
                u[7].set_alpha(255*u[2]-255)
                u[6].set_alpha(255*u[2]-255)

                u[2] += 6/self.fps
                u[2]  = round(u[2],2)
            
            else :

                u[3].set_alpha(255*u[9])
                u[7].set_alpha(255*u[9])
                u[6].set_alpha(255*u[9])

                u[9] -= 6/self.fps
                u[9]  = round(u[9],2)

        center_rect = u[4]
        a_c_rect    = u[3].get_rect(center = center_rect)
        circle_rect = u[7].get_rect(center = center_rect)
        number_rect = u[6].get_rect(center = center_rect)

        self.my_settings.screen.blit(u[3],a_c_rect)
        self.my_settings.screen.blit(u[7],circle_rect)
        self.my_settings.screen.blit(u[6],(number_rect[0]+ReSize(1),number_rect[1]+ReSize(8)))
    
        if u[1] >= self.ar_time + self.od_time :
            self.show_circles.pop(0)
            
            if u[11] == False :

                self.t_miss += 1

                self.acc.append(0)
                self.show_acc.append([self.acc_miss,u[4],GetTime(),0])

                self.acc_check = True

                self.health -= self.health_minus

                if self.combo >= 20 :
                    Play(self.sounds,'miss',1,self.volume,self.volume_effects)
                self.combo = 0

def GetFollowPoint(self) :

    if self.f < len(self.circles) - 1 :

        if GetTime() - self.paused_time  >=  self.start_time + self.circles[self.f][2] - self.ar_time :

            coor1 = [round(self.circles[self.f][0]   / 512 * self.wi * 3/4 * 0.86 + ReSize(360),2),
                     round(self.circles[self.f][1]   / 384 * self.he       * 0.86 + ReSize(75), 2)]
            coor2 = [round(self.circles[self.f+1][0] / 512 * self.wi * 3/4 * 0.86 + ReSize(360),2),
                     round(self.circles[self.f+1][1] / 384 * self.he       * 0.86 + ReSize(75), 2)]

            if coor1 != coor2 and self.circles[self.f+1][3] != 1 :

                hypot = math.hypot(coor2[0]-coor1[0],coor2[1]-coor1[1])
                tan   = abs(coor2[0]-coor1[0])

                if tan == 0 :
                    followpoint_angle = 90

                else :
                    
                    if (coor1[0] < coor2[0] and coor1[1] < coor2[1]) or (coor1[0] > coor2[0] and coor1[1] > coor2[1]) :
                        followpoint_angle = -math.degrees(math.acos(tan/hypot))

                    else :
                        followpoint_angle = math.degrees(math.acos(tan/hypot))

                followpoint = pygame.transform.smoothscale(self.followpoint,(hypot*0.9,self.followpoint.get_height())).convert_alpha()
                followpoint = pygame.transform.rotate(followpoint,followpoint_angle).convert_alpha()

                if coor1[0] >= coor2[0] : x = coor2[0]
                if coor1[1] >= coor2[1] : y = coor2[1]
                if coor1[0] <  coor2[0] : x = coor1[0]
                if coor1[1] <  coor2[1] : y = coor1[1]

                center_rect      = (abs((coor2[0]-coor1[0])/2) + x,
                                    abs((coor2[1]-coor1[1])/2) + y)

                followpoint_rect = followpoint.get_rect(center = center_rect)
            
                self.show_followpoints.append([GetTime()-self.paused_time,0,followpoint_rect,followpoint,0,self.circles[self.f+1][2]-self.circles[self.f][2]])

            self.f += 1

def SetFollowPoints(self) :

    for f in self.show_followpoints :

        if self.waiting == False :
        
            f[1] = GetTime() - f[0] - self.paused_time

            if f[4] < 1 and f[1] < f[5] :

                f[4] += 6/self.fps
                f[4]  = round(f[4],2)

            f[3].set_alpha(f[4]*255)

            if f[1] > f[5] + self.ar_time or self.acc_check :

                f[4] -= 6/self.fps
                f[4]  = round(f[4],2)

                if f[1] > f[5] + self.ar_time + self.od_time :
                    self.show_followpoints.pop(0)

        self.my_settings.screen.blit(f[3],f[2])