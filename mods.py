import pygame

class MenuMods :

    def getMods( menu: classmethod ) -> None : # definir les modes de jeu

        menu.mods = ["easy",    "nofail",      "halftime",
                    "hardrock", "suddendeath", "doubletime", "hidden",   "flashlight",
                    "relax",    "autopilot",   "spunout",    "autoplay", "scorev2"]

        w = 0
        h = 0
        menu.mods_icons = []
        for i in range( len( menu.mods ) ) :

            center_rect = ( menu.reSize( 505 + 220*w ), menu.reSize( 305 + 220*h ) )
            mod_icon    = menu.load( f"skins\\{menu.skin}\\mods\\{menu.mods[i]}.png", (menu.reSize( 180 ), menu.reSize( 180 )), False )
            mod_rect    = mod_icon.get_rect( center = center_rect )

            w += 1

            if i == 2 or i == 7 :
                h += 1
                w  = 0

            menu.mods_icons.append( [mod_icon, mod_rect, center_rect, False, 0] )

    def modChoice( menu: classmethod ) -> list : # choisir un mode de jeu

        loop = True
        while loop :

            menu.clock.tick( menu.frequence )
            menu.updateShowMods()

            menu.pos = pygame.mouse.get_pos()
            for menu.event in pygame.event.get() :

                if menu.event.type == pygame.MOUSEBUTTONDOWN and menu.event.button == pygame.BUTTON_LEFT :

                    menu.modSelect()

                if menu.event.type == pygame.KEYDOWN and (menu.event.key == pygame.K_F1 or menu.event.key == pygame.K_ESCAPE) :

                    loop = False

                    return menu.mod_list

                menu.gameQuit()

            pygame.display.flip()

    def modSelect( menu: classmethod ) -> None :

        for i in range( len( menu.mods_icons ) ) :

            mod_rect = menu.mods_icons[i][1]

            if mod_rect.collidepoint( menu.pos ) :

                if menu.mods_icons[i][3] == False :
                    menu.mods_icons[i][3] = True

                    if i == 0 :
                        if menu.mods_icons[3][3]  : menu.mods_icons[3][3]  = False
                    elif i == 1 :
                        if menu.mods_icons[4][3]  : menu.mods_icons[4][3]  = False
                        if menu.mods_icons[8][3]  : menu.mods_icons[8][3]  = False
                        if menu.mods_icons[9][3]  : menu.mods_icons[9][3]  = False
                    elif i == 2 :
                        if menu.mods_icons[5][3]  : menu.mods_icons[5][3]  = False
                    elif i == 3 :
                        if menu.mods_icons[0][3]  : menu.mods_icons[0][3]  = False
                    elif i == 4 :
                        if menu.mods_icons[1][3]  : menu.mods_icons[1][3]  = False
                        if menu.mods_icons[8][3]  : menu.mods_icons[8][3]  = False
                        if menu.mods_icons[9][3]  : menu.mods_icons[9][3]  = False
                        if menu.mods_icons[11][3] : menu.mods_icons[11][3] = False
                    elif i == 5 :
                        if menu.mods_icons[2][3]  : menu.mods_icons[2][3]  = False
                    elif i == 8 :
                        if menu.mods_icons[1][3]  : menu.mods_icons[1][3]  = False
                        if menu.mods_icons[4][3]  : menu.mods_icons[4][3]  = False
                        if menu.mods_icons[9][3]  : menu.mods_icons[9][3]  = False
                        if menu.mods_icons[11][3] : menu.mods_icons[11][3] = False
                    elif i == 9 :
                        if menu.mods_icons[1][3]  : menu.mods_icons[1][3]  = False
                        if menu.mods_icons[4][3]  : menu.mods_icons[4][3]  = False
                        if menu.mods_icons[8][3]  : menu.mods_icons[8][3]  = False
                        if menu.mods_icons[10][3] : menu.mods_icons[10][3] = False
                        if menu.mods_icons[11][3] : menu.mods_icons[11][3] = False
                    elif i == 10 :
                        if menu.mods_icons[9][3]  : menu.mods_icons[9][3]  = False
                        if menu.mods_icons[11][3] : menu.mods_icons[11][3] = False
                    elif i == 11 :
                        if menu.mods_icons[4][3]  : menu.mods_icons[4][3]  = False
                        if menu.mods_icons[8][3]  : menu.mods_icons[8][3]  = False
                        if menu.mods_icons[9][3]  : menu.mods_icons[9][3]  = False
                        if menu.mods_icons[10][3] : menu.mods_icons[10][3] = False

                else :
                    menu.mods_icons[i][3] = False

    def updateShowMods( menu: classmethod ) -> None :

        for i in range( len( menu.mods_icons ) ) :

            if menu.mods_icons[i][3] == False :
                if menu.mods_icons[i][4] > 0 :
                    menu.mods_icons[i][4] -= 1

            elif menu.mods_icons[i][4] < 15 :
                menu.mods_icons[i][4] += 1

            mod_icon = pygame.transform.rotate( menu.mods_icons[i][0], - menu.mods_icons[i][4] ).convert()
            mod_rect = mod_icon.get_rect( center = menu.mods_icons[i][2] )

            menu.screen.blit( mod_icon, mod_rect )

    def setModList( menu: classmethod ) -> None :

        menu.mod_list = []

        for i in range( len( menu.mods_icons ) ) :

            if menu.mods_icons[i][3] :

                menu.mod_list.append( menu.mods[i] )