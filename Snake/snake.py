import pygame
import random
import copy
from button import Button

pygame.init()

# display the window of game
blockLength = 30
screenWidth = 600
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))

# caption the window
pygame.display.set_caption("SNAKE")

# icon of the window
icon = pygame.image.load(
    "C:\\Users\\hp\\Desktop\\All\\vs_codes\\pygamecode\\Snake\\snake.png")
pygame.display.set_icon(icon)

# colors for the game
dim_white = (100, 100, 100)  # color of grid lines and scoreCount
white = (0, 0, 255)  # color of snake
red = (0, 255, 0)  # color of food
black = (255, 255, 255)  # color of background
green = (255, 0, 0)  # color of GameOver text

# list for getting random co-ordinates of food and snake head
xCordList = [x for x in range(0, screenWidth, blockLength)]
yCordList = [y for y in range(0, screenHeight, blockLength)]
snakeHeadX = random.choice(xCordList)
snakeHeadY = random.choice(yCordList)

# GAMEOVER text


def show_gameover():
    global screenHeight
    global screenWidth
    text = pygame.font.Font("freesansbold.ttf", int(screenHeight*0.1))
    gameover = text.render("GAME OVER", True, green)
    screen.blit(gameover, (int(screenWidth*0.18), int(screenHeight*0.4)))


# Score text
scoreFont = pygame.font.Font("freesansbold.ttf", int(screenHeight*0.08))


def showScore(x, y):
    global scoreFont
    global scoreCount
    score = scoreFont.render(str(scoreCount), True, dim_white)
    screen.blit(score, (x, y))

# grid view


def grid():
    for i in range(0, screenWidth, blockLength):
        pygame.draw.line(screen, dim_white, (i, 0), (i, screenHeight), 2)

    for j in range(0, screenWidth, blockLength):
        pygame.draw.line(screen, dim_white, (0, j), (screenWidth, j), 2)


# returns random co-ordinates in tuple
def randomCoordinates():
    x, y = random.choice(xCordList), random.choice(yCordList)
    return (x, y)


# for first food
foodPosition = randomCoordinates()

# display at given coordinates


def show_Food(cordinates):
    pygame.draw.rect(screen, red, (cordinates, (blockLength, blockLength)))


playClicked = False
while True:
    # adding play button
    b = Button(screen, (80, 45, 200), (200, 250, 255),
               (int(screenWidth*0.4), int(screenHeight*0.4)), (100, 60), "PLAY", 30)
    state = 'original'
    while not playClicked:
        screen.fill((200, 200, 200))
        b.show()
        for event in pygame.event.get():
            if b.isOverMouse() == True:
                state = 'changed'
                if event.type == pygame.MOUSEBUTTONUP:
                    playClicked = True
            elif b.isOverMouse() == False:
                state = 'original'
            if event.type == pygame.QUIT:
                pygame.quit()
        if state == 'changed':
            b.changeColor((80, 240, 80), (14, 37, 100))

        pygame.display.update()

    # change in X and Y of snake's head
    changeSnakeY = 0
    changeSnakeX = blockLength

    # clock for fps
    clock = pygame.time.Clock()
    # game over condition
    over = False
    # food eaten condition
    eaten = False

    # snakeLength
    snakeLength = 1

    # snakePostion list
    snakePositions = []

    # game loop
    while True:

        # iter the loop 10 times in 1 sec, otherwise it will eat up your cpu memory
        clock.tick(5)
        scoreCount = snakeLength - 1

        # game over condition
        for i in range(len(snakePositions)):
            if snakePositions[i] == (snakeHeadX, snakeHeadY):
                over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # exit game
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if changeSnakeY != blockLength:
                        changeSnakeY = -blockLength
                        changeSnakeX = 0
                if event.key == pygame.K_DOWN:
                    if changeSnakeY != -blockLength:
                        changeSnakeY = blockLength
                        changeSnakeX = 0
                if event.key == pygame.K_LEFT:
                    if changeSnakeX != blockLength:
                        changeSnakeX = -blockLength
                        changeSnakeY = 0
                if event.key == pygame.K_RIGHT:
                    if changeSnakeX != -blockLength:
                        changeSnakeX = blockLength
                        changeSnakeY = 0
                if event.key == pygame.K_l:
                    snakeLength += 1
                if event.key == pygame.K_f:
                    foodPosition = randomCoordinates()

        # Logic of game

        if over == False:

            # adding info in a list about the positions where head is moving
            snakePositions.append((snakeHeadX, snakeHeadY))
            if len(snakePositions) == snakeLength:
                snakePositions.pop(0)

            screen.fill(black)

            snakeHeadX += changeSnakeX
            snakeHeadY += changeSnakeY

            # eating Food
            if (snakeHeadX, snakeHeadY) == foodPosition:
                eaten = True
                snakeLength += 1

            # portal boundaries
            if snakeHeadY <= -1:
                snakeHeadY = screenHeight - blockLength
            if snakeHeadY >= screenHeight - blockLength + 2:
                snakeHeadY = 0
            if snakeHeadX <= -1:
                snakeHeadX = screenWidth - blockLength
            if snakeHeadX >= screenWidth - blockLength + 2:
                snakeHeadX = 0

            # displaying snake

            snakeHead = pygame.draw.rect(
                screen, white, ((snakeHeadX, snakeHeadY), (blockLength, blockLength)))
            # snake's body
            for i in range(len(snakePositions)):
                pygame.draw.rect(
                    screen, white, (snakePositions[i], (blockLength, blockLength)))

            # displaying food
            if eaten:
                foodPosition = randomCoordinates()
                eaten = False
            show_Food(foodPosition)

            grid()

            # displaying Score
            showScore(10, 10)

        if over == True:
            b2 = Button(screen, (80, 45, 200), (200, 250, 255),
                        (int(screenWidth*0.4), int(screenHeight*0.7)), (150, 60), "REPLAY", 30)
            state2 = 'original'
            replayClicked = False
            while not replayClicked:
                show_gameover()
                b2.show()
                for event in pygame.event.get():
                    if b2.isOverMouse() == True:
                        state2 = 'changed'
                        if event.type == pygame.MOUSEBUTTONUP:
                            replayClicked = True
                    elif b2.isOverMouse() == False:
                        state2 = 'original'
                    if event.type == pygame.QUIT:
                        pygame.quit()
                if state2 == 'changed':
                    b2.changeColor((80, 240, 80), (14, 37, 100))

                pygame.display.update()

            break

        pygame.display.update()
