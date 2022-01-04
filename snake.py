import pygame
import random
import argparse
import json
pygame.init()

SCREEN_WIDTH=1000
SCREEN_HEIGHT=1000
SNAKE_LENGTH=3
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

font = pygame.font.SysFont('Arial', 25)
obstacles = pygame.sprite.Group()
pointgroup = pygame.sprite.Group()
scorelist = pygame.sprite.Group()
allspriteslist = pygame.sprite.Group()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the width and height of each snake segment and point
segment_width = 18
segment_height = 18
# Margin between each segment
segment_margin = 2
# Set initial speed
x_change = segment_width + segment_margin
y_change = 0
game_matrix_rows=0
game_matrix_cols=0
obstacle_matrix=[],[]
snake_segments=[]
list_of_scores=[]

class Segment(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface([segment_width, segment_height])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Point(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface([segment_width, segment_height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def parse_command():
    global SCREEN_WIDTH,SCREEN_HEIGHT,game_matrix_rows,game_matrix_cols,obstacle_matrix
    # Instantiate the parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, required=True)
    args = parser.parse_args()
    with open(args.name) as f:
        d = json.load(f)
        SCREEN_WIDTH =20* int(d['rows'])
        SCREEN_HEIGHT =20* int(d['cols'])
    game_matrix_rows = int(d['rows'])
    game_matrix_cols = int(d['cols'])
    obstacle_matrix = d['game_state']

#when the game loops we need to reset the x_change and the y_change values
def initialise_for_loop():
    global x_change,y_change
    x_change = segment_width + segment_margin
    y_change = 0

def initialise_snake():
    global allspriteslist,snake_segments
    snake_segments = []
    for i in range(SNAKE_LENGTH):
        x = 20
        y = 20
        segment = Segment(x, y)
        snake_segments.append(segment)
        allspriteslist.add(segment)

def game_over():
        screen.fill(BLACK)

        #highscore display on game over screen
        y_score=50+100
        list_of_scores.append(len(snake_segments)+1)
        screen.blit(font.render('High scores', True, (255,255,255)), (SCREEN_WIDTH/2-60, y_score))
        y_score+=25
        list_of_scores.sort(reverse=True)

        #the number of displayed scores is dependent on the screen resolution
        score_display_max=SCREEN_HEIGHT/2
        score_count=0
        for score in list_of_scores:
            score_count+=25
            if(score_count>score_display_max): break
            screen.blit(font.render(str(score), True, (255,255,255)), (SCREEN_WIDTH/2, y_score))
            pygame.display.flip()
            y_score+=25

        #removing the "dead" snake
        for i in range(len(snake_segments)):
            old_segment = snake_segments.pop()
            allspriteslist.remove(old_segment)

        #game over and contiune buttons
        color1 = (255, 255, 255)
        color2 = (255, 255, 255)
        x_change = 0
        y_change = 0
        unclicked=True
        rect1 = pygame.Rect(SCREEN_WIDTH/2-100, 50, 0, 0).inflate(100, 50)
        rect2 = pygame.Rect(SCREEN_WIDTH/2+100, 50, 0, 0).inflate(100, 50)
        while unclicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    unclicked = True
                point = pygame.mouse.get_pos()
                collide1 = rect1.collidepoint(point)
                collide2 = rect2.collidepoint(point)
                if collide1:
                    color1 = (0, 255, 0)
                    if event.type == pygame.MOUSEBUTTONUP:
                        unclicked = False

                        #max number of recursions is 1000
                        game_loop()
                        
                elif collide2:
                    color2 = (255, 0, 0)
                    if event.type == pygame.MOUSEBUTTONUP:
                        #save list of scores in external file
                        file = open("savefile.txt","r+")
                        file.truncate(0)
                        file.close()
                        string_ints = [str(int) for int in list_of_scores]
                        str_of_ints = ' '.join(string_ints)
                        f = open("savefile.txt", "a")
                        f.write(str_of_ints)
                        f.close()
                        unclicked = False
                        done = True
                        exit()
                else:
                    color1 = (255, 255, 255)
                    color2 = (255, 255, 255)
                pygame.draw.rect(screen, color1, rect1)
                pygame.draw.rect(screen, color2, rect2)
                screen.blit(font.render('Reset', True, (0,0,0)), (SCREEN_WIDTH/2-133, 35))
                screen.blit(font.render('Quit', True, (0,0,0)), (SCREEN_WIDTH/2+80, 35))
                pygame.display.flip()

def snake_movement(event):
    global x_change,y_change
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            x_change = (segment_width + segment_margin) * -1
            y_change = 0
        if event.key == pygame.K_RIGHT:
            x_change = (segment_width + segment_margin)
            y_change = 0
        if event.key == pygame.K_UP:
            x_change = 0
            y_change = (segment_height + segment_margin) * -1
        if event.key == pygame.K_DOWN:
            x_change = 0
            y_change = (segment_height + segment_margin)

def screen_wrap():
        x = snake_segments[0].rect.x + x_change
        x=x%SCREEN_WIDTH
        y = snake_segments[0].rect.y + y_change
        y=y%SCREEN_HEIGHT
        segment = Segment(x, y)
        return segment

def load_game():
    global list_of_scores
    f = open("savefile.txt", "r")
    string_list = f.read()
    for r in string_list:
        if r>='0' and r<='9':
            list_of_scores.append(int(r))


def menu_screen():
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption('Snake')
    screen.fill(BLACK)

    #game over and contiune buttons
    color1 = (255, 255, 255)
    color2 = (255, 255, 255)
    color3 = (255, 255, 255)
    x_change = 0
    y_change = 0
    unclicked=True
    rect1 = pygame.Rect(SCREEN_WIDTH/2-200, 50, 0, 0).inflate(300, 50)
    rect2 = pygame.Rect(SCREEN_WIDTH/2+200, 50, 0, 0).inflate(300, 50)
    rect3 = pygame.Rect(SCREEN_WIDTH/2,SCREEN_HEIGHT/2, 0, 0).inflate(300, 50)
    while unclicked:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                unclicked = True
            point = pygame.mouse.get_pos()
            collide1 = rect1.collidepoint(point)
            collide2 = rect2.collidepoint(point)
            collide3 = rect3.collidepoint(point)
            if collide1:
                color1 = (0, 255, 0)
                if event.type == pygame.MOUSEBUTTONUP:
                    unclicked = False
                    #max number of recursions is 1000
                    game_loop()
                    
            elif collide2:
                color2 = (0, 0, 255)
                if event.type == pygame.MOUSEBUTTONUP:
                    unclicked = False
                    load_game()
                    game_loop()

            elif collide3:
                color3 = (255, 0, 0)
                if event.type == pygame.MOUSEBUTTONUP:
                    unclicked = False
                    done = True
                    exit()

            else:
                color1 = (255, 255, 255)
                color2 = (255, 255, 255)
                color3 = (255, 255, 255)
            pygame.draw.rect(screen, color1, rect1)
            pygame.draw.rect(screen, color2, rect2)
            pygame.draw.rect(screen, color3, rect3)
            screen.blit(font.render('New Game', True, (0,0,0)), (SCREEN_WIDTH/2-250, 35))
            screen.blit(font.render('Continue', True, (0,0,0)), (SCREEN_WIDTH/2+150, 35))
            screen.blit(font.render('Quit', True, (0,0,0)), (SCREEN_WIDTH/2-30,SCREEN_HEIGHT/2-10))
            pygame.display.flip()

def game_loop():

    global allspriteslist,snake_segments,x_change,y_change,list_of_scores,pointgroup
    
    initialise_for_loop()

    initialise_snake()

    segment=snake_segments[len(snake_segments)-1]

    #initialising the points
    point = Point(20,20)
    pointgroup.add(point)
    
    clock = pygame.time.Clock()
    done = False

    while not done:
        #before moving the snake we add all the obstacles
        for i in range(game_matrix_rows):
            for j in range(game_matrix_cols):
                if obstacle_matrix[j][i]== 1:
                    obstacle = Segment(i*20,j*20)
                    obstacles.add(obstacle)
        point_acquired = False

        #for quitting during the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            snake_movement(event)

        #acquiring a point
        point_hit_list = pygame.sprite.spritecollide(segment, pointgroup, False)
        if(point_hit_list): point_acquired=True

        #"animation"
        if not point_acquired:
            old_segment = snake_segments.pop()
            allspriteslist.remove(old_segment)

        #adding another random point to the board, if one has been collected, 
        else: 
            pointgroup.remove(point)
            point = Point(random.randrange(0, SCREEN_WIDTH,20),random.randrange(0, SCREEN_HEIGHT,20))
            point_hit_list = pygame.sprite.spritecollide(point, obstacles, True)
            if(point_hit_list):
                while (point_hit_list):
                    point = Point(random.randrange(0, SCREEN_WIDTH,20),random.randrange(0, SCREEN_HEIGHT,20))
                    point_hit_list = pygame.sprite.spritecollide(point, obstacles, True)
            pointgroup.add(point)

        segment = screen_wrap()

        #collision and game over
        blocks_hit_list = pygame.sprite.spritecollide(segment, allspriteslist, True)
        blocks_hit_list1 =  pygame.sprite.spritecollide(segment, obstacles, True)
        if(blocks_hit_list or blocks_hit_list1):
            pointgroup.remove(point)
            game_over()
            

        #drawing all elements on the screen       
        snake_segments.insert(0, segment)
        allspriteslist.add(segment)
        screen.fill(BLACK)
        allspriteslist.draw(screen)
        pointgroup.draw(screen)
        obstacles.draw(screen)
        screen.blit(font.render(str(len(snake_segments)), True, (255,255,255)), (SCREEN_WIDTH/2, SCREEN_HEIGHT-50))
        pygame.display.flip()

        #gamespeed
        clock.tick(len(snake_segments)*2)

if __name__=="__main__":
    parse_command()
    menu_screen()     
    pygame.quit()