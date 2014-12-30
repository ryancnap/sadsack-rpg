'''testGame_modular_animation.py; 


-Warning, code probably isn't structured very well, needs cleaned up.
-Still lots of hardcoded numbers/file paths, no clue if this will work on 
 any system that's not GNU/Linux. 
-If you want to run it, please remember to mess with the filepaths around
 line 95, I should change them to constants at the top of the file but either
 way I don't know how to write an error catching piece of code to find the 
 correct animation files on someone else's system. 
 
-More disclaimers: I don't really know the difference between blitting, 
 updating, and display flipping, so for all I know this could be taking up way
 more resources than it needs to.
-On animations: all of the ints that deal with speed, animation, framerates, 
 etc. are "trial and errored." Soon I'll figure out the right way to calculate
 how many FPS you need when taking pixel size of file, number of frames per
 animation, size of tiles in a tiled map, and such into consideration.
 
-Alot of this is messy as hell. I really don't like how I'm making maps.
 Anytime you want to change the width/height of the map, you're going to have
 to go into the list and manually edit it. I couldn't find any decent tutorials
 on using Tiled maps in pygame, so oh well. Another future to-do.
-Oh and by the way, watch out changing the screen variable for the display.
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

DEPENDS ON: PYTHON 2.X; PYGAME(V.?); MAPS.PY MODULE

'''
#Imports: glob deals with grabbing files I believe. 
import pygame, sys, glob

#Crashes if I remove import all; I heard this was bad practice so I'll have to 
#figure out what pygame module deals with event/keypress handling as that seems
#to be the problem. 
from pygame import *

#Need maps module; not only for map, but that's where my screen object is
#defined.
from maps import *

pygame.init()

#If you read the docstring at the top of file, you know that there's no 
#rhyme or reason to my framerate.
FPS = 45
clock = pygame.time.Clock()

#This is where I used to define constants for tilemap size and screen.
            
#Define base player class; more to be added later.
class Player:
    def __init__(self):
        self.x = 200
        self.y = 300
        self.ani_speed_init = 8
        self.ani_speed = self.ani_speed_init
        self.ani = glob.glob("bmage/bmage_right*.png")
        self.ani.sort() #make sure frames are in numbered order
        self.ani_pos = 0 #this will be the first frame
        self.ani_max = len(self.ani) - 1 
        #^will find max frames of self_ani array, minus one
        #due to counting from 0
        self.img = pygame.image.load(self.ani[0])
        self.update_x(0)
        self.update_y(0)
        
    def update_x(self, x_pos):
        if x_pos != 0:
            self.ani_speed -= 2
            self.x += x_pos #Increments player's x-pos
            if self.ani_speed == 0:
                self.img = pygame.image.load(self.ani[self.ani_pos])
                self.ani_speed = self.ani_speed_init
                #If reach last frame, reset to first frame
                if self.ani_pos == self.ani_max:
                   self.ani_pos = 0
                else:
                    self.ani_pos += 1
        screen.blit(self.img,(self.x, self.y))
        
#Had to make a separate update function for y-movement, couldn't wrap my mind
#around making one update method that would work for both. Needless to say, 
#this section of code also makes me sad. 
    def update_y(self, y_pos):
            if y_pos != 0:
                self.ani_speed -= 2
                self.y -= y_pos #Decrements player's current y-pos
                if self.ani_speed == 0:
                    self.img = pygame.image.load(self.ani[self.ani_pos])
                    self.ani_speed = self.ani_speed_init
                    
                    #If reach last frame, reset to first frame
                    if self.ani_pos == self.ani_max:
                       self.ani_pos = 0
                    else:
                        self.ani_pos += 1
            screen.blit(self.img,(self.x, self.y))
            

player1 = Player()
x_pos = 0
y_pos = 0

#Enter main game loop.                
while True:

    #I'm pretty sure that the screen.fill is for when game visuals are a little
    #more advanced, might make sure the screen is cleared after/before loop.
    screen.fill((0,0,0))
    clock.tick(FPS)    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        #Handling cardinal direction movement with arrow keys
        
        #If the right arrowkey is pressed, player1's animation changes to 
        #the two-frame animation of him walking right.    
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            player1.ani = glob.glob("bmage/bmage_right*.png")
            
            #As long as key is held down, update pos(position) by two.
            #This sets pos to 2, the actual updating of frames and coordinates
            #is handled by the player classes update methods. 
            x_pos = 2 
            
        elif event.type == KEYUP and event.key == K_RIGHT:
            x_pos = 0
            #Once the pressed key is released, set pos to 0. The way the update
            #method handles pos means that the whole method will never be run,
            #ie. we won't animate or move because now no keys are being pressed.
            
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
    
    #Call mymap, update player's position, and draw everything to screen.
    display_mymap()
    player1.update_x(x_pos)
    player1.update_y(y_pos)
    pygame.display.update()
            
        
    
    
    
    
    
    
    
    
    
    
    
    
