import pygame
from sounds import Play
from tools import get_time, rs
import math

def SetSpinners(self) :

    if self.waiting == False :

        if self.show_spinner :

            for p in self.show_spinners :

                p[1] = get_time() - p[0] - self.paused_time
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

                    self.click_time = get_time()

                self.pos2 = pygame.mouse.get_pos()

                spin_center = math.hypot(self.wi/2-self.pos[0],self.he/2-self.pos[1])
                self.spin_x      = (self.pos[0]-self.pos2[0])/spin_center*60
                self.spin_y      = (self.pos[1]-self.pos2[1])/spin_center*60
                
                self.spin = Spinning(self)
                
                for p in self.show_spinners :

                    if get_time() - self.click_time >= p[2] / 2 :

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

                            self.spin_score_bonus_time = get_time()
                            self.spin_score_bonus     += 1

                            self.spin_score = self.combo_font.render(str(self.spin_score_bonus*1000),False,self.white).convert()

        if get_time() < self.spin_score_bonus_time + 1000 :

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

def GetSpinner(self) :

    if self.q < len(self.spinners) :

        if get_time() - self.paused_time  >=  self.start_time + self.spinners[self.q][0] - self.ar_time :
            
            self.show_spinners.append([get_time()-self.paused_time,0,self.spinners[self.q][1]-self.spinners[self.q][0],self.spinner,0])

            self.show_spinner     = True
            self.spinner_fade     = True
            self.click_time_check = False
            self.spin_score_bonus = 0

            self.q += 1

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

def SetCircles(self) :

    for u in self.show_circles :

        if self.waiting == False :
        
            u[1] = get_time() - u[0] - self.paused_time

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

        center_rect = (u[4][0],u[4][1])
        a_c_rect    = u[3].get_rect(center = center_rect)
        circle_rect = u[7].get_rect(center = center_rect)
        number_rect = u[6].get_rect(center = center_rect)

        self.my_settings.screen.blit(u[3],a_c_rect)
        self.my_settings.screen.blit(u[7],circle_rect)
        self.my_settings.screen.blit(u[6],(number_rect[0]+rs(1),number_rect[1]+rs(8)))
    
        if u[1] >= self.ar_time + self.od_time :
            self.show_circles.pop(0)
            
            if u[11] == False :

                self.acc.append(0)
                self.show_acc.append([self.acc_miss,u[4],get_time(),0])

                self.acc_check = True

                self.health -= self.health_minus

                if self.combo >= 20 :
                    Play(self.sounds,'miss',1,self.volume,self.volume_effects)
                self.combo = 0

def GetCircle(self) :

    if self.e < len(self.circles) :

        if get_time() - self.paused_time  >=  self.start_time + self.circles[self.e][2] - self.ar_time :

            coor = [round(self.circles[self.e][0]/512*self.wi*3/4*0.86+rs(360),2),round(self.circles[self.e][1]/384*self.he*0.86+rs(75),2)]

            if self.circles[self.e][3] == 1 :
                self.numbers = 1
            else :
                self.numbers += 1

            number = self.number_font.render(f'{self.numbers}',False,self.white).convert()

            self.show_circles.append([get_time()-self.paused_time,0,1,self.a_circle,coor,self.circles[self.e][2],number,self.circle,self.fade,1,self.acc_check,self.faded])

            self.e += 1

    elif self.e == len(self.circles) :

        self.end_time = get_time()

        self.e += 1