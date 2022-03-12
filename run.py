import math
import pygame
from settings import Settings
from math import inf
from tools import load,SkinSelect,SongSelect,Score,get_time,import_sounds,play,rs

my_settings = Settings()
wi = my_settings.width
he = my_settings.height

white  = (255,255,255)
grey   = (48,48,48)
black  = (0,0,0)
orange = (218,174,70)
green  = (87,227,19)
blue   = (50,188,231)

class Run :

    def __init__(self,ii,diff,songs,skin,sounds,volume) :

        circles0,circles = [],[]
        show_circles     = []

        cs_t,ar_t,od_t,hp_t = [],[],[],[]

        a   = 0
        map = songs[ii][2][diff]
        with open(map,'r') as map_file :

            for i in map_file :

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
        
        with open('assets\\settings.txt','r') as settings_file :

            a = 0

            lines = settings_file.readlines()
            for i in lines :
                
                if a == 0 :

                    offset = int(i)

                a += 1

        if offset != 0 :
            show_offset = True
        else :
            show_offset = False

        offset_time = get_time()

        del circles0,tab,cs_t,ar_t,od_t,hp_t,num,cycle,a

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

        show_acc = []
        acc_miss = load(f'skins\\{skin}\\miss.png',(c_s/2,c_s/2))
        acc_100  = load(f'skins\\{skin}\\100.png',(c_s/2,c_s/2))
        acc_50   = load(f'skins\\{skin}\\50.png',(c_s/2,c_s/2))

        fade  = False
        faded = False

        start_time  = get_time()
        paused_time = 0
        pause_time  = 0
        end_time    = inf

        cs_od_hp = cs + od + hp

        if cs_od_hp < 6 :
            difficulty_multiplier = 2
        
        elif cs_od_hp >= 6 and cs_od_hp < 13 :
            difficulty_multiplier = 3

        elif cs_od_hp >= 13 and cs_od_hp < 18 :
            difficulty_multiplier = 4
        
        elif cs_od_hp >= 18 and cs_od_hp < 25 :
            difficulty_multiplier = 5

        elif cs_od_hp >= 25 :
            difficulty_multiplier = 6

        mod_multiplier = 1
        hit_value      = 0
        score          = 0
        combo          = 0
        combo_font     = pygame.font.SysFont('segoeuisemibold',round(rs(90)))

        max_health     = 600
        health         = max_health
        health_minus   = 50*hp/6
        passive_health = health_minus/500
        health_bar_bg  = pygame.Rect(rs(20),rs(20),rs(600),rs(20))

        ur_50     = pygame.Rect(rs(821),rs(1050),rs(278),rs(8))
        ur_100    = pygame.Rect(rs(875),rs(1050),rs(172),rs(8))
        ur_300    = pygame.Rect(rs(928),rs(1050),rs(66),rs(8))
        ur_middle = pygame.Rect(rs(959),rs(1039),rs(4),rs(30))
        show_ur   = []

        score_txt = combo_font.render('0',False,white).convert()
        combo_txt = combo_font.render('0',False,white).convert()
        acc_txt   = acc_font.render('100.00%',False,white).convert()

        music_start = get_time() + start_offset
        playing     = False
        waiting     = False

        pygame.mixer.music.load(songs[ii][1])
        pygame.mixer.music.set_volume(volume)

        e  = 0
        UI = True

        running = True
        while running :

            my_settings.clock.tick(my_settings.frequence)

            if waiting == False :

                if get_time() - paused_time >= music_start and playing == False :
                
                    pygame.mixer.music.play()
                    playing = True
                
                if e < len(circles) :

                    if get_time() - paused_time  >=  start_time + circles[e][2] - ar_time :

                        create_time = get_time() - paused_time
                        coor        = [round(circles[e][0]/512*wi*3/4*0.86+rs(360),2),round(circles[e][1]/384*he*0.86+rs(75),2)]

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

                if get_time() >= end_time + start_offset or health <= 0 :
                    running = False

                    pygame.mixer.music.pause()

                    with open('assets\\settings.txt','w') as settings_file :
                        
                        modifs = [offset,volume]

                        for a in range(len(lines)) :

                            settings_file.write(lines[a].replace(lines[a],str(modifs[a])))

                    if health <= 0 :
                        play(sounds,'fail',1,volume)
                        menu()

                    Score(accuracy)
                    
                    pygame.mixer.music.unpause()
                    menu()
                
            if game_break == False :
                pygame.draw.rect(my_settings.screen,black,noir)
            else :
                my_settings.screen.blit(bg,(0,0))
                #my_settings.screen.blit(dim,(0,0))

            for u in show_circles :

                if waiting == False :
                
                    u[1] = get_time() - u[0] - paused_time

                    if u[1] >= ar_time and u[8] == False :
                        u[8] = True

                    if u[2] < 4 :

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

                my_settings.screen.blit(u[3],(u[4][0]-u[3].get_width()/2,u[4][1]-u[3].get_width()/2))
                my_settings.screen.blit(u[7],(u[4][0]-c_s/2,u[4][1]-c_s/2))
                my_settings.screen.blit(u[6],(u[4][0]-u[6].get_width()/2+rs(2),u[4][1]-u[6].get_height()/2+rs(7)))
            
                if u[1] >= ar_time + od_time :
                    show_circles.pop(0)
                    
                    if u[11] == False :

                        acc.append(0)
                        show_acc.append([acc_miss,u[4],get_time(),0])

                        acc_check = True

                        health -= health_minus

                        if combo >= 20 :
                            play(sounds,'miss',1,volume)
                        combo = 0
            
            if acc_check :

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
            
            if waiting == False :

                pos = pygame.mouse.get_pos()

                trail_count += round(5000/fps)
                if trail_count > 100 :

                    trail_pos.append([pos,cursor_trail,255])
                    trail_count = 0
                
                if len(trail_pos) > 8 :
                    trail_pos.pop(0)
                
                health    -= passive_health*160/fps
                health_bar = pygame.Rect(rs(20),rs(20),rs(600*health/600),rs(20))

            if len(show_ur) > 20 :
                show_ur.pop(0)

            for s in range(len(show_acc)) :

                showed_time = get_time() - show_acc[s][2]

                if showed_time < 300 :

                    show_acc[s][3] += 255/300*1000/fps

                if showed_time >= 300 :

                    show_acc[s][1][1] += 0.5*160/fps
        
                if showed_time > 400 :

                    show_acc[s][3] -= 255/100*1000/fps

                show_acc[s][0].set_alpha(show_acc[s][3])
                show_acc[s][0].convert_alpha()

                if showed_time > 500 :

                    show_acc.pop(s)
                    break

            if show_offset :
                
                if offset < 0 :
                    offset_txt = fps_font.render(f'Local offset : {offset}ms',False,white).convert()
                else :
                    offset_txt = fps_font.render(f'Local offset : +{offset}ms',False,white).convert()

                if get_time() - offset_time - paused_time >= 1000 :
                    show_offset = False
            
            if UI :

                my_settings.screen.blit(combo_txt,(rs(20),rs(960)))
                my_settings.screen.blit(score_txt,(rs(1910)-score_txt.get_width(),rs(-20)))
                my_settings.screen.blit(acc_txt,(rs(1910)-acc_txt.get_width(),rs(80)))
                my_settings.screen.blit(fps_txt,(rs(1910)-fps_txt.get_width(),rs(1075)-fps_txt.get_height()))

                pygame.draw.rect(my_settings.screen,grey,health_bar_bg)
                pygame.draw.rect(my_settings.screen,white,health_bar)
                
            pygame.draw.rect(my_settings.screen,orange,ur_50)
            pygame.draw.rect(my_settings.screen,green,ur_100)
            pygame.draw.rect(my_settings.screen,blue,ur_300)
            pygame.draw.rect(my_settings.screen,white,ur_middle)

            for u in show_ur :
                
                ur_hit = pygame.Rect(961-rs(u[1]),rs(1039),rs(2),rs(30))
                pygame.draw.rect(my_settings.screen,u[0],ur_hit)

            for s in show_acc :
                my_settings.screen.blit(s[0],(s[1][0]-c_s/4,s[1][1]-c_s/2))
            
            if show_offset :
                my_settings.screen.blit(offset_txt,(wi/2-offset_txt.get_width()/2,rs(10)))

            for t in trail_pos :

                if waiting == False :

                    t[2] -= 7*160/fps
                t[1].set_alpha(t[2])

                my_settings.screen.blit(t[1],(t[0][0]-t_s/2,t[0][1]-t_s/2))

            my_settings.screen.blit(cursor,(pos[0]-c_s/2,pos[1]-c_s/2))

            if waiting :

                my_settings.screen.blit(cursor,(pos1[0]-c_s/2,pos1[1]-c_s/2))

            pygame.display.flip()
            
            key = pygame.key.get_pressed()
            for event in pygame.event.get() :

                if waiting == False :

                    if (event.type == pygame.KEYDOWN and event.key == pygame.K_x) or (event.type == pygame.KEYDOWN and event.key == pygame.K_v) :

                        for v in range(len(show_circles)) :

                            if acc_check == False and show_circles[v][11] == False :

                                distance = math.hypot(show_circles[v][4][0]-pos[0],show_circles[v][4][1]-pos[1])

                                if distance < c_s/2*115/121 :

                                    acc_check = True

                                    difference = abs(get_time() - (start_time + show_circles[v][5] + paused_time) + offset)

                                    if difference < od_time :

                                        if difference < od_time/4 :
                                            hit_value = 300
                                            show_ur.append([blue,278*difference/od_time/2])

                                        if difference > od_time/4 and difference < od_time/2 :
                                            hit_value = 100
                                            show_ur.append([green,278*difference/od_time/2])
                                            show_acc.append([acc_100,show_circles[v][4],get_time(),0])
                                        
                                        if difference > od_time/2 :
                                            hit_value = 50
                                            show_ur.append([orange,278*difference/od_time/2])
                                            show_acc.append([acc_50,show_circles[v][4],get_time(),0])

                                        acc.append(round(hit_value/3,2))
                                        health_bonus = round(hit_value/30,2)

                                        if health + health_bonus < max_health :
                                            health += health_bonus
                                        else :
                                            health = max_health

                                        play(sounds,'hit',0.5,volume)
                                        combo += 1

                                    else :

                                        acc.append(0)
                                        show_acc.append([acc_miss,show_circles[v][4],get_time(),0])

                                        health -= health_minus

                                        if combo >= 20 :
                                            play(sounds,'miss',1,volume)
                                        combo = 0

                                    show_circles[v][8]  = True
                                    show_circles[v][11] = True

                else :

                    pos1 = pygame.mouse.get_pos()

                    if (event.type == pygame.KEYDOWN and event.key == pygame.K_x) or (event.type == pygame.KEYDOWN and event.key == pygame.K_v) :
                        
                        distance1 = math.hypot(pos1[0]-pos[0],pos1[1]-pos[1])

                        if distance1 < 5 :

                            waiting = False

                            pygame.mixer.music.unpause()
                                                        
                            paused_time += get_time() - pause_time
                        
                if  (event.type == pygame.KEYDOWN and event.key == pygame.K_TAB and key[pygame.K_LSHIFT]) or\
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT and key[pygame.K_TAB]) :
                    if UI :
                        UI = False
                    else :
                        UI = True

                if event.type == pygame.KEYDOWN and event.key == pygame.K_EQUALS :
                    offset     += 5
                    offset_time = get_time()
                    show_offset = True

                if event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS :
                    offset     -= 5
                    offset_time = get_time()
                    show_offset = True

                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and key[pygame.K_LALT]) :
                    running = False

                    with open('assets\\settings.txt','w') as settings_file :

                        modifs = [offset,volume]

                        for a in range(len(lines)) :

                            settings_file.write(lines[a].replace(lines[a],f'{modifs[a]}\n'))

                    pygame.quit()
                    exit()

                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) :
                    running = False
                    
                    if waiting :
                        paused_time += get_time() - pause_time

                    pause_time = get_time()

                    pygame.mouse.set_visible(True)
                    pygame.mixer.music.pause()

                    my_settings.screen.blit(pause_screen,(0,0))
                    pygame.display.flip()
                    
                    with open('assets\\settings.txt','w') as settings_file :

                        modifs = [offset,volume]

                        for a in range(len(lines)) :

                            settings_file.write(lines[a].replace(lines[a],f'{modifs[a]}\n'))

                    loop = True
                    while loop :

                        for event in pygame.event.get() :

                            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE :
                                loop    = False
                                running = True
                                waiting = True

                                pygame.mouse.set_visible(False)

                                fps_time += get_time() - pause_time

                            if event.type == pygame.KEYDOWN and event.key == pygame.K_q :
                                loop  = False

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

    with open('assets\\settings.txt','r') as settings_file :

            a = 0

            lines = settings_file.readlines()
            for i in lines :
                
                if a == 1 :

                    volume = int(i)

                a += 1

    show_volume = False
    volume_font = pygame.font.SysFont('arial',round(rs(30)))
    volume_txt  = volume_font.render(f'{volume}%',False,white).convert()
    volume_noir = pygame.Rect(wi-volume_txt.get_width(),he-volume_txt.get_height(),volume_txt.get_width(),volume_txt.get_height())
    volume_time = get_time()

    loop = True
    while loop :

        my_settings.clock.tick(my_settings.frequence)

        if show_volume :
            
            pygame.draw.rect(my_settings.screen,black,volume_noir)

            if get_time() >= volume_time + 1000 :
                show_volume = False
                continue

            my_settings.screen.blit(volume_txt,(wi-volume_txt.get_width(),he-volume_txt.get_height()))

        pygame.display.flip()

        key = pygame.key.get_pressed()
        for event in pygame.event.get() :

            if event.type == pygame.MOUSEBUTTONDOWN :

                if event.button == pygame.BUTTON_LEFT :

                    pos = pygame.mouse.get_pos()

                    for ii in range(len(songs)) :

                        song = songs[ii][0]
                        song = pygame.transform.scale(song,(wi/5,he/5)).convert()

                        song_rect   = song.get_rect()
                        song_rect.y = my_settings.height/5*ii

                        if song_rect.collidepoint(pos) :
                            loop = False

                            play(sounds,'click',1,volume)

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
                                    
                                        for i in range(len(diffs)) :
                                    
                                            diff = font.render(diffs[i],False,white).convert()

                                            diff_rect   = diff.get_rect()
                                            diff_rect.x = wi/5
                                            diff_rect.y = he/20*i+he/5*ii

                                            if diff_rect.collidepoint(pos) :
                                                loop2 = False

                                                play(sounds,'click',1,volume)

                                                pygame.mouse.set_visible(False)
                                                Run(ii,i,songs,skin,sounds,volume)

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

                if event.button == 4 or event.button == 5 :
                    
                    if event.button == 4 :

                        if volume < 100:

                            volume     += 1
                
                    if event.button == 5 :

                        if volume > 0 :

                            volume     -= 1

                    show_volume = True
                    volume_txt  = volume_font.render(f'{volume}%',False,white).convert()
                    volume_time = get_time()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_s :

                pygame.draw.rect(my_settings.screen,black,noir)

                skin   = SkinSelect(font,skin,sounds)
                songs  = SongSelect()
                sounds = import_sounds(skin)
                
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and key[pygame.K_LALT]) :
                loop = False

                pygame.quit()
                exit()