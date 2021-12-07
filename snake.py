import pygame
import random
import argparse
import json
pygame.init()
bigfont = pygame.font.Font(None, 80)
smallfont = pygame.font.Font(None, 45)
SCREEN_WIDTH=1000
SCREEN_HEIGHT=1000
list_of_scores=[]
obstacles = pygame.sprite.Group()
scorelist = pygame.sprite.Group()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
segment_width = 18
segment_height = 18
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
game_matrix_rows=0
game_matrix_cols=0
obstacle_matrix=[],[]

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
    #parser.add_argument('file', type=argparse.FileType('r'))
    args = parser.parse_args()
    print(args)
    with open('table.json') as f:
        d = json.load(f)
        SCREEN_WIDTH =20* int(d['rows'])
        SCREEN_HEIGHT =20* int(d['cols'])
    game_matrix_rows = int(d['rows'])
    game_matrix_cols = int(d['cols'])
    obstacle_matrix = d['game_state']



    

def all_of_it():
    for i in range(game_matrix_rows):
        for j in range(game_matrix_cols):
            if obstacle_matrix[j][i]== 1:
                obstacle = Segment(i*20,j*20)
                obstacles.add(obstacle)
    font = pygame.font.SysFont('Arial', 25)
    global list_of_scores
    BLACK = (0, 0, 0)
    SNAKE_LENGTH=3
    # Set the width and height of each snake segment and point
    segment_width = 18
    segment_height = 18
    # Margin between each segment
    segment_margin = 2
    
    # Set initial speed
    x_change = segment_width + segment_margin
    y_change = 0
    
    #initialising the screen
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pygame.display.set_caption('Snake')
    allspriteslist = pygame.sprite.Group()
    pointgroup = pygame.sprite.Group()
    
    #initialising the snake
    snake_segments = []
    for i in range(SNAKE_LENGTH):
        x = 20
        y = 20
        segment = Segment(x, y)
        snake_segments.append(segment)
        allspriteslist.add(segment)

    #initialising the points
    point = Point(100,100)
    pointgroup.add(point)
    
    clock = pygame.time.Clock()
    done = False


    while not done:
        point_acquired = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

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

        point_hit_list = pygame.sprite.spritecollide(segment, pointgroup, False)
        if(point_hit_list): point_acquired=True

        #"animation" and screenwrap
        if not point_acquired:
            old_segment = snake_segments.pop()
            allspriteslist.remove(old_segment)
        else: 
            pointgroup.remove(point)
            #random.randrange(start, stop[, step])
            point = Point(random.randrange(0, SCREEN_WIDTH,20),random.randrange(0, SCREEN_HEIGHT,20))
            pointgroup.add(point)

        x = snake_segments[0].rect.x + x_change
        x=x%SCREEN_WIDTH
        y = snake_segments[0].rect.y + y_change
        y=y%SCREEN_HEIGHT
        segment = Segment(x, y)

        #collision and game over
        blocks_hit_list = pygame.sprite.spritecollide(segment, allspriteslist, True)
        blocks_hit_list1 =  pygame.sprite.spritecollide(segment, obstacles, True)
        if(blocks_hit_list or blocks_hit_list1):
            screen.fill(BLACK)
            y_score=50+100
            
            list_of_scores.append(len(snake_segments)+1)
            screen.blit(font.render('High scores', True, (255,255,255)), (SCREEN_WIDTH/2-60, y_score))
            y_score+=25
            list_of_scores.sort(reverse=True)
            score_display_max=SCREEN_HEIGHT/2
            score_count=0
            for score in list_of_scores:
                score_count+=25
                if(score_count>score_display_max): break
                screen.blit(font.render(str(score), True, (255,255,255)), (SCREEN_WIDTH/2, y_score))
                pygame.display.flip()
                y_score+=25

            
           
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
                        all_of_it()
                elif collide2:
                    color2 = (255, 0, 0)
                    if event.type == pygame.MOUSEBUTTONUP:
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
            

        #drawing all elements on the screen
        
        snake_segments.insert(0, segment)
        allspriteslist.add(segment)
        screen.fill(BLACK)
        allspriteslist.draw(screen)
        pointgroup.draw(screen)
        obstacles.draw(screen)
        screen.blit(font.render(str(len(snake_segments)), True, (255,255,255)), (SCREEN_WIDTH/2, 100))
        pygame.display.flip()
        #gamespeed
        clock.tick(len(snake_segments))
        
parse_command()
all_of_it()
pygame.quit()