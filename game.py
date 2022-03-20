import math
import pygame
from sounds import Play
from tools import GetTime
from gameend import ProposeOffset

def SetBreak(self) :
    for g in self.game_breaks :

        if GetTime() >= self.start_time + g[0] - self.paused_time + 1000 :
            self.game_break = True
        
        if GetTime() >= self.start_time + g[1] - self.paused_time - 1000 :
            self.game_break = False
            self.game_breaks.pop(0)

def ApplyBreaks(self) :
    
    if GetTime() >= self.music_start - self.start_offset/2.5 and self.break_lock == False :
        self.game_break = False
        self.break_lock = True

    if GetTime() >= self.end_time + self.start_offset/2.5 :
        self.game_break = True

def StartGame(self) :
    
    pygame.mixer.music.play()
    self.playing = True
    
def EndGame(self) :

    self.running = False

    pygame.mixer.music.pause()

    if self.health <= 0 :
        Play(self.sounds,'fail',1,self.volume,self.volume_effects)
        self.death = True

    if self.total_ur != [] :
        self.offset += ProposeOffset(self)

    Write(self)

def Write(self) :

    with open('assets\\settings.txt','w') as settings_file :

        modifs = [self.offset,self.volume,self.volume_music,self.volume_effects,self.skin]

        for a in range(len(self.lines)) :

            settings_file.write(self.lines[a].replace(self.lines[a],f'{modifs[a]}\n'))

def GetPause(self) :
    
    if (self.event.type == pygame.KEYDOWN and self.event.key == pygame.K_ESCAPE) :
        self.running = False
        
        if self.waiting :
            self.paused_time += GetTime() - self.pause_time

        self.pause_time = GetTime()

        pygame.mouse.set_visible(True)
        pygame.mixer.music.pause()

        self.my_settings.screen.blit(self.pause_screen,(0,0))
        pygame.display.flip()
        
        Write(self)

        Pause(self)

def Pause(self) :

    loop = True
    while loop :

        for self.event in pygame.event.get() :

            if self.event.type == pygame.KEYDOWN and self.event.key == pygame.K_ESCAPE :
                loop = False

                self.running = True
                self.waiting = True

                pygame.mouse.set_visible(False)

                self.fps_time += GetTime() - self.pause_time

            if self.event.type == pygame.KEYDOWN and self.event.key == pygame.K_q :
                loop = False

                self.to_menu = True

            GameQuit(self)

def UnPause(self) :

    pos1 = pygame.mouse.get_pos()

    if (self.event.type == pygame.KEYDOWN and self.event.key == pygame.K_x) or (self.event.type == pygame.KEYDOWN and self.event.key == pygame.K_v) :
        
        distance1 = math.hypot(pos1[0]-self.pos[0],pos1[1]-self.pos[1])

        if distance1 < 5 :

            self.waiting = False

            pygame.mixer.music.unpause()
                                        
            self.paused_time += GetTime() - self.pause_time

def ChangeOffset(self) :
    if self.event.type == pygame.KEYDOWN and self.event.key == pygame.K_EQUALS :

        if self.key[pygame.K_LSHIFT] :
            self.offset += 1
        else :
            self.offset += 5

        self.offset_time = GetTime()
        self.show_offset = True

    if self.event.type == pygame.KEYDOWN and self.event.key == pygame.K_MINUS :

        if self.key[pygame.K_LSHIFT] :
            self.offset -= 1
        else :
            self.offset -= 5

        self.offset_time = GetTime()
        self.show_offset = True

def GameQuit(self) :

    if self.event.type == pygame.QUIT or (self.event.type == pygame.KEYDOWN and self.event.key == pygame.K_F4 and self.key[pygame.K_LALT]) :

        Write(self)

        pygame.quit()
        exit(0)

def GetClicks(self) :

    if self.event.type == pygame.KEYDOWN and (self.event.key == pygame.K_x or self.event.key == pygame.K_v) :

        if self.click_check == False :
            self.click_check = True
        
        GetAcc(self)
        
    if self.event.type == pygame.KEYUP and (self.event.key == pygame.K_x or self.event.key == pygame.K_v) :
        self.click_check = False

def GetAcc(self) :

    for v in range(len(self.show_circles)) :

        if self.acc_check == False and self.show_circles[v][11] == False :

            distance = math.hypot(self.show_circles[v][4][0]-self.pos[0],self.show_circles[v][4][1]-self.pos[1])

            if distance < self.c_s/2*115/121 :

                self.acc_check = True

                difference = GetTime() - (self.start_time + self.show_circles[v][5] + self.paused_time) + self.offset
                self.total_ur.append(difference)

                if abs(difference) < self.od_time :

                    if abs(difference) < self.od_time/4 :
                        self.t_300 += 1

                        self.hit_value = 300
                        self.show_ur.append([self.blue,278*difference/self.od_time/2,GetTime(),0])

                    if abs(difference) > self.od_time/4 and abs(difference) < self.od_time/2 :
                        self.t_100 += 1

                        self.hit_value = 100
                        self.show_ur.append([self.green,278*difference/self.od_time/2,GetTime(),0])
                        self.show_acc.append([self.acc_100,self.show_circles[v][4],GetTime(),0])
                    
                    if abs(difference) > self.od_time/2 :
                        self.t_50 += 1

                        self.hit_value = 50
                        self.show_ur.append([self.orange,278*difference/self.od_time/2,GetTime(),0])
                        self.show_acc.append([self.acc_50,self.show_circles[v][4],GetTime(),0])

                    self.acc.append(round(self.hit_value/3,2))
                    health_bonus = round(self.hit_value/30,2)

                    if self.health + health_bonus < self.max_health :
                        self.health += health_bonus
                    else :
                        self.health = self.max_health

                    Play(self.sounds,'hit',0.5,self.volume,self.volume_effects)
                    self.combo += 1

                else :
                    
                    self.t_miss += 1

                    self.hit_value = 0
                    self.show_acc.append([self.acc_miss,self.show_circles[v][4],GetTime(),0])

                    self.acc.append(0)

                    self.health -= self.health_minus

                    if self.combo >= 20 :
                        Play(self.sounds,'miss',1,self.volume,self.volume_effects)
                    self.combo = 0

                self.show_circles[v][8]  = True
                self.show_circles[v][11] = True