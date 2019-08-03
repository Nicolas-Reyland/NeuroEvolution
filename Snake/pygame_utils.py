#################### Plat_Cube ####################

import pygame as pg

pg.init()

# fonts
smallfont = pg.font.SysFont (None, 25)   # 25 = font size
medfont = pg.font.SysFont (None, 50) 
largefont = pg.font.SysFont (None, 80)
giantfont = pg.font.SysFont (None, 160)

def text_objects (text, color, size):
    if size == 'small':
        textSurface = smallfont.render (text, True, color)
    elif size == 'medium':
        textSurface = medfont.render (text, True, color)
    elif size == 'large':
        textSurface = largefont.render (text, True, color)
    elif size == 'giant':
        textSurface = giantfont.render (text, True, color)

    return textSurface, textSurface.get_rect ()

def text_to_button (msg, color, buttonx, buttony, buttonwidth, buttonheight, size = 'small'):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (buttonx+(buttonwidth/2), buttony+(buttonheight/2))
    screen.blit (textSurf, textRect)

def message_to_screen (msg,color, y_displace=0, size = 'small'):
    textSurface, textRect = text_objects(msg, color, size)
    textRect.center = (disp_w / 2), (disp_h / 2)+y_displace
    screen.blit (textSurface, textRect)





























