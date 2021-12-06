import pygame
import random
pygame.init()
bigfont = pygame.font.Font(None, 80)
smallfont = pygame.font.Font(None, 45)
SCREEN_WIDTH=1080
SCREEN_HEIGHT=720
list_of_scores=[]
scorelist = pygame.sprite.Group()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def all_of_it():
    global list_of_scores
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    SNAKE_LENGTH=3
    SCREEN_WIDTH=1080
    SCREEN_HEIGHT=720
    # Set the width and height of each snake segment and point
    segment_width = 18
    segment_height = 18
    point_witdh = 20
    point_height = 20
    # Margin between each segment
    segment_margin = 2
    
    # Set initial speed
    x_change = segment_width + segment_margin
    y_change = 0
    
    
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
        if(blocks_hit_list):
            screen.fill(BLACK)
            x_change = 0
            y_change = 0
            unclicked=True
            rect1 = pygame.Rect(SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2, 0, 0).inflate(100, 100)
            rect2 = pygame.Rect(SCREEN_WIDTH/2+100, SCREEN_HEIGHT/2, 0, 0).inflate(100, 100)
            while unclicked:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        unclicked = False
                point = pygame.mouse.get_pos()
                collide1 = rect1.collidepoint(point)
                collide2 = rect2.collidepoint(point)
                if collide1:
                    color1 = (0, 255, 0)
                    if event.type == pygame.MOUSEBUTTONUP:all_of_it()
                if collide2:
                    color2 = (255, 0, 0)
                    if event.type == pygame.MOUSEBUTTONUP:
                        unclicked = False
                        done = True
                else:
                    color1 = (255, 255, 255)
                    color2 = (255, 255, 255)
                pygame.draw.rect(screen, color1, rect1)
                pygame.display.flip()
                pygame.draw.rect(screen, color2, rect2)
                pygame.display.flip()
            
            



        #drawing all elements on the screen
        snake_segments.insert(0, segment)
        allspriteslist.add(segment)
        screen.fill(BLACK)
        allspriteslist.draw(screen)
        pointgroup.draw(screen)
        pygame.display.flip()
        #gamespeed
        clock.tick(len(snake_segments))
        print(len(snake_segments))
        
    pygame.quit()

all_of_it()