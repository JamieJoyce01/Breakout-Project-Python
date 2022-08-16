import pygame
import random
import time

#objects
#
#init
#
#while loop gameloop
#   input - EventLoop
#   update
#   render/draw
#
#cleanup

pygame.init()


#Please take 'pygame.FULLSCREEN' out of line 78 if you wish to use resolution
#Display resolution - Can be changed by not recommended as scaling of the objects is not 100% there
x = 1130
y = 910
xy = [x,y]

blockwidth = ((x-10)/14)-10
blockheight = (y-(y-10)/1.3)/8-10 #A bit spaghetti but just for the scaling for the resolution

class rectangle:
    def __init__(self,x,y,colour):
        self.colour = colour
        self.rect = pygame.Rect(x,y, blockwidth,blockheight)
    def draw(self):
        pygame.draw.rect(game, self.colour, self.rect)
        
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(x/2,y/2,10,10)
        self.velocity = [(random.choice([-4,4])),(random.choice([-4,4]))] #choses random direction to start out of 4 possible angles
    def draw(self):
        pygame.draw.rect(game,(150,150,150),self.rect)
        self.rect.x += self.velocity[0]
        self.rect.y+=self.velocity[1]
    def invert(self):
        self.velocity[1] = -self.velocity[1] #Ball bounces off rect or paddle
    
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect((x/2)-50,y-100, 70,15)
    def draw(self):
        pygame.draw.rect(game, (150,150,255), self.rect)
    def left(self):
        self.rect.x-=10
    def right(self):
        self.rect.x+=10

class Text:
    def __init__(self,string,x,y):
        self.x = x
        self.y = y
        font = pygame.font.Font("freesansbold.ttf",32)
        self.text = font.render(str(string),True,(255,255,255),game)
    def draw(self):
        game.blit(self.text,(self.x,self.y))
        
class LiveText: #Difference between text and live text is that live text needs to be updated (such as lives or score)
    def __init__(self,string,x,y): #Could of possibly made this an inherited function but I didnt have the time.
        self.x = x
        self.y = y
        self.font = pygame.font.Font("freesansbold.ttf",32)
        self.text = self.font.render("____",True,(255,255,255),game) #placeholder font until first loop redraws
    def draw(self,string):
        self.string = string
        self.text = self.font.render(str(self.string),True,(255,255,255),game)
        game.blit(self.text,(self.x,self.y))
        

game = pygame.display.set_mode(xy, pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN)
pygame.display.set_caption("Breakout Game - Jamie Joyce")
backgroundcolour = pygame.Color(0,0,0,0)

blocklist = []
text = []

lives = 5 #variable declartion
score = 0
i = 0
gameend = False

colour = (255,0,0) #Starting red for the first 28 blocks

for row in range(8): #This for loop is for colouring and drawing the blocks with the right spacing.
    for column in range(14):
        if i > 27 and i < 54:
            colour = (255,165,0)
        elif i > 55 and i < 82:
            colour = (0,255,0)
        elif i > 83:
            colour = (245,218,66)
        blocklist.append(rectangle(column*blockwidth+10 * (column + 1),row*blockheight+10 * (row+1),colour)) #Not very clear but it was hard to get an accurate gap on both sides of the screen
        i+=1
        
paddle = Paddle()#initalisation
ball = Ball()

text.append(Text("Lives",10,y/3))
text.append(Text("Score",x-100,y/3))
hearts = LiveText(lives,10,y/3+50)
points = LiveText(score,x-100,y/3+50)

paddleleft,paddleright = False, False
gameloop = True
while gameloop:
    #INPUT
    pygame.time.delay(20) #Just so the ball doesnt whizz off
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #So game closes when the X is pressed
            gameloop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: #Following IF statements are for the movement of the paddle,
                paddleleft = True          #used a Bool so i could hold down the button and it would move.
            elif event.key == pygame.K_RIGHT:
                paddleright = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                paddleleft = False
            elif event.key == pygame.K_RIGHT:
                paddleright = False
    if paddleleft:
        paddle.left()
    elif paddleright:
        paddle.right()
    #UPDATE

    for block in blocklist:
        if block.rect.colliderect(ball) == True:
            blocklist.remove(block) #senses when the ball is in one of the blocks and deletes the block and bounces the ball
            ball.invert()
            if len(blocklist) <= 0: #if all blocks are destroyed you win!
                text.append(Text("You Win!",(x/2)-50,y/2))
                gameend = True
            score += 4 #score goes up by 4 to match the original game
    if paddle.rect.colliderect(ball) == True:
            ball.invert() #if collides with the paddle then bounce              

    #These If statements are the once that makes the ball bounce off the sides
    if ball.rect.x>=x-10:
        ball.velocity[0] = -ball.velocity[0]
    elif ball.rect.x<=0:
        ball.velocity[0] = -ball.velocity[0]
    elif ball.rect.y>y-10:
        if lives == 0:
            text.append(Text("You Lose!",(x/2)-50,y/2))
            gameend = True
        else:
            lives-=1
            del ball #Re-initalising the ball just so it starts in the starting position again
            ball = Ball()
    elif ball.rect.y<0:
        ball.velocity[1] = -ball.velocity[1]
    
    
        

    #RENDER
    game.fill(backgroundcolour)
        
    for block in blocklist: #For loop to draw all blocks every frame
        block.draw()
    for t in text: #Same for all the texts
        t.draw()
        
    hearts.draw(lives)
    points.draw(score)
    
    paddle.draw()
    ball.draw()
    
    pygame.display.flip()
    if gameend == True:
        time.sleep(2) #timer so the user can see when they win or lose before the game closes
        break

pygame.quit()

