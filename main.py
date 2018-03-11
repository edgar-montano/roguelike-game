#########################
#   Pythonic RL         #
# based on Jotaf's guide#
#   written by em2532   #
#########################

import libtcodpy as libtcod

############### CONSTANTS####################
#actual size of the window
SCREEN_WIDTH        = 80
SCREEN_HEIGHT       = 50

#size of the map
MAP_WIDTH           = 80
MAP_HEIGHT          = 45

LIMIT_FPS           = 20      #20 frames-per-second maximum
FULLSCREEN          = False  #fullscreen on startup
#String constants
TITLE               = 'PyRL'
# Color constants
color_dark_wall     = libtcod.Color(0,0,100)
color_dark_ground   = libtcod.Color(50,50,100)
##############################################

#######Tile CLASS DEFINITION##################
# TODO: add support for Tiles that inflict damage
class Tile:
    """
    Tile class for map creation
    """
    def __init__(self, blocked, block_sight=None):
        """
        Creates a tile, and uses a blocked flag to determine
        if the tile is passable. By default block_sight is set to
        None meaning field of vision is blocked, and blocked is set to false 
        """
        self.blocked = blocked
        # if tile is blocked so is the sight
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight
    
    def setBlocked(self,blocked_flag=True):
        """
        Set tile tile block, sets the tile as blocked and
        sets the block_sight flag. Default parameter is a boolean set to True,
        meaning by default setBlocked() sets  the values to blocked. 
        """
        self.blocked=blocked_flag
        self.block_sight=blocked_flag

class Rect:
    """
    Helper class used in the process of room creation 
    """
    def __init__(self,x,y,w,h):
        self.x1=x
        self.y1=y
        self.x2=x+w
        self.y2=y+h
        
###############################################

#######OBJECT CLASS DEFINITIONS################
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
        self.x= x
        self.y=y
        self.char=char
        self.color=color

    def move(self, dx, dy):
        """
        Moves the object based on a predefined input:
        negative values denote for a change in opposite direction.
        """
        if not map[self.x + dx][self.y + dy].blocked:
            # print("Location: (%d,%d) is blocked: %s" %
            #       (self.x+dx, self.y+dy, map[self.x + dx][self.y + dy].blocked))
            # print("\t block_sight is: %s " %
            #       map[self.x + dx][self.y + dy].block_sight)
            self.x+=dx
            self.y+=dy 
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

###############FUNCTIONS######################
def make_map():
    """
    Simple map generating algorithm that used a nest list comprehension 
    to generate a multi-dimensional array of Tiles. 
    """
    global map
    # fill map with blocked tiles, then use create room to generate rooms
    # [note: list comprenhsion must call Tile using a parameter in constructor
    # otherwise it will result in referring to the same floor instead of
    # creating a new tile object!]
    map = [[Tile(True)
            for y in range(MAP_HEIGHT)]
           for x in range(MAP_WIDTH)]

    # static walls used for debugging purposes
    # later include procedural generation of rooms
    room1 = Rect(20,15,10,15)
    room2 = Rect(50, 15, 10, 15)
    create_room(room1)
    create_room(room2)

    # connect the rooms 
    create_htunnel(25, 55, 23)

    # place player in room 
    player.x = 25
    player.y = 23

   


# TODO: Add support for directional movement
# and add support for num pad movement along with vi keys
def handle_keys():
    """
    Handless the movement of the player. The function 
    console_wait_for_keypress blocks all actions until the player
    makes a move. 
    """
    #blocks the game and awaits input
    key = libtcod.console_wait_for_keypress(True)
    
    # handle setting keys, in this case handle escape or alt+enter
    # to toggle fullscreen
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    elif key.vk == libtcod.KEY_ESCAPE:
        return True
    
    #handle player movement
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        player.move(0,-1)
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        player.move(0,1)
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        player.move(-1,0)
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        player.move(1,0)
    #print("(%d,%d)" % (player.x,player.y))

def render_all():
    """
    Renders all objects to the displays.   
    """
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH): 
            wall = map[x][y].block_sight
            if wall: 
                libtcod.console_set_char_background(con,x,y,color_dark_wall,libtcod.BKGND_SET)
            else:
                libtcod.console_set_char_background(con,x,y,color_dark_ground,libtcod.BKGND_SET)
    #draw all objects on screen
    for object in objects:
        object.draw()
    
    # blit render onto screen
    libtcod.console_blit(con,0,0,SCREEN_WIDTH,SCREEN_HEIGHT,0,0,0)


def create_room(room):
    """
    Create a room, takes in a room argument
    """
    global map
    for x in range(room.x1+1, room.x2):
        for y in range(room.y1+1, room.y2):
            map[x][y].setBlocked(False)
            # map[x][y].blocked = False
            # map[x][y].block_sight = False

def create_htunnel(x1,x2,y):
    """
    Create a horizontal tunnel 
    """
    global map
    # if x1 < x2, x1 will be the minimum of both, and x2 the maximum
    for x in range(min(x1,x2), max(x1,x2)+1):
        map[x][y].setBlocked(False)

def create_vtunnel(y1,y2,x):
    """
    Create a vertical tunnel
    """
    global map
    for x in range(min(y1,y2), max(y1,y2)+1):
        map[x][y].setBlocked(False)
    

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
npc = Object(SCREEN_WIDTH/2-5, SCREEN_HEIGHT/2, 'd', libtcod.yellow)
objects = [npc, player]

#generates map 
make_map()
##############################################

# Main game loop
while not libtcod.console_is_window_closed():
    
    # This iterates through each object and 
    # draws them onto the screen, instead of manually 
    # calling console_put_char
    render_all()
    
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
