import pygame
import glob
import os
from settings import Settings
from math import inf
from tools import load,SkinSelect,SongSelect,Score,get_time

my_settings = Settings()
wi = my_settings.width
he = my_settings.height

class Run :

    def __init__(self,ii,diff,songs,skin) :

        circles0,circles = [],[]
        show_circles     = []

        cs_t,ar_t = [],[]

        a   = 0
        map = songs[ii][2][diff]
        with open(map,'r') as file :

            for i in file :

                a += 1

                if i == '\n' :
                    continue

                elif a == 1 :
                    for q in i :
                        if q != '\n' :
                            cs_t.append(q)

                    cs = ''.join(cs_t)
                    cs = float(cs)

                elif a == 2 :
                    for o in i :
                        if o != '\n' :
                            ar_t.append(o)

                    ar = ''.join(ar_t)
                    ar = float(ar)
                    ar = 450*10/ar

                else :
                    circles0.append(i)

            tab = []
            for j in circles0 :

                for k in j :
                    if k != ',' and k != '\n' :
                        tab.append(k)

                    else :
                        tab = ''.join(tab)
                        circles.append(tab)
                        tab = []

        circles0 = []
        for m in circles :
            circles0.append(int(m))
        
        num     = 0
        circles = []

        for i in range(int(len(circles0)/4)) :
            circles0[i*4+2] += 3000

            for j in range(4) :

                tab.append(circles0[num])
                num += 1

            circles.append(tab)

            tab = []
        
        pause_screen = load('images\\pause_screen.png',(wi,he))
        dim          = load('images\\noir93.png',(wi,he))
        bg           = pygame.transform.scale(songs[ii][0],(wi,he))
        
        c_s     = 121/cs*4.9/1920*wi
        circle  = load(f'skins\\{skin}\\hitcircle.png',(c_s,c_s))

        a_c_s    = c_s*4
        a_circle = load(f'skins\\{skin}\\approachcircle.png',(a_c_s,a_c_s))

        number_font = pygame.font.Font('assets\\fonts\\LeagueSpartanBold.ttf', round(c_s/2))

        cursor       = load(f'skins\\{skin}\\cursor.png',(c_s,c_s))
        t_s          = c_s/4
        cursor_trail = load(f'skins\\{skin}\\cursortrail.png',(t_s,t_s))
        trail_pos    = []
        trail_count  = 0

        fpss     = []
        avg_fps  = 0
        fps_time = get_time()
        fps_font = pygame.font.SysFont('arial', round(20/1280*wi))

        offset = 0
        
        acc       = []
        acc_check = False
        accuracy  = 0
        acc_font  = pygame.font.SysFont('segoeuisemibold', round(30/1280*wi))

        start_time  = get_time()
        paused_time = 0
        pause_time  = 0
        end_time    = inf

        combo      = 0
        combo_font = pygame.font.SysFont('segoeuisemibold', round(60/1280*wi))
        
        hit_sound = pygame.mixer.Sound(f'assets\\skins\\{skin}\\hit.ogg')
        hit_sound.set_volume(0.5)
        
        miss_sound = pygame.mixer.Sound(f'assets\\skins\\{skin}\\miss.ogg')
        miss_sound.set_volume(1)

        music_start = get_time() + 3000
        playing = False

        pygame.mixer.music.load(songs[ii][1])
        pygame.mixer.music.set_volume(1)

        e = 0

        running = True
        while running :

            if get_time() >= music_start and playing == False:
            
                pygame.mixer.music.play()
                playing = True

            acc_check  = False
            
            my_settings.clock.tick(my_settings.frequence)

            if e < len(circles) :

                if get_time() - paused_time  >=  start_time + circles[e][2] - ar :

                    create_time = get_time()
                    coor        = [circles[e][0]/512*wi*3/4*0.86+240/1280*wi,circles[e][1]/384*he*0.86+50/1280*wi]

                    if circles[e][3] == 1 :
                        numbers = 1
                    else :
                        numbers += 1

                    number = number_font.render(f'{numbers}',False,(255,255,255)).convert()

                    show_circles.append([create_time,0,1,a_circle,coor,circles[e][2],number,circle])

                    e += 1

            elif e == len(circles) :

                end_time = get_time()
                e += 1

            if get_time() >= end_time + 3000 :
                running = False

                Score(accuracy)
                menu()
            
            my_settings.screen.blit(bg,(0,0))
            my_settings.screen.blit(dim,(0,0))
            
            if len(show_circles) > 0 :

                for u in show_circles :
                    
                    u[1] = get_time() - u[0]

                    if u[2] < 6 :
                        a_c_width = u[3].get_width()

                        a_c_rescale = a_c_s*1/u[2]

                        u[3]  = pygame.transform.scale(a_circle,(a_c_rescale,a_c_rescale))
                        u[3].set_alpha(255*u[2]/2-255/2)
                        u[2] += 6/fps
                        u[2]  = round(u[2],2)

                    if u[1] < ar :
                        my_settings.screen.blit(u[3],(u[4][0]-a_c_width/2+1,u[4][1]-a_c_width/2+1))
                        my_settings.screen.blit(u[7],(u[4][0]-c_s/2,u[4][1]-c_s/2))
                        my_settings.screen.blit(u[6],(u[4][0]-u[6].get_width()/2+2*1920/wi,u[4][1]-u[6].get_height()/2+7*1920/wi))

                    if u[1] >= 2*ar :
                        show_circles.pop(0)
                        
                        if acc_check == False :
                            acc.append(0)

                            if combo >= 20 :
                                miss_sound.play()
                            combo = 0

            if len(acc) != 0 :

                for w in acc :
                    accuracy += w

                accuracy /= len(acc)

            acc_txt = acc_font.render(f'{round(accuracy,2)}%',False,(255,255,255)).convert()
            my_settings.screen.blit(acc_txt,(1170/1280*wi,5/1280*wi))
            
            accuracy = 0
        
            fps = round(1000 / (get_time() - fps_time),2)

            fpss.append(fps)
            if len(fpss) > 40 :
                fpss.pop(0)

            for i in fpss :
                avg_fps += i

            avg_fps /= len(fpss)

            fps_txt = fps_font.render(f'{round(avg_fps)}fps',False,(255,255,255)).convert()
            my_settings.screen.blit(fps_txt,(0,0))
            
            avg_fps  = 0
            fps_time = get_time()
            
            pos = pygame.mouse.get_pos()

            trail_count += round(5000 / fps)
            if trail_count > 100 :

                trail_pos.append([pos,cursor_trail,255])
                trail_count = 0
            
            if len(trail_pos) > 8 :
                trail_pos.pop(0)
            
            for t in trail_pos :

                t[2] -= 7*160/fps
                t[1].set_alpha(t[2])

                my_settings.screen.blit(t[1],(t[0][0]-t_s/2,t[0][1]-t_s/2))

            my_settings.screen.blit(cursor,(pos[0]-c_s/2,pos[1]-c_s/2))

            combo_txt = combo_font.render(f'{combo}x',False,(255,255,255)).convert()
            my_settings.screen.blit(combo_txt,(20*1920/wi,960*1080/he))

            pygame.mouse.set_visible(False)
            pygame.display.flip()

            key = pygame.key.get_pressed()
            for event in pygame.event.get() :

                if (event.type == pygame.KEYDOWN and event.key == pygame.K_x) or (event.type == pygame.KEYDOWN and event.key == pygame.K_v) :

                    if len(show_circles) > 0 :

                        for v in range(len(show_circles)) :

                            if acc_check == False :

                                circle_rect = circle.get_rect()
                                circle_rect.center = show_circles[v][4]

                                if circle_rect.collidepoint(pos) :

                                    acc_check = True

                                    difference = abs(get_time() - (start_time + show_circles[v][5] + paused_time) + offset)

                                    if difference < 200 :

                                        if difference < 50 :
                                            acc.append(100)

                                        if difference > 50 and difference < 100 :
                                            acc.append(33.33)
                                        
                                        if difference > 100 :
                                            acc.append(16.67)

                                        hit_sound.play()
                                        combo += 1

                                    else :
                                        acc.append(0)

                                        if combo >= 20 :
                                            miss_sound.play()
                                        combo = 0

                                    show_circles.pop(v)

                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and key[pygame.K_LALT]) :
                    running = False

                    pygame.quit()
                    exit()

                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) :
                    running = False

                    pause_time = get_time()

                    pygame.mouse.set_visible(True)
                    pygame.mixer.music.pause()

                    my_settings.screen.blit(pause_screen,(0,0))
                    pygame.display.flip()

                    loop = True
                    while loop :

                        for event in pygame.event.get() :

                            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE :
                                loop    = False
                                running = True

                                paused_time += get_time() - pause_time

                                pygame.mixer.music.unpause()

                            if event.type == pygame.KEYDOWN and event.key == pygame.K_q :
                                loop = False

                                menu()

                            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and key[pygame.K_LALT]) :
                                loop = False

                                pygame.quit()
                                exit()

