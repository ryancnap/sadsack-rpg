"""testGame_modular_animation.py;


-Warning, code probably isn't structured very well, needs cleaned up.
-Still lots of hardcoded numbers/file paths, no clue if this will work on
 any system that's not GNU/Linux.
-If you want to run it, please remember to mess with the filepaths around
 line 95, I should change them to constants at the top of the file but either
 way I don't know how to write an error catching piece of code to find the
 correct animation files on someone else's system.
-Sprite was made with 8 images,  2 frames for each direction.

-More disclaimers: I don't really know the difference between blitting,
 updating, and display flipping, so for all I know this could be taking up way
 more resources than it needs to.
-On animations: all of the ints that deal with speed, animation, framerates,
 etc. are "trial and errored." Soon I'll figure out the right way to calculate
 how many FPS you need when taking size of file, number of frames per
 animation, size of tiles in a tiled map, and such into consideration.

-Alot of this is messy as hell. I really don't like how I'm making maps.
 Anytime you want to change the width/height of the map, you're going to have
 to go into the list and manually edit it. I couldn't find any decent tutorials
 on using Tiled maps in pygame, so oh well. Another future to-do.
-Watch out changing the screen variable for the display.
 I was trying to make this a little more modular by putting the map function
 into a different file, and for some reason I now have to define screen in
 both the main game file and the maps.py module, due to the fact that my Player
 class doesn't know what to do when I tell him to update because the
 display_mymaps function hasn't been called yet, therefore screen hasn't been
 defined yet; introduce previously mentioned dirty workaround, because if I
 call the maps function anywhere else it displays ontop of my sprite, which
 isn't too exciting.
-I'm very new to python, pygame, and OO concepts. So the OO code below is
 probably some twisted halfbreed but it really helped with animating the
 player so it's there. Code could probably be much more robust to expansion and
 change, but I'm still very much at a beginner level so this game is very much
 at a beginner level. At least my sprite moves around.

COPYRIGHT:  RYAN CAMARATTA, 2014
CONTACT:    RYANCNAP@GMAIL.COM

DEPENDS ON: PYTHON 2.X; PYGAME(V.?); my MAPS.PY MODULE

"""

# Imports
import pygame
import sys, os, glob
from pygame import *

# Crashes if I remove import all; I heard this was bad practice so I'll have to
# figure out what pygame module deals with event/keypress handling as
# that seems to be the problem.

# OLD: Need maps module; not only for map, but that's where my screen object is
# defined.
# NEW: Need tiledtmxloader by ___. 
import tiledtmxloader

# If you read the docstring at the top of file, you know that there's no
# rhyme or reason to my framerate; but this is where I put constants.

# This is where I used to define constants for tilemap size and screen.
# Now it's just a cozy home to set fonts :)



# parse the map. (it is done here to initialize the
# window the same size as the map if it is small enough)
path_to_map = os.path.join(os.pardir, "../../../python-dev/game/tile-images/tmx-tilemaps/hopefully.tmx")
print("usage: python %s your_map.tmx\n\nUsing default map '%s'\n" % \
        (os.path.basename(__file__), path_to_map))

world_map = tiledtmxloader.tmxreader.TileMapParser().parse_decode(path_to_map)

# load the images using pygame
resources = tiledtmxloader.helperspygame.ResourceLoaderPygame()
resources.load(world_map) 

# prepare map rendering
assert world_map.orientation == "orthogonal"

# renderer
renderer = tiledtmxloader.helperspygame.RendererPygame()

# init pygame and set up a screen
pygame.init()

screen_width = min(1024, world_map.pixel_width)
screen_height = min(768, world_map.pixel_height)
screen = pygame.display.set_mode((screen_width, screen_height))
BLACK = ((255, 255, 255))
pygame.display.set_caption("What a neat game")
font = pygame.font.SysFont('Calibri', 25, True, False)

frames_per_sec = 45.0
clock = pygame.time.Clock()


# cam_offset is for scrolling
cam_world_pos_x = 0
cam_world_pos_y = 0

# set initial cam position and size
renderer.set_camera_position_and_size(cam_world_pos_x, cam_world_pos_y, \
                                    screen_width, screen_height, "topleft")

# retrieve the layers
sprite_layers = tiledtmxloader.helperspygame.get_layers_from_map(resources)

# Define base player class; more to be added later.


