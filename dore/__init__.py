r"""
`    ___  |/|
    (   ) |/|
  .-.| |  |_|  ___ .-. .--.
 /   \ | (___)(   )   \    \
|  .-. | (___) | ' .-. ;.-. ;
| |  | | // \\ |  / (___) | |
| |  | |// _ \\| |    | |/  |
| |  | || | | || |    | ' _.'
| '  | || |_| || |    | .'.-.
' `-'  /\\_._//| |    ' `-' /
 `.__,'  \_|_/(___)    `.__.'

Direct Object Reference Exploitation (DORE)
"""


__version__ = 0.001
__author__ = 'naryal2580'


from .style import *
from .core import *
from .extra import *

# To ignore linting errors
from dore import extra, core, style


del Event, extra, core, style, bad, blink, blue, blue_l, bold, cyan, cyan_l, dim, good, green, green_l, hidden, invert, italic, normal, purple, purple_l, red, red_l, rst, strike, uline, white, white_l, yellow, yellow_l, TextIOBase, BufferedIOBase, RawIOBase, IOBase


banner(__version__)

print(warn('''
DISCLAIMER -> I do not support or encourage any illegal stuff,
and is not responsible for what you end up doing with dore.
'''[1:-1]))

_is_tor_active = is_active('tor.service')
if _is_tor_active != None:  # It didn't throw `False`
    if not _is_tor_active:
        print(warn('TOR is not started on this device'))
else:
    print(info('INFO -> Make sure, your proxies are reachable first'))