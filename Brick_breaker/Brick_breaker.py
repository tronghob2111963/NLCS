import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

bg_color = (0, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

window = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Brick Breaker")
font = pygame.font.Font('freesansbold.ttf', 15)
mess_font = pygame.font.Font('freesansbold.ttf', 50)
FPS = 60

paddle_width = 100
paddle_height = 20

paddle_color = (255, 255, 255)

paddle_x = (WIDTH - paddle_width) // 2
paddle_y = HEIGHT - 50

clock = pygame.time.Clock()


class Paddle:
    def __init__(self, posX, posY, width, height, speed, color):
        self.posX, self.posY = posX, posY
        self.width, self.height = width, height
        self.speed = speed
        self.color = color
        self.paddleRect = pygame.Rect(self.posX, self.posY, self.width, self.height)
        self.paddle = pygame.draw.rect(window, self.color, self.paddleRect)

    def display(self):
        self.paddle = pygame.draw.rect(window, self.color, self.paddleRect)

    def update(self, xFac):
        self.posX += self.speed * xFac
        if self.posX <= 0:
            self.posX = 0
        elif self.posX + self.width >= WIDTH:
            self.posX = WIDTH - self.width
        self.paddleRect = pygame.Rect(self.posX, self.posY, self.width, self.height)

    def getRect(self):
        return self.paddleRect


class Block:
    def __init__(self, posx, posy, width, height, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.color = color
        self.damage = 100
        self.health = 100
        self.blockRect = pygame.Rect(self.posx, self.posy, self.width, self.height)
        self.block = pygame.draw.rect(window, self.color, self.blockRect)

    def display(self):
        if self.health > 0:
            self.brick = pygame.draw.rect(window, self.color, self.blockRect)

    def hit(self):
        self.health -= self.damage

    def getRect(self):
        return self.blockRect

    def getHealth(self):
        return self.health


def collisionChecker(rect, ball):
    if pygame.Rect.colliderect(rect, ball):
        return True
    return False


class Ball:
    def __init__(self, posX, posY, radius, speed, color):
        self.posX, self.posY = posX, posY
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac, self.yFac = 1, 1
        self.ball = pygame.draw.circle(window, self.color, (self.posX, self.posY), self.radius)
    def display(self):
        self.ball = pygame.draw.circle(window, self.color, (self.posX, self.posY), self.radius)
    def update(self):
        self.posX += self.xFac * self.speed
        self.posY += self.yFac * self.speed
        if self.posX <= 0 or self.posX >= WIDTH:
            self.xFac *= -1
        if self.posY <= 0:
            self.yFac *= -1
        if self.posY >= HEIGHT:
            return True
        return False
    def reset(self):
        self.posX = 0
        self.posY = HEIGHT
        self.xFac, self.yFac = 1, -1
    def hit(self):
        self.yFac *= -1
    def getRect(self):
        return self.ball


def gameOver():
    gameOver = True
    game_over_mess = mess_font.render("Game over", True, RED)
    game_over_mess_rect = game_over_mess.get_rect()
    game_over_mess_rect = (WIDTH // 2, HEIGHT // 2 + 10)

    while gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
        window.blit(game_over_mess, game_over_mess_rect)
        pygame.display.update()


def gameWin(score):
    gameWin = True
    game_win_mess = mess_font.render("You Win!", True, GREEN)
    score_mess = font.render("Your Score: " + str(score), True, WHITE)
    game_win_mess_rect = game_win_mess.get_rect()
    game_win_mess_rect.center = (WIDTH // 2, HEIGHT // 2 + 10)
    score_mess_rect = score_mess.get_rect()
    score_mess_rect.center = (WIDTH // 2, HEIGHT // 2 + 50)

    while gameWin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
        window.blit(game_win_mess, game_win_mess_rect)
        window.blit(score_mess, score_mess_rect)
        pygame.display.update()


def populateBlock(blockWidth, blockHeight, horizontalGap, verticalGap):
    listOfBlock = []
    for i in range(10, 750, blockWidth + horizontalGap):
        for j in range(10, HEIGHT // 5, blockHeight + verticalGap):
            listOfBlock.append(Block(i, j, blockWidth, blockHeight, GREEN))
    return listOfBlock


def main():
    running = True
    game_started = False
    lives = 3
    score = 0

    scoreText = font.render("Score", True, WHITE)
    scoreTextRect = scoreText.get_rect()
    scoreTextRect.center = (20, HEIGHT - 10)

    livesText = font.render("Lives", True, WHITE)
    livesTextRect = livesText.get_rect()
    livesTextRect.center = (100, HEIGHT - 10)

    name_game = mess_font.render("Brick Breaker", True, WHITE)
    name_game_rect = name_game.get_rect()
    name_game_rect.center = (WIDTH // 2, HEIGHT // 2 + 10)

    start_text = font.render("Press Space to Start", True, WHITE)
    start_text_rect = start_text.get_rect()
    start_text_rect.center = (WIDTH // 2, HEIGHT // 2 + 50)

    paddle = Paddle(0, HEIGHT - 50, 100, 20, 10, WHITE)

    paddleFacx = 0
    ball = Ball(1, HEIGHT - 100, 7, 3, RED)
    blockWidth, blockHeight = 40, 30
    horizontalGap, verticalGap = 1, 1

    listofBlock = populateBlock(blockWidth, blockHeight, horizontalGap, verticalGap)

    while running:
        window.fill(BLACK)
        if not game_started:
            window.blit(name_game, name_game_rect)
            window.blit(start_text, start_text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_started = True
            pygame.display.update()
            continue

        window.blit(scoreText, scoreTextRect)
        window.blit(livesText, livesTextRect)

        scoreText = font.render("Score " + str(score), True, WHITE)
        livesText = font.render("Lives " + str(lives), True, WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    paddleFacx = -1
                if event.key == pygame.K_RIGHT:
                    paddleFacx = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    paddleFacx = 0

        if not listofBlock:
            running = gameWin(score)
            while listofBlock:
                listofBlock.pop(0)
            lives = 3
            score = 0
            listofBlock = populateBlock(blockWidth, blockHeight, horizontalGap, verticalGap)

        if lives <= 0:
            running = gameOver()
            while listofBlock:
                listofBlock.pop(0)
            lives = 3
            score = 0
            listofBlock = populateBlock(blockWidth, blockHeight, horizontalGap, verticalGap)

        if collisionChecker(paddle.getRect(), ball.getRect()):
            ball.hit()
        for block in listofBlock:
            if collisionChecker(block.getRect(), ball.getRect()):
                ball.hit()
                block.hit()
                if block.getHealth() <= 0:
                    listofBlock.pop(listofBlock.index(block))
                    score += 5

        paddle.update(paddleFacx)
        paddle.display()
        lifeLost = ball.update()
        if lifeLost:
            lives -= 1
            ball.reset()
        ball.display()
        for block in listofBlock:
            block.display()

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()


