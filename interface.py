import pygame
from tools import GetTime, ReSize

def DarkenScreen(self) :

    if self.game_break == False :
        pygame.draw.rect(self.my_settings.screen,(0,0,0),self.noir)
        #self.UI = True

    else :
        self.my_settings.screen.blit(self.bg,(0,0))
        self.my_settings.screen.blit(self.dim,(0,0))
        #self.UI = False

def SetShowOnScreen(self) :

    if self.waiting == False :

        self.trail_count += round(5000/self.fps)
        if self.trail_count > 100 :

            self.trail_pos.append([self.pos,self.cursor_trail,255])
            self.trail_count = 0
        
        if len(self.trail_pos) > 8 :
            self.trail_pos.pop(0)
        
        self.health    -= self.passive_health*160/self.fps
        self.health_bar = pygame.Rect(ReSize(20),ReSize(20),ReSize(600*self.health/600),ReSize(20))

    for s in self.show_ur :
        s[3] = GetTime() - s[2] - self.paused_time

    if self.show_ur != [] and (len(self.show_ur) > 20 or self.show_ur[0][3] >= 8000) :
        self.show_ur.pop(0)

    for s in range(len(self.show_acc)) :

        showed_time = GetTime() - self.show_acc[s][2]

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

        if GetTime() - self.offset_time - self.paused_time >= 1000 :
            self.show_offset = False

def ShowOnScreen(self) :

    if self.UI == False and self.UI_alpha > 0 :
            
        self.UI_alpha -= 20*160/self.fps

    if self.UI_alpha > 0 :

        self.combo_txt.set_alpha(self.UI_alpha)
        self.score_txt.set_alpha(self.UI_alpha)
        self.acc_txt.set_alpha(self.UI_alpha)
        self.fps_txt.set_alpha(self.UI_alpha)

        self.my_settings.screen.blit(self.combo_txt,(ReSize(20),ReSize(960)))
        self.my_settings.screen.blit(self.score_txt,(ReSize(1910)-self.score_txt.get_width(),ReSize(-20)))
        self.my_settings.screen.blit(self.acc_txt,(ReSize(1910)-self.acc_txt.get_width(),ReSize(80)))
        self.my_settings.screen.blit(self.fps_txt,(ReSize(1910)-self.fps_txt.get_width(),ReSize(1075)-self.fps_txt.get_height()))

        pygame.draw.rect(self.my_settings.screen,self.grey,self.health_bar_bg)
        pygame.draw.rect(self.my_settings.screen,self.white,self.health_bar)

    pygame.draw.rect(self.my_settings.screen,self.orange,self.ur_50)
    pygame.draw.rect(self.my_settings.screen,self.green,self.ur_100)
    pygame.draw.rect(self.my_settings.screen,self.blue,self.ur_300)
    pygame.draw.rect(self.my_settings.screen,self.white,self.ur_middle)

    for u in self.show_ur :
        
        ur_hit = pygame.Rect(ReSize(961+u[1]),ReSize(1039),ReSize(2),ReSize(30))
        pygame.draw.rect(self.my_settings.screen,u[0],ur_hit)

    for s in self.show_acc :

        show_acc_rect = s[0].get_rect(center = (s[1][0],s[1][1]-ReSize(60)))
        self.my_settings.screen.blit(s[0],show_acc_rect)
    
    if self.show_offset :

        offset_txt_rect = self.offset_txt.get_rect(center = (self.wi/2,ReSize(20)))
        self.my_settings.screen.blit(self.offset_txt,offset_txt_rect)

    if self.spin_score_bonus_alpha > 0 :

        spin_score_rect = self.spin_score.get_rect(center = (self.wi/2,self.he/4*3))
        self.my_settings.screen.blit(self.spin_score,spin_score_rect)

    for t in self.trail_pos :

        if self.waiting == False :

            t[2] -= 7*160/self.fps
        t[1].set_alpha(t[2])

        trail_rect = t[1].get_rect(center = t[0])
        self.my_settings.screen.blit(t[1],trail_rect)

    if self.waiting == False :
        self.pos3 = pygame.mouse.get_pos()
    
    cursor_rect = self.cursor.get_rect(center = self.pos3)
    self.my_settings.screen.blit(self.cursor,cursor_rect)

    if self.waiting :

        waiting_cursor_rect = self.cursor.get_rect(center = self.pos)
        self.my_settings.screen.blit(self.cursor,waiting_cursor_rect)

def SetFps(self) :

    self.fps = round(1000 / (GetTime() - self.fps_time),2)

    self.fpss.append(self.fps)
    if len(self.fpss) > 40 :
        self.fpss.pop(0)

    for i in self.fpss :
        self.avg_fps += i

    self.fps_time = GetTime()
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

def HideUI(self) :

    if (self.event.type == pygame.KEYDOWN and self.event.key == pygame.K_TAB and self.key[pygame.K_LSHIFT]) or\
       (self.event.type == pygame.KEYDOWN and self.event.key == pygame.K_LSHIFT and self.key[pygame.K_TAB]) :
        
        if self.UI :
            self.UI = False
        else :
            self.UI       = True
            self.UI_alpha = 255