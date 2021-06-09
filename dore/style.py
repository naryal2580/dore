from stoyled import *
from shutil import get_terminal_size as _get_terminal_size
from random import randint as _randint
from time import sleep
from threading import Thread as _Thread
from threading import Event

TERM_WIDTH = _get_terminal_size()[0]
ANIMATE = False


def banner(version, color=True):
    """
    A fancy banner, how can we forget this ;)

        Parameters:
            version: Version to be displayed in the banner
            color (bool): This just makes the banner look bold
    """
    logo = r'''
     ___  |/|
    (   ) |/|
  .-.| |  |_|  ___ .-. .--.   
 /   \ | (___)(   )   \    \  
|  .-. | (___) | ' .-. ;.-. ; 
| |  | | // \\ |  / (___) | | 
| |  | |// _ \\| |    | |/  | 
| |  | || | | || |    | ' _.' 
| '  | || |_| || |    | .'.-. 
' `-'  /\\_._//| |    ' `-' / 
 `.__,'  \_|_/(___)    `.__.'  --v{version} by naryal2580
'''[1:-1]
    if not version:
        version = ''
    logo = logo.replace('{version}', str(version))
    if color:
        print(bold + logo + rst)
    else:
        print(logo)


def clear_line():
    """
    This function simply clears a line
    
    NOTE: Make sure the line you want to clear has not sent you to a new line..
    """
    line_width = _get_terminal_size()[0]
    print('\r' + ' '*line_width + '\r', end='', flush=True)


def random_animation(text, refresh_time=0.07):
    """
    Animation which randomly lowers/uppers case of a character

        Parameters:
            text (str): String to be animated
            refresh_time (int/float): Refresh time for the animation, just simply sleeps haha
    """
    if not text:
        return
    txt = list(text)
    random_itr = _randint(0, len(text) - 1)
    random_chr = text[random_itr]
    if random_chr.islower():
        txt[random_itr] = text[random_itr].upper()
    else:
        txt[random_itr] = text[random_itr].lower()
    sleep(refresh_time)
    print(f"\r{''.join(txt)}", end='', flush=True)


def bar_animation(progress, size=100, text='', division=2):
    """
    Simple bar animation
    
        Parameters:
            progress (int): Progress (eg.: In 5/7 `5` is progress here)
            size (int): Progress length (eg.: In 5/7 `7` is progress length here)
            text (str): Text to be displayed on the animation, during the animation
            division (int): Size of bar to be divided with width of the terminal
    """
    global TERM_WIDTH
    if TERM_WIDTH != _get_terminal_size()[0]:
        TERM_WIDTH = _get_terminal_size()[0]
        clear_line()
    if text:
        text = ' ' + str(text)
    total_width = int( ( _get_terminal_size()[0] - 2 ) / division)
    _progress = int( total_width * (progress / size) )
    if text:
        if len(text) > _progress:
            text1 = text[:_progress]
            text2 = text[_progress:]
            if len(text2) > total_width - _progress:
                text2 = text2[:total_width - _progress - 3] + '...'
            if _progress == total_width:
                text = text[:total_width - 3] + '...'
                print(f'\r|{invert}{text}{rst}|', end='', flush=True)
            elif total_width in (_progress + 1, _progress + 2):
                text = text[:total_width - 3] + '...'
                print(f'\r|{invert}{text}{rst}|', end='', flush=True)
            elif _progress < total_width:
                print(f'\r|{invert}{text1}{" "*(_progress - len(text1))}{rst}{text2}{" "*(total_width - _progress - len(text2))}|', end='', flush=True)
            # else:
            #     print('F')
        else:
            print(f'\r|{invert}{text}{" "*(_progress - len(text))}{rst}{" "*(total_width - _progress)}|', end='', flush=True)
    else:
        print(f'\r|{invert}{" "*_progress}{rst}{" "*(total_width - _progress)}|', end='', flush=True)


class Animate(_Thread):
    """
    A threading.Thread Sub-Class for animations
    """
    def __init__(self, animation_style='random', text='', size=100, *args, **kwargs):
        super(Animate, self).__init__(*args, **kwargs)
        self.size = size
        self.text = text
        self.style = animation_style
        self._stop = Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        from .core import JUICE
        global ANIMATE
        ANIMATE = True
        if self.style == 'random':
            print(self.text, end='', flush=True)
            while ANIMATE:
                if self.stopped():
                    clear_line()
                    return
                random_animation(self.text)
        elif self.style == 'bar':
            while ANIMATE:
                if self.stopped():
                    clear_line()
                    return
                bar_animation(len(JUICE), self.size, f'{self.text} {len(JUICE)}/{self.size}')
            clear_line()
