import sys
from random import randint
import pygame


def targetMovement(targetList):
    if targetList:
        for targetRect in targetList:
            targetRect.x -= 3
            WINDOW.blit(bird, targetRect)
        return targetList
    else:
        return []


def targetMovement2(targetList2):
    if targetList2:
        for targetRect2 in targetList2:
            targetRect2.x += 3
            WINDOW.blit(duck, targetRect2)
        return targetList2
    else:
        return []


# setup
pygame.init()
pygame.font.init()
pygame.mixer.init()

# window
WIDTH = 640
HEIGHT = 480
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")

score = 0

# images
sky = pygame.image.load('Assets/sky.png')
sea = pygame.image.load('Assets/sea.png')
crosshair = pygame.image.load('Assets/crosshair.png')
crosshairRect = crosshair.get_rect()
pygame.mouse.set_visible(False)

# targets
duck = pygame.transform.scale(pygame.image.load('Assets/duck.png'), (110, 110))
duckRect = duck.get_rect(center=(-60, 350))
targetRectList2 = []

bird = pygame.transform.scale(pygame.image.load("Assets/bird.png"), (130, 130))
birdRect = bird.get_rect(center=(710, 120))
targetRectList = []

# music
bgMusicChannel = pygame.mixer.Channel(0)
soundtrack = pygame.mixer.Sound('Assets/backgroundMusic.mp3')
bgMusicChannel.play(soundtrack, loops=-1)


duckSound = pygame.mixer.Sound('Assets/quackSound.mp3')
birdSound = pygame.mixer.Sound('Assets/birdSound.mp3')

gunshot = pygame.mixer.Sound('Assets/gunshot.mp3')
gunshot.set_volume(0.8)

gunshotChannel = pygame.mixer.Channel(1)
duckSoundChannel = pygame.mixer.Channel(2)
birdSoundChannel = pygame.mixer.Channel(3)

# text
gameFont = pygame.font.Font(None, 35)

# timer
targetTimer = pygame.USEREVENT + 1
pygame.time.set_timer(targetTimer, 1500)

clock = pygame.time.Clock()

running = True
while running:
    clock.tick(60)
    pygame.display.update()

    mousePos = pygame.mouse.get_pos()
    crosshairRect.center = mousePos

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == targetTimer:
            targetRectList.append(bird.get_rect(center=(randint(710, 1000), 120)))

        if event.type == targetTimer:
            targetRectList2.append(duck.get_rect(center=(randint(-300, -60), 350)))

        # controller and collision for bird
        if event.type == pygame.MOUSEBUTTONDOWN:
            gunshotChannel.play(gunshot)
            for targetRect in targetRectList:
                if targetRect.collidepoint(event.pos):
                    score += 1
                    targetRectList.remove(targetRect)
                    birdSoundChannel.play(birdSound)

        # controller and collision for bird
        if event.type == pygame.MOUSEBUTTONDOWN:
            gunshotChannel.play(gunshot)
            for targetRect2 in targetRectList2:
                if targetRect2.collidepoint(event.pos):
                    score += 1
                    targetRectList2.remove(targetRect2)
                    duckSoundChannel.play(duckSound)

    targetRectList = targetMovement(targetRectList)
    targetRectList2 = targetMovement2(targetRectList2)

    # drawing on WIN
    WINDOW.blit(sea, (-10, 240))
    WINDOW.blit(sky, (0, -45))
    fontSurf = gameFont.render(f"Score: {score}", True, 'yellow')
    WINDOW.blit(fontSurf, (10, 10))
    for targetRect2 in targetRectList2:
        WINDOW.blit(duck, targetRect2)

    for targetRect in targetRectList:
        WINDOW.blit(bird, targetRect)
    WINDOW.blit(crosshair, crosshairRect)
