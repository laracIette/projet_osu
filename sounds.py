import pygame

class Sounds :

    def importSounds( menu ) -> None : # cree un dictionnaire des sons

        menu.sounds = {
                "click" : pygame.mixer.Sound( f"assets\\skins\\{menu.skin}\\click.ogg" ),
                 "fail" : pygame.mixer.Sound( f"assets\\skins\\{menu.skin}\\fail.ogg" ),
                  "hit" : pygame.mixer.Sound( f"assets\\skins\\{menu.skin}\\hit.ogg" ),
                 "miss" : pygame.mixer.Sound( f"assets\\skins\\{menu.skin}\\miss.ogg" ),
          "spinnerspin" : pygame.mixer.Sound( f"assets\\skins\\{menu.skin}\\spinnerspin.ogg" ),
         "spinnerbonus" : pygame.mixer.Sound( f"assets\\skins\\{menu.skin}\\spinnerbonus.ogg" )
        }

    def playSound( self, name: str, volume: int, type: int ) -> None : # joue un son

        self.sounds[name].set_volume( volume*self.volume/100*type/100 )
        self.sounds[name].play()