def menu() :

    pygame.mouse.set_visible(True)

    noir = load('images\\noir.png',(wi,he))
    font = pygame.font.Font('assets\\fonts\\shippori.ttf', round(30/1280*wi))

    my_settings.screen.blit(noir,(0,0))
    
    skin  = 'whitecat'
    songs = SongSelect()

    loop = True
    while loop :

        my_settings.clock.tick(my_settings.frequence)
        pygame.display.flip()

        key = pygame.key.get_pressed()
        for event in pygame.event.get() :

            if event.type == pygame.MOUSEBUTTONDOWN :
                pos = pygame.mouse.get_pos()

                for ii in range(len(songs)) :

                    song = songs[ii][0]
                    song = pygame.transform.scale(song,(wi/5,he/5))

                    song_rect   = song.get_rect()
                    song_rect.y = my_settings.height/5*ii

                    if song_rect.collidepoint(pos) :
                        loop = False

                        diffs = songs[ii][3]
                        for i in range(len(diffs)) :
                    
                            diff = font.render(diffs[i],False,(255,255,255)).convert()
                            my_settings.screen.blit(diff,(wi/5,he/20*i+he/5*ii))
                        
                        loop2 = True
                        while loop2 :
                            
                            my_settings.clock.tick(my_settings.frequence)
                            pygame.display.flip()
                            
                            key = pygame.key.get_pressed()
                            for event in pygame.event.get() :

                                if event.type == pygame.MOUSEBUTTONDOWN :
                                    pos = pygame.mouse.get_pos()
                                
                                    diffs = songs[ii][3]
                                    for i in range(len(diffs)) :
                                
                                        diff = font.render(diffs[i],False,(255,255,255)).convert()

                                        diff_rect   = diff.get_rect()
                                        diff_rect.x = wi/5
                                        diff_rect.y = he/20*i+he/5*ii

                                        if diff_rect.collidepoint(pos) :
                                            loop2 = False

                                            Run(ii,i,songs,skin)

                                if event.type == pygame.KEYDOWN and event.key == pygame.K_s :
                                    loop2 = False

                                    my_settings.screen.blit(noir,(0,0))

                                    skin  = SkinSelect(font,skin)
                                    songs = SongSelect()

                                    loop = True

                                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE :
                                    loop2 = False
                                    
                                    menu()

                                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and key[pygame.K_LALT]) :
                                    loop2 = False

                                    pygame.quit()
                                    exit()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s :

                my_settings.screen.blit(noir,(0,0))

                skin  = SkinSelect(font,skin)
                songs = SongSelect()

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and key[pygame.K_LALT]) :
                loop = False

                pygame.quit()
                exit()