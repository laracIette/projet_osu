import pygame
from settings import Settings
from tools import rs,get_time

my_settings = Settings()

def DarkenScreen(self) :

    if self.game_break == False :
        pygame.draw.rect(my_settings.screen,(0,0,0),self.noir)
        #self.UI = True

    else :
        my_settings.screen.blit(self.bg,(0,0))
        #my_settings.screen.blit(dim,(0,0))
        #self.UI = False

def ShowOnScreen(self) :

    if self.UI :

        my_settings.screen.blit(self.combo_txt,(rs(20),rs(960)))
        my_settings.screen.blit(self.score_txt,(rs(1910)-self.score_txt.get_width(),rs(-20)))
        my_settings.screen.blit(self.acc_txt,(rs(1910)-self.acc_txt.get_width(),rs(80)))
        my_settings.screen.blit(self.fps_txt,(rs(1910)-self.fps_txt.get_width(),rs(1075)-self.fps_txt.get_height()))

        pygame.draw.rect(my_settings.screen,self.grey,self.health_bar_bg)
        pygame.draw.rect(my_settings.screen,self.white,self.health_bar)
        
    pygame.draw.rect(my_settings.screen,self.orange,self.ur_50)
    pygame.draw.rect(my_settings.screen,self.green,self.ur_100)
    pygame.draw.rect(my_settings.screen,self.blue,self.ur_300)
    pygame.draw.rect(my_settings.screen,self.white,self.ur_middle)

    for u in self.show_ur :
        
        ur_hit = pygame.Rect(rs(961+u[1]),rs(1039),rs(2),rs(30))
        pygame.draw.rect(my_settings.screen,u[0],ur_hit)

    for s in self.show_acc :

        show_acc_rect = s[0].get_rect(center = (s[1][0],s[1][1]-rs(60)))
        my_settings.screen.blit(s[0],show_acc_rect)
    
    if self.show_offset :

        offset_txt_rect = self.offset_txt.get_rect(center = (self.wi/2,rs(20)))
        my_settings.screen.blit(self.offset_txt,offset_txt_rect)

    if self.spin_score_bonus_alpha > 0 :

        spin_score_rect = self.spin_score.get_rect(center = (self.wi/2,self.he/4*3))
        my_settings.screen.blit(self.spin_score,spin_score_rect)

    for t in self.trail_pos :

        if self.waiting == False :

            t[2] -= 7*160/self.fps
        t[1].set_alpha(t[2])

        trail_rect = t[1].get_rect(center = t[0])
        my_settings.screen.blit(t[1],trail_rect)

    if self.waiting == False :
        self.pos3 = pygame.mouse.get_pos()
    
    cursor_rect = self.cursor.get_rect(center = self.pos3)
    my_settings.screen.blit(self.cursor,cursor_rect)

    if self.waiting :

        waiting_cursor_rect = self.cursor.get_rect(center = self.pos)
        my_settings.screen.blit(self.cursor,waiting_cursor_rect)

def SetShowOnScreen(self) :

    if self.waiting == False :

        self.trail_count += round(5000/self.fps)
        if self.trail_count > 100 :

            self.trail_pos.append([self.pos,self.cursor_trail,255])
            self.trail_count = 0
        
        if len(self.trail_pos) > 8 :
            self.trail_pos.pop(0)
        
        self.health    -= self.passive_health*160/self.fps
        self.health_bar = pygame.Rect(rs(20),rs(20),rs(600*self.health/600),rs(20))

    for s in self.show_ur :
        s[3] = get_time() - s[2] - self.paused_time

    if self.show_ur != [] and (len(self.show_ur) > 20 or self.show_ur[0][3] >= 8000) :
        self.show_ur.pop(0)

    for s in range(len(self.show_acc)) :

        showed_time = get_time() - self.show_acc[s][2]

        if showed_time < 300 :

            self.show_acc[s][3] += 255/300*1000/self.fps

        if showed_time >= 300 :

            self.show_acc[s][1][1] += 0.5*160/self.fps

        if showed_time > 400 :

            self.show_acc[s][3] -= 255/100*1000/self.fps

        self.show_acc[s][0].set_alpha(self.show_acc[s][3])
        self.show_acc[s][0].convert_alpha()

        if showed_time > 500 :

            self.show_acc.pop(0)
            break

    if self.show_offset :
        
        if self.offset < 0 :
            self.offset_txt = self.fps_font.render(f'Local offset : {self.offset}ms',False,self.white).convert()
        else :
            self.offset_txt = self.fps_font.render(f'Local offset : +{self.offset}ms',False,self.white).convert()

        if get_time() - self.offset_time - self.paused_time >= 1000 :
            self.show_offset = False

def SetFps(self) :

    self.fps = round(1000 / (get_time() - self.fps_time),2)

    self.fpss.append(self.fps)
    if len(self.fpss) > 40 :
        self.fpss.pop(0)

    for i in self.fpss :
        self.avg_fps += i

    self.fps_time = get_time()
    self.avg_fps /= len(self.fpss)
    self.fps_txt  = self.fps_font.render(f'{round(self.avg_fps)}fps',False,self.white).convert()
    self.avg_fps  = 0

def UItextRenders(self) :

    if self.acc_check :

        self.accuracy = 0

        if len(self.acc) != 0 :

            for w in self.acc :
                self.accuracy += w

            self.accuracy /= len(self.acc)

        if self.combo > 2 :
            combo_multiplier = self.combo - 2
        else :
            combo_multiplier = 0

        self.score += round(self.hit_value + (self.hit_value * ((combo_multiplier * self.difficulty_multiplier * self.mod_multiplier) / 25)))
        
        self.acc_txt    = self.acc_font.render(f'{round(self.accuracy,2)}%',False,self.white).convert()
        self.combo_txt  = self.combo_font.render(f'{self.combo}x',False,self.white).convert()
        self.score_txt  = self.combo_font.render(str(self.score),False,self.white).convert()

        self.acc_check = False