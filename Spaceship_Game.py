import pygame
import os

WIDTH, HEIGHT = 1000, 667

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACESHIP FIGHT!")

pygame.mixer.init(22050,-16,2,2048)
pygame.font.init()

BORDER = pygame.Rect(WIDTH/2-2.5, 0, 5, HEIGHT)

WINNING_SCORE = 10

WHITE = (255,255,255)
BLACK = (0,0,0)
LIGHT_BLUE = (0,155,255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

DEFAULT_IMAGE_SIZE = (500,413)
FPS = 60
SHIP_WIDTH = 80
SHIP_HEIGHT = 68
VELOCITY = 5

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

BULLET_VEL = 25
MAX_BULLETS = 300

GUN_SOUND_01 = ("Assets\Assets_Gun+Silencer.mp3")
BULLET_HIT_SOUND = ("Assets\Assets_Grenade+1.mp3")

blue_ship_2 = 'pinpng.com-space-ship-png-313268.png'
SHIP_3 = 'balck_white_ship_01.png'
grey_ship_1 = 'PngItem_851786.png'

#Images
SHIP_2 = pygame.image.load(os.path.join('Assets', blue_ship_2))
SHIP_1 = pygame.image.load(os.path.join('Assets', grey_ship_1))
SPACE_BACKGROUND = pygame.image.load(os.path.join('Assets', 'photo-1534796636912-3b95b3ab5986.jpg'))


#Ships rotated and scaled
ship_1 = pygame.transform.rotate(pygame.transform.scale(SHIP_1, (SHIP_WIDTH, SHIP_HEIGHT)), 270)
ship_2 = pygame.transform.rotate(pygame.transform.scale(SHIP_2, (SHIP_WIDTH, SHIP_HEIGHT)), 90)

WINNER_FONT = pygame.font.SysFont('comicsans', 100)


def draw_window(player2, player1, red_bullets, yellow_bullets, PLAYER1_SCORE, PLAYER2_SCORE):
    
    WIN.fill(WHITE)
    WIN.blit(SPACE_BACKGROUND, (0,0))
    
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    score_01 = myfont.render("PLAYER 1 SCORE: " + str(PLAYER1_SCORE), False, (255, 255, 255)) 
    score_02 = myfont.render("PLAYER 2 SCORE: " + str(PLAYER2_SCORE), False, (255, 255, 255)) 
    WIN.blit(score_01, (20,10))
    WIN.blit(score_02, (WIDTH/2 + 20, 10))
    
    pygame.draw.rect(WIN, BLACK, BORDER)
    
    #DRAW BULLETS
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)


    #DRAW SHIPS
    WIN.blit(ship_2, (player2.x, player2.y))
    WIN.blit(ship_1, (player1.x, player1.y))  

    pygame.display.update()



#SHIP 1 MOVEMENT AND BORDERS FOR SHIPS
def ship1_movement(keys_pressed, player1):
    
    if keys_pressed[pygame.K_a] and player1.x - VELOCITY > 0: #left
        player1.x -= VELOCITY
    if keys_pressed[pygame.K_d] and player1.x + VELOCITY + player1.width < BORDER.x+10: #right
        player1.x += VELOCITY    
    if keys_pressed[pygame.K_s] and player1.y + VELOCITY + player1.height < HEIGHT - 15: #down
        player1.y += VELOCITY           
    if keys_pressed[pygame.K_w]and player1.y - VELOCITY > 0: #up
        player1.y -= VELOCITY 

#SHIP 2 MOVEMENT AND BORDERS FOR SHIPS
def ship2_movement(keys_pressed, player2):
    
    if keys_pressed[pygame.K_LEFT] and  player2.x - VELOCITY > BORDER.x + BORDER.width: #left
        player2.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and player2.x + VELOCITY + player2.width < WIDTH+10: #right
        player2.x += VELOCITY                
    if keys_pressed[pygame.K_DOWN] and player2.y + VELOCITY + player2.height < HEIGHT - 15: #down
        player2.y += VELOCITY             
    if keys_pressed[pygame.K_UP] and player2.y - VELOCITY > 0: #up
        player2.y -= VELOCITY     

#WHAT HAPPENS WHEN BULLETS HIT OTHER SHIP
def handle_bullets(yellow_bullets, red_bullets, player1, player2):
    
    #PLAYER 1 BULLETS
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if player2.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    
    #PLAYER 2 BULLETS
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if player1.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, LIGHT_BLUE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/4 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)  
 

def main():
    
    #SCORE
    PLAYER2_SCORE = 0
    PLAYER1_SCORE = 0

    #PLAYERS
    player1 = pygame.Rect(100, 300, SHIP_WIDTH, SHIP_HEIGHT)
    player2 = pygame.Rect(700, 300, SHIP_WIDTH, SHIP_HEIGHT)
    
    red_bullets = []
    yellow_bullets = []
    
    #LOOP TO RUN PROGRAM
    clock  = pygame.time.Clock()

    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            #FIRES PLAYER 1 BULLETS
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    pygame.mixer.music.load(GUN_SOUND_01)
                    bullet = pygame.Rect(
                        player1.x+5 + player1.width-25, player1.y + player1.height//2 +5, 10, 5)
                    yellow_bullets.append(bullet)
                    pygame.mixer.music.play(0,0,5)
                    
                #FIRES PLAYER 2 BULLETS
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    pygame.mixer.music.load(GUN_SOUND_01)
                    bullet = pygame.Rect(
                        player2.x-15, player2.y + player2.height//2 + 3, 10, 5)
                    red_bullets.append(bullet)
                    pygame.mixer.music.play(0,0,5)
            
            #PLAYER 2 HIT
            if event.type == RED_HIT:
                pygame.mixer.music.load(BULLET_HIT_SOUND)
                PLAYER1_SCORE += 1
                pygame.mixer.music.play(0,0,5)
                

            #PLAYER 1 HIT
            if event.type == YELLOW_HIT:
                pygame.mixer.music.load(BULLET_HIT_SOUND)
                PLAYER2_SCORE += 1
                pygame.mixer.music.play(0,0,5) 
        
        
        keys_pressed = pygame.key.get_pressed()
        
        ship1_movement(keys_pressed, player1)
        ship2_movement(keys_pressed, player2)
        handle_bullets(yellow_bullets, red_bullets, player1, player2)
        draw_window(player2, player1, red_bullets, yellow_bullets, PLAYER1_SCORE, PLAYER2_SCORE)


        #CHECK FOR WINNER
        winner_text = ""

        if PLAYER1_SCORE >= 10:
            winner_text = "PLAYER 1 WINS!"
        if PLAYER2_SCORE >= 10:
            winner_text = "PLAYER 2 WINS!"
        if winner_text != "":
            draw_winner(winner_text)
            break
            
    main()

if __name__ == "__main__":
    main()
