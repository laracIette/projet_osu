import pygame

def ImportSounds(skin) :
    sounds = {
               'click' : pygame.mixer.Sound(f'assets\\skins\\{skin}\\click.ogg'),
                'fail' : pygame.mixer.Sound(f'assets\\skins\\{skin}\\fail.ogg'),
                 'hit' : pygame.mixer.Sound(f'assets\\skins\\{skin}\\hit.ogg'),
                'miss' : pygame.mixer.Sound(f'assets\\skins\\{skin}\\miss.ogg'),
         'spinnerspin' : pygame.mixer.Sound(f'assets\\skins\\{skin}\\spinnerspin.ogg'),
        'spinnerbonus' : pygame.mixer.Sound(f'assets\\skins\\{skin}\\spinnerbonus.ogg')
    }
    return sounds

def Play(sounds,name,volume,percentage,type) :
    sounds[name].set_volume(volume*percentage/100*type/100)
    sounds[name].play()