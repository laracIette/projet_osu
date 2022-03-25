def SetMap(self) : # determination et classage dans des tableau des elements a afficher pendant une partie

    circles0,self.circles = [],[]

    cs_t,ar_t,od_t,hp_t = [],[],[],[]

    spinner_lock       = False
    spinners0,self.spinners = [],[]

    a   = 0
    map = self.songs[self.map][2][self.diff]
        

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

                    self.ar = ''.join(ar_t)
                    self.ar = float(self.ar)

                    SetAR(self)

                elif a == 3 :
                    for o in i :
                        if o != '\n' :
                            od_t.append(o)

                    self.od = ''.join(od_t)
                    self.od = float(self.od)

                    SetOD(self)
                
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
    
    num = 0
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
    h = 0
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

def SetAR(self) : # reglages correspondants au temps d'approche des objets d'une partie

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

    self.ar_int  = ars[round(self.ar)][0]
    self.ar_rest = round(self.ar,1)-round(self.ar)
    self.ar_time = ars[round(self.ar)][0] - ars[round(self.ar)][1]*self.ar_rest
    self.ar_time = round(self.ar_time)

def SetOD(self) : # reglages correspondants a la difficulte des objets d'une partie

    self.od_time = 79.5 - self.od*6

def SetHP(self) : # reglages correspondants au gain et perte de points de vie

    pass

def SetMultiplier(self) : # multiplier pris en compte lors du calcul du score
    
    if self.cs_od_hp < 6 :
        self.difficulty_multiplier = 2
    
    elif self.cs_od_hp >= 6 and self.cs_od_hp < 13 :
        self.difficulty_multiplier = 3

    elif self.cs_od_hp >= 13 and self.cs_od_hp < 18 :
        self.difficulty_multiplier = 4
    
    elif self.cs_od_hp >= 18 and self.cs_od_hp < 25 :
        self.difficulty_multiplier = 5

    elif self.cs_od_hp >= 25 :
        self.difficulty_multiplier = 6