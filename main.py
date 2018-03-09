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

#############CLASS DEFINITIONS################
class Object:
    """
    This is a generic object that can represent the 
    player, an npc, item, stairs, etc.
    """
    def __init__(self,x,y,char,color):
        """
        Constructor that determines location of object
        character represent object, and the color of the object.
        This constructor should always be called on creating a new 
        object.
        """
        self.x = x
        self.y = y
        self.char = char
        self.color = color
    def move(self, dx, dy):
        """
        Moves the object based on a predefined input:
        negative values denote for a change in opposite direction.
        """
        self.x += dx
        self.y += dy 
    def draw(self):
        """
        Sets the color and then draws the character represented by the positional values.
        """
        libtcod.console_set_default_foreground(con,self.color)
        libtcod.console_put_char(con,self.x,self.y,self.char,libtcod.BKGND_NONE)
    def clear(self):
        """
        Erases the character
        """
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)
##############################################


###############INITIALIZATION################
# set custom greyscale font
libtcod.console_set_custom_font(
    'arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

#now initialization the console window, setting
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FULLSCREEN)

# creates a console buffer we can use to store results of drawing functions
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

# Initializes the player object, an npc object, then creates 
# a list of all objects to iterate through
# makes updating all objects easier. 
player = Object(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, '@', libtcod.white)
npc    = Object(SCREEN_WIDTH/2-5, SCREEN_HEIGHT/2, 'd',libtcod.yellow)
objects = [npc,player]
##############################################

###############FUNCTIONS######################
def handle_keys():
    #global playerx, playery
    #blocks the game and awaits input
    key = libtcod.console_wait_for_keypress(True)
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    elif key.vk == libtcod.KEY_ESCAPE:
        return True
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        player.move(0,-1)
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        player.move(0,1)
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        player.move(-1,0)
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        player.move(1,0)
##############################################


# Main game loop
while not libtcod.console_is_window_closed():
    
    # This iterates through each object and 
    # draws them onto the screen, instead of manually 
    # calling console_put_char
    for object in objects:
        object.draw()
    
    # blits the contents of the new console to the root
    libtcod.console_blit(con,0,0, SCREEN_WIDTH,SCREEN_HEIGHT,0,0,0)

    #flushes changes to screen
    libtcod.console_flush()

    # Iterates through all objects, and clears them from the screen
    # this is so that next turn, we dont have trails of previous moves 
    # still on the screen. 
    for object in objects:
        object.clear()

    #determine whether exit has been called, otherwise move character
    #the reason we call handle keys last is because it initiates the start of the next turn
    exit = handle_keys()
    if exit:
        break
