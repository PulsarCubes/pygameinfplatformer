import math
import pygame
import random as rand


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('the_guy-removebg-preview.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = False

    def flip(self):
        self.image = pygame.transform.flip(self.image, True, False)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.image = pygame.image.load('platform-removebg-preview.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Floor(Platform):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((1200, 50))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 865


pygame.init()
jumping = False
WHITE = (255, 255, 255)
green = (68, 234, 82)
flip = False
width, height = 1200, 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('GTTTATINT Clone')
bg = pygame.image.load('sky.gif').convert()
scroll = 0
tiles = math.ceil(width / bg.get_width()) + 1
score=-1
clock = pygame.time.Clock()
running = True
gravity = 0.7
player_speed_y = 0

player = Player(600, 650)
player_group = pygame.sprite.Group()
player_group.add(player)
platform1 = Platform()
platform2 = Platform()
platform3 = Platform()

floor = Floor()
platformgroup = pygame.sprite.Group()
platformgroup.add(platform1)
platformgroup.add(platform2)
platformgroup.add(platform3)
platformlist=[platform1, platform2, platform3]
platformgroup.add(floor)


def handle_collisions(player, platforms):
    global player_speed_y
    global jumping
    for platform in platforms:
        if player.rect.colliderect(platform.rect):

            if player.rect.bottom <= platform.rect.top + player_speed_y:
                player.rect.bottom = platform.rect.top
                player_speed_y = 0
                jumping = False  # Reset vertical speed after collision
            # elif player.rect.top >= platform.rect.bottom - player_speed_y:
            #     player.rect.top = platform.rect.bottom
            #     player_speed_y = 0  # Reset vertical speed after collision
            elif player.rect.right <= platform.rect.left + 10:
                player.rect.right = platform.rect.left
            elif player.rect.left >= platform.rect.right - 10:
                player.rect.left = platform.rect.right


def randomizeplatforms():
    global platformlist
    global score
    min_distance = 250
    max_distance = 250

    # Place the first platform within jumping distance from the player's starting position
    platformlist[0].rect.x = rand.randint(200, 900)
    platformlist[0].rect.y = rand.randint(player.rect.bottom - 300, player.rect.bottom - 200)

    # Copy of the platform list for iteration
    platformlist_copy = platformlist[1:]

    for platform in platformlist_copy:
        prev_platform = platformlist[platformlist.index(platform) - 1]
        platform.rect.x = rand.randint(200, 900)
        # Ensure the platform is within a reachable distance from the previous platform
        platform.rect.y = rand.randint(prev_platform.rect.y - max_distance, prev_platform.rect.y - min_distance)
        platformlist.remove(prev_platform)

    if platformlist:
        del platformlist[0]

    score+=1
def scrollplatforms():
    if player.rect.top < 0:
        scroll_amount = -player.rect.top
        for platform in platformgroup:
            platform.rect.y += scroll_amount
        player.rect.y += scroll_amount
def gameover():
    global score
    for platform in platformgroup:
        platform.kill()

    screen.fill(WHITE)
    screen.blit(bg, (0, 0))
    gofont = pygame.font.SysFont('Comic Sans MS', 70)
    gotext = gofont.render(f'Game Over! Your score was {str(score)}', True, (0, 0, 0))
    gorect = gotext.get_rect()
    gorect.center = (width / 2, height / 2)

    screen.blit(gotext, gorect)
    pygame.display.update()

    # Game Over loop to keep the screen open until the user quits
    gameover_running = True
    while gameover_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

randomizeplatforms()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        if player.rect.x > 0:
            player.rect.x -= 15
            if not player.direction:
                player.flip()
                player.direction = True
    if keys[pygame.K_RIGHT]:
        if player.rect.x < 1120:
            player.rect.x += 15
            if player.direction:
                player.flip()
                player.direction = False
    if keys[pygame.K_UP] and not jumping:
        player_speed_y = -27  # Adjust player speed when jumping
        jumping = True

    # Apply gravity always
    player_speed_y += gravity

    player.rect.y += player_speed_y

    # Check collision with platforms
    handle_collisions(player, platformgroup)
    scrollplatforms()
    for platform in platformgroup:
        if platform.rect.y>height:
            if platform is not floor:
                platformlist.append(platform)
                randomizeplatforms()



    if flip:
        player.flip()

    if player.rect.top>900:
        break
    screen.fill(WHITE)
    screen.blit(bg, (0, 0))

    platformgroup.draw(screen)
    player_group.draw(screen)

    font = pygame.font.SysFont('Comic Sans MS', 30)
    text = font.render(f'score:{str(score)}', True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.topleft = 0, 0

    screen.blit(text, text_rect)
    pygame.display.update()
    clock.tick(60)

gameover()
