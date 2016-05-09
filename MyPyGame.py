import pygame
import time
import random
import sys

pygame.init()

pause = True

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
green = (0,220,0)
bright_green = (0,255,0)
red = (220,0,0)
bright_red = (255,0,0)
blue = (0,0,255)
 
block_color = (53,115,255)

crash_sound = pygame.mixer.Sound("Crash.wav")


car_width = 73
num = 3
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

carImg = pygame.image.load('racecar.png')


def things(thingx, thingy, thingw, thingh, block_color):
    for i in range(num):
        pygame.draw.rect(gameDisplay, block_color, [thingx[i], thingy[i], thingw, thingh])

def quitgame():
    pygame.quit()
    quit()

def ReadScore():
    f = open('score.txt', 'r')
    f.seek(0)
    score = f.read()
    f.close()
    return int(score)

def ShowHighest():
    font = pygame.font.SysFont(None, 25)
    text = font.render("Highest score - " + str(ReadScore()), True, black)
    gameDisplay.blit(text,(580,0))

def WriteScore(num):
    f = open('score.txt', 'w')
    f.seek(0)
    f.write(str(num))
    f.close()
    

def MaxScore(number):
    font = pygame.font.SysFont('comicsansms', 40)
    text = font.render("Highest score buddy!!!" + str(number), True, black)
    gameDisplay.blit(text,(120,300))
    pygame.display.update()
    time.sleep(2)

    game_loop()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def paused():
    pygame.mixer.music.pause()
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    

    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        #gameDisplay.fill(white)
        

        button("Continue",150,450,100,50,green,bright_green,unpause)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        
        pygame.display.update()
        clock.tick(15)

def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False


def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(text,(0,0))

def car(x,y):
    gameDisplay.blit(carImg,(x,y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
    
    

def crash():

    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)
    
    
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("You Crashed", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    

    while True:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        #gameDisplay.fill(white)
        

        button("Play Again",150,450,100,50,green,bright_green,game_loop)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15) 

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(white)
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects("A bit Racey", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("GO!",150,450,100,50,green,bright_green,game_loop)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)
    
def game_loop():
    global pause
    
    pygame.mixer.music.load('gamemusic.mp3')
    pygame.mixer.music.play(-1)
    
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0

    thing_startx = random.sample(range(0,display_width),num)
    thing_starty = random.sample(range(-1500,-600),num)
    thing_speed = 7
    thing_width = 100
    thing_height = 100

    dodged = 0

    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
                elif event.key == pygame.K_p:
                    pause = True
                    paused()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        gameDisplay.fill(white)

        # things(thingx, thingy, thingw, thingh, color)

        things(thing_startx, thing_starty, thing_width, thing_height,block_color)
        for i in range(num):
            thing_starty[i] += thing_speed
        things_dodged(dodged)
        ShowHighest()
        car(x,y)

        if x > display_width - car_width or x < 0:
            gameDisplay.fill(white)
            crash()

        for i in range(num):
            if thing_starty[i] > display_height:
                    thing_starty[i] = 0 - thing_height
                    thing_startx[i] = random.randrange(0,display_width)
                    dodged += 1
                    if dodged > 15:
                        thing_speed += 1
                    elif dodged > 45:
                        thing_speed += 1.3
                    elif dodged > 60:
                        thing_speed += 1.6
        

        ####

        for i in range(num):
            if y < thing_starty[i]+thing_height:
                if x > thing_startx[i] and x < thing_startx[i] + thing_width or x+car_width > thing_startx[i] and x + car_width < thing_startx[i]+thing_width:
                    if ReadScore() < dodged:
                        WriteScore(dodged)
                        gameDisplay.fill(white)
                        MaxScore(dodged)
                        
                    else:
                        gameDisplay.fill(white)
                        crash()
       
      
        
        
        
        pygame.display.update()
        clock.tick(60)
        
game_intro()
game_loop()
pygame.quit()
file.close()
quit()
