SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
#GUI
SPOT_GREEN = "#272324"
SPOT_BLACK = "#C8C5C0"
SPOT_WHITE = "#FFFFFF"
DIVIDER_HEIGHT = 3

# Menu line item types
LINE_NORMAL = 0
LINE_HIGHLIGHT = 1
LINE_TITLE = 2

try:
    import RPi.GPIO as gpio
    TEST_ENV = False
except:
    TEST_ENV = True
    gpio = None

SCALE = SCREEN_HEIGHT / 1060

LARGEFONT = ("ChicagoFLF", int(72 * SCALE))
MED_FONT =("ChicagoFLF", int(52 * SCALE))

#Clickwheel listening url and port
UDP_IP = "localhost"
UDP_PORT = 9090

MENU_PAGE_SIZE = 6 if SCREEN_HEIGHT < 300 else 7
