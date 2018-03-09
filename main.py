#########################
#   Pythonic RL         #
# based on Jotaf's guide#
#   written by em2532   #
#########################

import libtcodpy as libtcod

############### CONSTANTS####################
#actual size of the window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

#size of the map
MAP_WIDTH = 80
MAP_HEIGHT = 45

LIMIT_FPS = 20      #20 frames-per-second maximum
FULLSCREEN = False  #fullscreen on startup
#String constants
TITLE = 'PyRL'
##############################################


###############INITIALIZATION################
# set custom greyscale font
libtcod.console_set_custom_font('arial10x10.png',libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

#now initialization the console window, setting
libtcod.console_init_root(SCREEN_WIDTH,SCREEN_HEIGHT,TITLE,FULLSCREEN)

playerx = SCREEN_WIDTH/2
playery = SCREEN_HEIGHT/2
##############################################

###############FUNCTIONS######################
def handle_keys():
    global playerx, playery
    #blocks the game and awaits input
    key = libtcod.console_wait_for_keypress(True)
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    elif key.vk == libtcod.KEY_ESCAPE:
        return True
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        playery -= 1
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        playery += 1
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        playerx -= 1
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        playerx += 1
##############################################


# Main game loop
while not libtcod.console_is_window_closed():
    
    #set foreground of player to white
    libtcod.console_set_default_foreground(0,libtcod.white)

    #place character at coordinates (1,1)
    libtcod.console_put_char(0,playerx,playery,'@',libtcod.BKGND_NONE)

    #flushes changes to screen
    libtcod.console_flush()

    # place an empty space in players previous place in order to avoid 
    # printing a trail of characters on screen
    libtcod.console_put_char(0, playerx, playery,' ', libtcod.BKGND_NONE)

    #determine whether exit has been called, otherwise move character
    #the reason we call handle keys last is because it initiates the start of the next turn
    exit = handle_keys()
    if exit:
        break
