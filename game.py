import math
import pygame
from sounds import Play
from tools import GetTime
from setthings import SetAcc
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

def SetMap(self) :

    circles0,self.circles = [],[]
    self.show_circles     = []

    cs_t,ar_t,od_t,hp_t = [],[],[],[]

    spinner_lock       = False
    spinners0,self.spinners = [],[]
    self.show_spinners      = []

    a   = 0
    map = self.songs[self.ii][2][self.diff]
        

    with open(map,'r') as map_file :

        for i in map_file :

            if spinner_lock == False :
                
                for o in i:

                    if o == 's' :

                        spinner_lock = True

            if spinner_lock == False :

                a += 1

                if i == '\n' :
                    continue

                elif a == 1 :
                    for o in i :
                        if o != '\n' :
                            cs_t.append(o)

                    self.cs = ''.join(cs_t)
                    self.cs = float(self.cs)

                elif a == 2 :
                    for o in i :
                        if o != '\n' :
                            ar_t.append(o)

                    ar = ''.join(ar_t)
                    ar = float(ar)

                    self.ar_time = 450*10/ar

                elif a == 3 :
                    for o in i :
                        if o != '\n' :
                            od_t.append(o)

                    self.od = ''.join(od_t)
                    self.od = float(self.od)

                    self.od_time = 100*10/self.od
                
                elif a == 4 :
                    for o in i :
                        if o != '\n' :
                            hp_t.append(o)

                    self.hp = ''.join(hp_t)
                    self.hp = float(self.hp)

                else :
                    circles0.append(i)

            else :
                self.spinners.append(i)

    cycle = 1
    for c in circles0[0] :
        if c == ',' :
                cycle += 1

    tab = []
    for j in circles0 :

        for k in j :

            if k != ',' and k != '\n' :
                tab.append(k)

            else :
                tab = ''.join(tab)
                self.circles.append(tab)
                tab = []

    circles0 = []
    for m in self.circles :
        circles0.append(int(m))
    
    num     = 0
    self.circles = []

    self.start_offset = 2500-circles0[2]

    for i in range(int(len(circles0)/cycle)) :
        circles0[i*cycle+2] += self.start_offset

        for j in range(cycle) :

            tab.append(circles0[num])
            num += 1

        self.circles.append(tab)
        tab = []
    
    for j in self.spinners :

        for k in j :

            if k != ',' and k != 's' and k != '\n' :
                tab.append(k)

            elif tab != [] :
                tab = ''.join(tab)
                spinners0.append(tab)
                tab = []
    
    for r in range(len(spinners0)) :
        spinners0[r]  = int(spinners0[r])
        spinners0[r] += self.start_offset

    self.spinners = []
    h        = 0
    for r in range(int(len(spinners0)/2)) :

        self.spinners.append([spinners0[h],spinners0[h+1]])
        
        h += 2

    c = 0
    u = 0
    hit_objects = []
    for i in range(len(self.circles) + len(self.spinners)) :

        if self.spinners == [] or u == len(self.spinners) :
            hit_objects.append([self.circles[c][2],0])
            c += 1
            continue

        if self.circles == [] or c == len(self.circles) :
            hit_objects.append([self.spinners[u][0],1])
            hit_objects.append([self.spinners[u][1],1])
            u += 1
            continue

        if self.circles[c][2] < self.spinners[u][0] :
            hit_objects.append([self.circles[c][2],0])
            
            if c < len(self.circles) : c += 1

        else :
            hit_objects.append([self.spinners[u][0],1])
            hit_objects.append([self.spinners[u][1],1])
            
            if u < len(self.spinners) : u += 1
    
    self.game_breaks = []
    for p in range(len(hit_objects)-1) :
        
        if (hit_objects[p+1][0] - hit_objects[p][0] >= 5000 and hit_objects[p][1] != 1) or\
            (hit_objects[p+1][0] - hit_objects[p][0] >= 5000 and hit_objects[p+1][1] != 1) :
            self.game_breaks.append([hit_objects[p][0],hit_objects[p+1][0]])

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

    with open('assets\\settings.txt','w') as settings_file :

        modifs = [self.offset,self.volume,self.volume_music,self.volume_effects]

        for a in range(len(self.lines)) :

            settings_file.write(self.lines[a].replace(self.lines[a],f'{modifs[a]}\n'))


def Write(self) :

    with open('assets\\settings.txt','w') as settings_file :

        modifs = [self.offset,self.volume,self.volume_music,self.volume_effects]

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
        
        SetAcc(self)
        
    if self.event.type == pygame.KEYUP and (self.event.key == pygame.K_x or self.event.key == pygame.K_v) :
        self.click_check = False