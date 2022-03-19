import math

from tools import get_time, play

def SetAcc(self) :

    for v in range(len(self.show_circles)) :

        if self.acc_check == False and self.show_circles[v][11] == False :

            distance = math.hypot(self.show_circles[v][4][0]-self.pos[0],self.show_circles[v][4][1]-self.pos[1])

            if distance < self.c_s/2*115/121 :

                self.acc_check = True

                difference = get_time() - (self.start_time + self.show_circles[v][5] + self.paused_time) + self.offset
                self.total_ur.append(difference)

                if abs(difference) < self.od_time :

                    if abs(difference) < self.od_time/4 :
                        self.hit_value = 300
                        self.show_ur.append([self.blue,278*difference/self.od_time/2,get_time(),0])

                    if abs(difference) > self.od_time/4 and abs(difference) < self.od_time/2 :
                        self.hit_value = 100
                        self.show_ur.append([self.green,278*difference/self.od_time/2,get_time(),0])
                        self.show_acc.append([self.acc_100,self.show_circles[v][4],get_time(),0])
                    
                    if abs(difference) > self.od_time/2 :
                        self.hit_value = 50
                        self.show_ur.append([self.orange,278*difference/self.od_time/2,get_time(),0])
                        self.show_acc.append([self.acc_50,self.show_circles[v][4],get_time(),0])

                    self.acc.append(round(self.hit_value/3,2))
                    health_bonus = round(self.hit_value/30,2)

                    if self.health + health_bonus < self.max_health :
                        self.health += health_bonus
                    else :
                        self.health = self.max_health

                    play(self.sounds,'hit',0.5,self.volume,self.volume_effects)
                    self.combo += 1

                else :

                    self.hit_value = 0

                    self.acc.append(0)
                    self.show_acc.append([self.acc_miss,self.show_circles[v][4],get_time(),0])

                    self.health -= self.health_minus

                    if self.combo >= 20 :
                        play(self.sounds,'miss',1,self.volume,self.volume_effects)
                    self.combo = 0

                self.show_circles[v][8]  = True
                self.show_circles[v][11] = True
