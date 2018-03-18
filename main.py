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

# constants used for dungeon creation 
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

# Constants used for Field of View
FOV_ALGO = 0 # default FOV Algorithm
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 5

# Miscallaneous constants
LIMIT_FPS           = 20      #20 frames-per-second maximum
FULLSCREEN          = False  #fullscreen on startup
#String constants
TITLE               = 'PyRL'
# Color constants
color_dark_wall     = libtcod.Color(0,0,0)
color_light_wall   = libtcod.Color(130,110,50)
color_dark_ground   = libtcod.Color(50,50,150)
color_light_ground  = libtcod.Color(200,180,50)
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
    def center(self):
        """
        Finds the center of the rectangle
        """
        centerX = (self.x1 + self.x2)/2
        centerY = (self.y1 + self.y2)/2
        return (centerX,centerY)
    def intersect(self,other):
        """
        Determines if another room intersects with this one. 
        """
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)
        
        
        
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
        if libtcod.map_is_in_fov(fov_map,self.x,self.y):
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

   
    # list of all the rooms we will eventually create
    rooms = []
    # counter used to create rooms until we hit max amount of rooms. 
    num_rooms = 0

  
    # Here we are going to create x number of rooms, depending on MAX_ROOM
    # size field. 
    for r in range(MAX_ROOMS):
        # Generate coordinates for the room
        w = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        x = libtcod.random_get_int(0, 0, MAP_WIDTH - w - 1)
        y = libtcod.random_get_int(0, 0, MAP_HEIGHT - h - 1)

        
        
        #generate new room with our randomized dimensions
        new_room = Rect(x,y,w,h)
        
        # we'll use this flag to check if this room intersects with another 
        invalid_room = False
        
        # check if this room intersects with another room
        # if so this room is not valid 
        for other_room in rooms:      
            #this will break out the current loop that checks all the other rooms
            # and then continue to try to generate a new room. 
            if new_room.intersect(other_room):
                invalid_room = True
                break 
            
            #if the room is valid generate it 
        if not invalid_room:
            # generate new room
            create_room(new_room)
            
            #store the center of the room 
            (new_x,new_y)=new_room.center()

            # Debug message so we can see coordinates of room centers
            #print("Room created at %d,%d" % (new_x,new_y))
            
            # if this is the first room generated, set the player inside this room. 
            if num_rooms == 0:
                player.x=new_x
                player.y=new_y
            else:
                # since the room generated is NOT the first room, we must connect 
                # our newly generated room to another room. 
                # first we retrieve the coordinates of the center of the previous room
                (prev_x, prev_y) = rooms[num_rooms-1].center()

                # This random number gets a either 0 or 1, this is similar to flipping a coin
                # if the coin is heads we create the horizontal tunnel first then vertical
                if libtcod.random_get_int(0,0,1) == 1:
                    create_htunnel(prev_x, new_x, prev_y)
                    create_vtunnel(prev_y, new_y, new_x)
                else:
                    # the coin flip is tails so we create a vertical tunnel first
                    create_vtunnel(prev_y, new_y, prev_x)
                    create_htunnel(prev_x, new_x, new_y)
        
            # at this point we can append new room to list and 
            # increment room number counter 
            rooms.append(new_room)
            num_rooms+=1
                

   
# TODO: Add support for directional movement
# and add support for num pad movement along with vi keys
def handle_keys():
    """
    Handless the movement of the player. The function 
    console_wait_for_keypress blocks all actions until the player
    makes a move. 
    """

    global fov_recompute
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
        fov_recompute = True
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        player.move(0,1)
        fov_recompute = True
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        player.move(-1,0)
        fov_recompute = True
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        player.move(1,0)
        fov_recompute = True
    #print("(%d,%d)" % (player.x,player.y))

def render_all():
    """
    Renders all objects to the displays.   
    """
    global fov_recompute, fov_map

    if fov_recompute:
        # recmpute fov when needed 
        libtcod.map_compute_fov(fov_map, player.x, player.y,TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
        fov_recompute = False 

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH): 
            visible = libtcod.map_is_in_fov(fov_map,x,y)
            wall = map[x][y].block_sight
            if not visible:  
                if wall: 
                    libtcod.console_set_char_background(con,x,y,color_dark_wall,libtcod.BKGND_SET)
                else:
                    libtcod.console_set_char_background(con,x,y,color_dark_ground,libtcod.BKGND_SET)
            # this is the case where the wall is visible
            else:
                if wall:
                    libtcod.console_set_char_background(
                        con, x, y, color_light_wall, libtcod.BKGND_SET)
                else:
                    # the case where its a ground tile
                    libtcod.console_set_char_background(
                        con, x, y, color_light_ground, libtcod.BKGND_SET)
                    
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
    for y in range(min(y1,y2), max(y1,y2)+1):
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

# generate field of view effect
fov_map  = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
        libtcod.map_set_properties(fov_map, x,y, not map[x][y].block_sight, not map[x][y].blocked)

fov_recompute = True

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