class Player:
    def __init__(self):
        self.x = 200
        self.y = 300
        self.ani_speed_init = 8
        self.ani_speed = self.ani_speed_init
        self.ani = glob.glob("bmage/bmage_right*.png")
        self.ani.sort()  # make sure frames are in numbered order
        self.ani_pos = 0  # this will be the first frame
        self.ani_max = len(self.ani) - 1
        # ^will find max frames of self_ani array, minus one
        # due to counting from 0
        self.img = pygame.image.load(self.ani[0])
        self.update_x(0)
        self.update_y(0)
        # Let's try to make an inventory.
        self.inventory = {}
        # test collision with edges of map.
        self.blocked = False


    def update_x(self, x_pos):                
        if x_pos != 0:  # ie, if we're not standing still
            self.ani_speed -= 2
            self.x += x_pos  # Increments player's x-pos
            # TODO: this seems really hacky...
            # making a class method rely on a global variable sounds like it's bad
            # but should the Player class need to know anything about the camera?
            # maybe incorporate camera details into the Player class and he can
            # act as the view?
            global cam_world_pos_x
            cam_world_pos_x = cam_world_pos_x + 1
            if self.ani_speed == 0:
                self.img = pygame.image.load(self.ani[self.ani_pos])
                self.ani_speed = self.ani_speed_init
                # If reach last frame, reset to first frame
                if self.ani_pos == self.ani_max:
                    self.ani_pos = 0
                else:
                    self.ani_pos += 1
        screen.blit(self.img, (self.x, self.y))

    # Had to make a separate update function for y-movement,
    # couldn't wrap my mind around making one update method that would work for
    # both. Needless to say, this section of code also makes me sad.
    def update_y(self, y_pos):
        if y_pos != 0:
            self.ani_speed -= 2
            self.y -= y_pos  # Decrements player's current y-pos
            if self.ani_speed == 0:
                self.img = pygame.image.load(self.ani[self.ani_pos])
                self.ani_speed = self.ani_speed_init

                # If reach last frame, reset to first frame
                if self.ani_pos == self.ani_max:
                    self.ani_pos = 0
                else:
                    self.ani_pos += 1
        screen.blit(self.img, (self.x, self.y))

    # let's try to do something with inventory!
    # This turned out a lot uglier than expected, must be doing something wrong
    def populate_inv(self, item, description):
        self.inventory[item] = description
        # TODO: remove the magic numbers below when I have proper screen size
        # TODO: Make it blit under the previous entry so things aren't
        # getting\drawn on top of each other.
        for e in self.inventory:
            inv_text = font.render(item + ": " + description, True, BLACK)
            #screen.blit(inv_text, [MAP_WIDTH * TILE_SIZE - 400,
             #                      MAP_HEIGHT * TILE_SIZE + 20])

# ***** End base class Player

player1 = Player()
x_pos = 0
y_pos = 0


# Enter main game loop.
while True:

    # test collision with edges of screen
    #if player1.x_pos == world_map.pixel_width:
    #    player1.blocked = True
    #else:
    #    player1.blocked = False

    # Make sure the screen is cleared before/after every loop.
    screen.fill((0, 0, 0))
    clock.tick(frames_per_sec)

    # render the map
    for sprite_layer in sprite_layers:
        if sprite_layer.is_object_group:
            # we dont draw the object group layers
            # you should filter them out if not needed
            continue
        else:
            renderer.render_layer(screen, sprite_layer)

    #pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # Handling cardinal direction movement with arrow keys

        # If the right arrowkey is pressed, player1's animation changes to
        # the two-frame animation of him walking right.
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            player1.ani = glob.glob("bmage/bmage_right*.png")

            # As long as key is held down, update pos(position) by two.
            # This sets pos to 2, the actual updating of frames and coordinates
            # is handled by the player classes update methods.
            # test collision
            #if player1.blocked == False:
            x_pos = 2
            #else:
            #    player1.x_pos = 0

        elif event.type == KEYUP and event.key == K_RIGHT:
            x_pos = 0
            # Once the pressed key is released, set pos to 0. The way the
            # update method handles pos means that the whole method will
            # never be run, ie. we won't animate or move because now
            # no keys are being pressed.

        elif event.type == KEYDOWN and event.key == K_LEFT:
            player1.ani = glob.glob("bmage/bmage_left*.png")
            x_pos = -2

        elif event.type == KEYUP and event.key == K_LEFT:
            x_pos = 0

        elif event.type == KEYDOWN and event.key == K_UP:
            player1.ani = glob.glob("bmage/bmage_up*.png")
            y_pos = 2

        elif event.type == KEYUP and event.key == K_UP:
            y_pos = 0

        elif event.type == KEYDOWN and event.key == K_DOWN:
            player1.ani = glob.glob("bmage/bmage_down*.png")
            y_pos = -2

        elif event.type == KEYUP and event.key == K_DOWN:
            y_pos = 0

    # Call mymap, update player's position, and draw everything to screen.
    #display_mymap()

    player1.update_x(x_pos)
    player1.update_y(y_pos)
    player1.populate_inv('Sword', 'A rusty thing')
    pygame.display.update()
    # Line 227-ish, only updating cam_world_pos_x for every right button press.
    renderer.set_camera_position_and_size(cam_world_pos_x, cam_world_pos_y, \
                                    screen_width, screen_height, "topleft")