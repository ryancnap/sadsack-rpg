import pygame

#eventually I'll figure out how to use this to automatically generate
#the map so I don't have to manually add elements to the tilemap list. 
#this part of the code makes me sad.
MAP_WIDTH = 16 
MAP_HEIGHT = 12
TILE_SIZE = 37
#Margin will be used for black padding at the bottom of the screen; 
#later it will (hopefully) have player stats or other info and serve as a HUD.
margin = 60

#Screen object needs to be declared here so the map will work, 
#must import this module to run the main game file. 
screen = pygame.display.set_mode((MAP_WIDTH*TILE_SIZE, MAP_HEIGHT*TILE_SIZE+margin))

#Define the file paths to be used for the resource images
#MAY NEED TO COMMENT OUT THE SECTION AROUND LINE 
DIRTFILE = "dirt_tile.png"
GRASSFILE = "grass_tile.png"
WATERFILE = "water_tile.png"

#start map function definition here
def display_mymap():

    #define constants representing colors
    #move this out of the display_mymap function later
    GREEN = (0, 255, 0)
    BROWN = (153, 76, 0)
    BLUE = (0, 0, 255)

    #define constants representing the resources
    DIRT = 0
    GRASS = 1
    WATER = 2

    #define a dictionary to link the resources to colors
    colors = {
        DIRT : BROWN,
        #DIRT: pygame.image.load(DIRTFILE).convert(),
        GRASS: GREEN,
        #GRASS: pygame.image.load(GRASSFILE).convert(),
        WATER : BLUE
        #WATER: pygame.image.load(WATERFILE).convert()
            }
        
    #the map, basic colors for now    
    tilemap = [
        [GRASS, GRASS, GRASS, GRASS, WATER, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS],
        [WATER, WATER, GRASS, GRASS, WATER, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS],
        [WATER, WATER, GRASS, GRASS, WATER, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS],
        [WATER, GRASS, GRASS, GRASS, WATER, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS],
        [GRASS, GRASS, DIRT, GRASS, WATER, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS],
        [GRASS, GRASS, DIRT, GRASS, WATER, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS],
        [GRASS, GRASS, DIRT, GRASS, WATER, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS],
        [GRASS, GRASS, DIRT, GRASS, WATER, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS],
        [GRASS, GRASS, DIRT, GRASS, WATER, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS],
        [GRASS, GRASS, DIRT, GRASS, WATER, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS],
        [GRASS, GRASS, DIRT, GRASS, WATER, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS],
        [GRASS, GRASS, DIRT, GRASS, WATER, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS],
        
               ]


    #while True: CANNOT LOOP THIS, I LOSE EVENT HANDLING FOR MOVING PLAYER
    #loop through each row
    for row in range(MAP_HEIGHT):
        #loop through each column in the row
        for column in range(MAP_WIDTH):
            pygame.draw.rect(screen, colors[tilemap[row][column]], (column*TILE_SIZE,row*TILE_SIZE,TILE_SIZE,TILE_SIZE))
    #pygame.display.update()
    #^this was causing issues when I called another pygame.display.update()
    #after calling the mymap function and updating the player's position.
    #I think it was trying to update the tilemap every time the game looped,
    #resulting in my player flashing/blinking in and out.
    #THIS WORKS FOR NOW, AND IT (SHOULD) WORK FOR WHEN I SWITCH TO IMAGES FOR 
    #MY TILEMAP. HOWEVER I DON'T KNOW IF IT WILL GIVE ME PROBLEMS IF/WHEN I
    #SWITCH TO ANIMATED SPRITES FOR EACH IMAGE OF MY TILEMAP, SUCH AS 2 FRAMES
    #OF GRASS OR SOMETHING. THINK SONIC THE HEDGEHOG-LIKE BACKGROUNDS.

