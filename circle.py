from tools import Tools
tools = Tools()

class Circle :

    def __init__( self, time: int, coor: list, start_time: int, number: int, fade: bool, faded: bool, c_s: int, a_c_s: int, skin: str ) -> None:

        self.time       = time
        self.time_shown = 0
        self.alpha      = 1
        self.a_circle   = tools.load( f"skins\\{skin}\\approachcircle.png", (a_c_s, a_c_s), True )
        self.coor       = coor
        self.start_time = start_time
        self.number     = number
        self.circle     = tools.load( f"skins\\{skin}\\hitcircle.png", (c_s, c_s), True )
        self.fade       = fade
        self.a_alpha    = 1
        self.faded      = faded
        self.scale      = 1