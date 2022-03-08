import pygame
from settings import Settings
from math import inf
from tools import load,SkinSelect,SongSelect,Score,get_time,import_sounds,play,rs

my_settings = Settings()
wi = my_settings.width
he = my_settings.height
white = (255,255,255)
grey  = (48,48,48)
black = (0,0,0)

class Run :

    def __init__(self,ii,diff,songs,skin,sounds) :

        circles0,circles = [],[]
        show_circles     = []

        cs_t,ar_t,od_t,hp_t = [],[],[],[]

        a   = 0
        map = songs[ii][2][diff]
        with open(map,'r') as file :

            for i in file :

                a += 1

                if i == '\n' :
                    continue

                elif a == 1 :
                    for o in i :
                        if o != '\n' :
                            cs_t.append(o)

                    cs = ''.join(cs_t)
                    cs = float(cs)

                elif a == 2 :
                    for o in i :
                        if o != '\n' :
                            ar_t.append(o)

                    ar = ''.join(ar_t)
                    ar = float(ar)
                    ar_time = 450*10/ar

                elif a == 3 :
                    for o in i :
                        if o != '\n' :
                            od_t.append(o)

                    od = ''.join(od_t)
                    od = float(od)
                    od_time = 100*10/od
                
                elif a == 4 :
                    for o in i :
                        if o != '\n' :
                            hp_t.append(o)

                    hp = ''.join(hp_t)
                    hp = float(hp)

                else :
                    circles0.append(i)            

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
                        circles.append(tab)
                        tab = []

        circles0 = []
        for m in circles :
            circles0.append(int(m))
        
        num     = 0
        circles = []

        start_offset = 2500-circles0[2]

        for i in range(int(len(circles0)/cycle)) :
            circles0[i*cycle+2] += start_offset

            for j in range(cycle) :

                tab.append(circles0[num])
                num += 1

            circles.append(tab)
            tab = []
        
        pause_screen = load('images\\pause_screen.png',(wi,he))
        #dim         = load('images\\noir93.png',(wi,he))
        bg           = pygame.transform.scale(songs[ii][0],(wi,he)).convert()
        noir         = pygame.Rect(0,0,wi,he)
        
        game_break = True
        break_lock = False
        
        c_s     = rs(121/cs*4.9)
        circle  = load(f'skins\\{skin}\\hitcircle.png',(c_s,c_s))

        a_c_s    = c_s*4
        a_circle = load(f'skins\\{skin}\\approachcircle.png',(a_c_s,a_c_s))

        cursor       = load(f'skins\\{skin}\\cursor.png',(c_s,c_s))
        t_s          = c_s/4
        cursor_trail = load(f'skins\\{skin}\\cursortrail.png',(t_s,t_s))
        trail_pos    = []
        trail_count  = 0

        fpss     = []
        avg_fps  = 0
        fps_time = get_time()
        fps_font = pygame.font.SysFont('arial',round(rs(30)))

        number_font = pygame.font.Font('assets\\fonts\\LeagueSpartanBold.ttf',round(c_s/2))
        
        acc       = []
        acc_check = False
        acc_font  = pygame.font.SysFont('segoeuisemibold',round(rs(45)))

        fade  = False
        faded = False

        start_time  = get_time()
        paused_time = 0
        pause_time  = 0
        end_time    = inf

        cs_od_hp = cs + od + hp

        if cs_od_hp < 6 :
            difficulty_multiplier = 2
        
        elif cs_od_hp >= 6 and cs_od_hp < 13:
            difficulty_multiplier = 3

        elif cs_od_hp >= 13 and cs_od_hp < 18:
            difficulty_multiplier = 4
        
        elif cs_od_hp >= 18 and cs_od_hp < 25:
            difficulty_multiplier = 5

        elif cs_od_hp >= 25 :
            difficulty_multiplier = 6

        mod_multiplier = 1
        hit_value      = 0
        score          = 0
        combo          = 0
        combo_font     = pygame.font.SysFont('segoeuisemibold',round(rs(90)))

        offset = 0

        max_health     = 600
        health         = max_health
        health_minus   = 50*hp/6
        passive_health = health_minus/500
        health_bar_bg  = pygame.Rect(rs(20),rs(20),rs(600),rs(20))

        score_txt = combo_font.render('0',False,white).convert()
        combo_txt = combo_font.render('0',False,white).convert()
        acc_txt   = acc_font.render('100.00%',False,white).convert()

        music_start = get_time() + start_offset
        playing     = False

        UI    = True
        shift = False

        pygame.mixer.music.load(songs[ii][1])
        pygame.mixer.music.set_volume(1)

        e = 0

        running = True
        while running :

            if get_time() >= music_start and playing == False:
            
                pygame.mixer.music.play()
                playing = True
            
            my_settings.clock.tick(my_settings.frequence)

            if e < len(circles) :

                if get_time() - paused_time  >=  start_time + circles[e][2] - ar_time :

                    create_time = get_time()
                    coor        = [circles[e][0]/512*wi*3/4*0.86+rs(360),circles[e][1]/384*he*0.86+rs(75)]

                    if circles[e][3] == 1 :
                        numbers = 1
                    else :
                        numbers += 1

                    number = number_font.render(f'{numbers}',False,white).convert()

                    show_circles.append([create_time,0,1,a_circle,coor,circles[e][2],number,circle,fade,1,acc_check,faded])

                    e += 1

            elif e == len(circles) :

                end_time = get_time()

                e += 1

            if get_time() >= music_start - start_offset/2.5 and break_lock == False :
                game_break = False
                break_lock = True

            if get_time() >= end_time + start_offset/2.5 :
                game_break = True

            if get_time() >= end_time + start_offset or health <= 0:
                running = False

                pygame.mixer.music.pause()

                if health <= 0 :
                    play(sounds,'fail',1)
                    menu()

                Score(accuracy)
                
                pygame.mixer.music.unpause()
                menu()
            
            if game_break == False :
                pygame.draw.rect(my_settings.screen,black,noir)
            else :
                my_settings.screen.blit(bg,(0,0))
                #my_settings.screen.blit(dim,(0,0))
            
            if len(show_circles) > 0 :

                for u in show_circles :
                    
                    u[1] = get_time() - u[0]

                    if u[1] >= ar_time and u[8] == False :
                        u[8] = True

                    if u[2] < 4 :

                        a_c_width   = u[3].get_width()
                        a_c_rescale = a_c_s*1/u[2]
                        u[3]        = pygame.transform.scale(a_circle,(a_c_rescale,a_c_rescale))
                    
                    if u[8] == False :

                        u[3].set_alpha(255*u[2]/2-255/2)
                        u[7].set_alpha(255*u[2]-255)
                        u[6].set_alpha(255*u[2]-255)

                        u[2] += 6/fps
                        u[2]  = round(u[2],2)
                    
                    else :

                        u[3].set_alpha(255*u[9])
                        u[7].set_alpha(255*u[9])
                        u[6].set_alpha(255*u[9])

                        u[9] -= 6/fps
                        u[9]  = round(u[9],2)

                    my_settings.screen.blit(u[3],(u[4][0]-a_c_width/2,u[4][1]-a_c_width/2))
                    my_settings.screen.blit(u[7],(u[4][0]-c_s/2,u[4][1]-c_s/2))
                    my_settings.screen.blit(u[6],(u[4][0]-u[6].get_width()/2+rs(2),u[4][1]-u[6].get_height()/2+rs(7)))
                
                    if u[1] >= ar_time + od_time :
                        show_circles.pop(0)
                        
                        if u[11] == False :
                            acc.append(0)
                            acc_check = True

                            health -= health_minus

                            if combo >= 20 :
                                play(sounds,'miss',1)
                            combo = 0
            
            if acc_check == True :

                accuracy = 0

                if len(acc) != 0 :

                    for w in acc :
                        accuracy += w

                    accuracy /= len(acc)

                if combo > 2 :
                    combo_multiplier = combo - 2
                else :
                    combo_multiplier = 0

                score += round(hit_value + (hit_value * ((combo_multiplier * difficulty_multiplier * mod_multiplier) / 25)))
                
                acc_txt    = acc_font.render(f'{round(accuracy,2)}%',False,white).convert()
                combo_txt  = combo_font.render(f'{combo}x',False,white).convert()
                score_txt  = combo_font.render(str(score),False,white).convert()

                acc_check = False
            
            fps = round(1000 / (get_time() - fps_time),2)

            fpss.append(fps)
            if len(fpss) > 40 :
                fpss.pop(0)

            for i in fpss :
                avg_fps += i

            fps_time = get_time()
            avg_fps /= len(fpss)
            fps_txt  = fps_font.render(f'{round(avg_fps)}fps',False,white).convert()
            avg_fps  = 0
            
            pos = pygame.mouse.get_pos()

            trail_count += round(5000/fps)
            if trail_count > 100 :

                trail_pos.append([pos,cursor_trail,255])
                trail_count = 0
            
            if len(trail_pos) > 8 :
                trail_pos.pop(0)
            
            health    -= passive_health*160/fps
            health_bar = pygame.Rect(rs(20),rs(20),rs(600*health/600),rs(20))
            
            if UI == True :

                pygame.draw.rect(my_settings.screen,grey,health_bar_bg)
                pygame.draw.rect(my_settings.screen,white,health_bar)

                my_settings.screen.blit(combo_txt,(rs(20),rs(960)))
                my_settings.screen.blit(score_txt,(rs(1910)-score_txt.get_width(),rs(-20)))
                my_settings.screen.blit(acc_txt,(rs(1910)-acc_txt.get_width(),rs(80)))
                my_settings.screen.blit(fps_txt,(rs(1910)-fps_txt.get_width(),rs(1075)-fps_txt.get_height()))

            for t in trail_pos :

                t[2] -= 7*160/fps
                t[1].set_alpha(t[2])

                my_settings.screen.blit(t[1],(t[0][0]-t_s/2,t[0][1]-t_s/2))

            my_settings.screen.blit(cursor,(pos[0]-c_s/2,pos[1]-c_s/2))

            pygame.display.flip()

            key = pygame.key.get_pressed()
            for event in pygame.event.get() :

                if (event.type == pygame.KEYDOWN and event.key == pygame.K_x) or (event.type == pygame.KEYDOWN and event.key == pygame.K_v) :

                    if len(show_circles) > 0 :

                        for v in range(len(show_circles)) :

                            if acc_check == False and show_circles[v][11] == False :

                                circle_rect = circle.get_rect()
                                circle_rect.center = show_circles[v][4]

                                if circle_rect.collidepoint(pos) :

                                    acc_check = True

                                    difference = abs(get_time() - (start_time + show_circles[v][5] + paused_time) + offset)

                                    if difference < od_time :

                                        if difference < od_time/4 :
                                            hit_value = 300

                                        if difference > od_time/4 and difference < od_time/2 :
                                            hit_value = 100
                                        
                                        if difference > od_time/2 :
                                            hit_value = 50

                                        acc.append(round(hit_value/3,2))
                                        health_bonus = round(hit_value/30,2)

                                        if health + health_bonus < max_health :
                                            health += health_bonus
                                        else :
                                            health = max_health

                                        play(sounds,'hit',0.5)
                                        combo += 1

                                    else :
                                        acc.append(0)

                                        health -= health_minus

                                        if combo >= 20 :
                                            play(sounds,'miss',1)
                                        combo = 0

                                    show_circles[v][8] = True
                                    show_circles[v][11] = True

                if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT :
                    shift = True
                if event.type == pygame.KEYUP and event.key == pygame.K_LSHIFT :
                    shift = False

                if shift == True :
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB :
                        if UI == True :
                            UI = False
                        else :
                            UI = True

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

                                pygame.mouse.set_visible(False)
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

    noir = pygame.Rect(0,0,wi,he)
    font = pygame.font.Font('assets\\fonts\\shippori.ttf',round(rs(45)))

    pygame.draw.rect(my_settings.screen,black,noir)
    
    skin   = 'whitecat'
    songs  = SongSelect()
    sounds = import_sounds(skin)

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
                    song = pygame.transform.scale(song,(wi/5,he/5)).convert()

                    song_rect   = song.get_rect()
                    song_rect.y = my_settings.height/5*ii

                    if song_rect.collidepoint(pos) :
                        loop = False

                        play(sounds,'click',1)

                        diffs = songs[ii][3]
                        for i in range(len(diffs)) :
                    
                            diff = font.render(diffs[i],False,white).convert()
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
                                
                                        diff = font.render(diffs[i],False,white).convert()

                                        diff_rect   = diff.get_rect()
                                        diff_rect.x = wi/5
                                        diff_rect.y = he/20*i+he/5*ii

                                        if diff_rect.collidepoint(pos) :
                                            loop2 = False

                                            play(sounds,'click',1)

                                            pygame.mouse.set_visible(False)
                                            Run(ii,i,songs,skin,sounds)

                                if event.type == pygame.KEYDOWN and event.key == pygame.K_s :
                                    loop2 = False

                                    pygame.draw.rect(my_settings.screen,black,noir)

                                    skin   = SkinSelect(font,skin,sounds)
                                    songs  = SongSelect()
                                    sounds = import_sounds(skin)

                                    loop = True

                                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE :
                                    loop2 = False
                                    
                                    menu()

                                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and key[pygame.K_LALT]) :
                                    loop2 = False

                                    pygame.quit()
                                    exit()
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s :

                pygame.draw.rect(my_settings.screen,black,noir)

                skin   = SkinSelect(font,skin,sounds)
                songs  = SongSelect()
                sounds = import_sounds(skin)

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and key[pygame.K_LALT]) :
                loop = False

                pygame.quit()
                exit()