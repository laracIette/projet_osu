def SetMap(osu) : # determination et classage dans des tableau des elements a afficher pendant une partie

    cs_t,ar_t,od_t,hp_t = [],[],[],[]

    spinner_lock           = False
    spinners0,osu.spinners = [],[]
    circles0,osu.circles   = [],[]

    a   = 0
    map = osu.songs[osu.map][2][osu.diff]
        

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

                    osu.cs = ''.join(cs_t)
                    osu.cs = float(osu.cs)

                elif a == 2 :
                    for o in i :
                        if o != '\n' :
                            ar_t.append(o)

                    osu.ar = ''.join(ar_t)
                    osu.ar = float(osu.ar)

                    SetAR(osu)

                elif a == 3 :
                    for o in i :
                        if o != '\n' :
                            od_t.append(o)

                    osu.od = ''.join(od_t)
                    osu.od = float(osu.od)

                    SetOD(osu)
                
                elif a == 4 :
                    for o in i :
                        if o != '\n' :
                            hp_t.append(o)

                    osu.hp = ''.join(hp_t)
                    osu.hp = float(osu.hp)

                else :
                    circles0.append(i)

            else :
                osu.spinners.append(i)

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
                osu.circles.append(tab)
                tab = []

    circles0 = []
    for m in osu.circles :
        circles0.append(int(m))
    
    num = 0
    osu.circles = []

    osu.start_offset = 2500-circles0[2]

    for i in range(int(len(circles0)/cycle)) :
        circles0[i*cycle+2] += osu.start_offset

        for j in range(cycle) :

            tab.append(circles0[num])
            num += 1

        osu.circles.append(tab)
        tab = []
    
    for j in osu.spinners :

        for k in j :

            if k != ',' and k != 's' and k != '\n' :
                tab.append(k)

            elif tab != [] :
                tab = ''.join(tab)
                spinners0.append(tab)
                tab = []
    
    for r in range(len(spinners0)) :
        spinners0[r]  = int(spinners0[r])
        spinners0[r] += osu.start_offset

    osu.spinners = []
    h = 0
    for r in range(int(len(spinners0)/2)) :

        osu.spinners.append([spinners0[h],spinners0[h+1]])
        
        h += 2

    c = 0
    u = 0
    hit_objects = []
    for i in range(len(osu.circles) + len(osu.spinners)) :

        if osu.spinners == [] or u == len(osu.spinners) :
            hit_objects.append([osu.circles[c][2],0])
            c += 1
            continue

        if osu.circles == [] or c == len(osu.circles) :
            hit_objects.append([osu.spinners[u][0],1])
            hit_objects.append([osu.spinners[u][1],1])
            u += 1
            continue

        if osu.circles[c][2] < osu.spinners[u][0] :
            hit_objects.append([osu.circles[c][2],0])
            
            if c < len(osu.circles) : c += 1

        else :
            hit_objects.append([osu.spinners[u][0],1])
            hit_objects.append([osu.spinners[u][1],1])
            
            if u < len(osu.spinners) : u += 1
    
    osu.game_breaks = []
    for p in range(len(hit_objects)-1) :
        
        if (hit_objects[p+1][0] - hit_objects[p][0] >= 5000 and hit_objects[p][1] != 1) or\
           (hit_objects[p+1][0] - hit_objects[p][0] >= 5000 and hit_objects[p+1][1] != 1) :
           
            osu.game_breaks.append([hit_objects[p][0],hit_objects[p+1][0]])

def SetAR(osu) : # reglages correspondants au temps d'approche des objets d'une partie

    ars = {
        0  : [1800,120],
        1  : [1680,120],
        2  : [1560,120],
        3  : [1440,120],
        4  : [1320,120],
        5  : [1200,150],
        6  : [1050,150],
        7  : [900,150],
        8  : [750,150],
        9  : [600,150],
        10 : [450,150],
        11 : [300,150],
    }

    osu.ar_int  = ars[round(osu.ar)][0]
    osu.ar_rest = round(osu.ar,1)-round(osu.ar)
    osu.ar_time = ars[round(osu.ar)][0] - ars[round(osu.ar)][1]*osu.ar_rest
    osu.ar_time = round(osu.ar_time)

def SetOD(osu) : # reglages correspondants a la difficulte des objets d'une partie

    osu.od_time = 79.5 - osu.od*6

def SetHP(osu) : # reglages correspondants au gain et perte de points de vie

    pass

def SetMultiplier(osu) : # multiplier pris en compte lors du calcul du score
    
    cs_od_hp = osu.cs + osu.od + osu.hp

    if cs_od_hp < 6 :
        osu.difficulty_multiplier = 2
    
    elif cs_od_hp >= 6 and cs_od_hp < 13 :
        osu.difficulty_multiplier = 3

    elif cs_od_hp >= 13 and cs_od_hp < 18 :
        osu.difficulty_multiplier = 4
    
    elif cs_od_hp >= 18 and cs_od_hp < 25 :
        osu.difficulty_multiplier = 5

    elif cs_od_hp >= 25 :
        osu.difficulty_multiplier = 6