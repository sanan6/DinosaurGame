import pygame
from pygame.locals import *
from dinosaur import Dinosaur
from settings import *
import sys
from collections import deque
from environment import Cacti
import random

class Game(object):

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(SIZE_GAME)
        self.started = 0

        self.background = pygame.image.load('assets/images/background.png').convert()
        self.background = pygame.transform.scale(self.background, SIZE_GAME)

        self.dino = Dinosaur(WIN_WIDTH / 16, BASELINE)
        self.screen.blit(self.background, (0, 0))
        self.dino.draw(self.screen)
        pygame.display.flip()

        self.obstacles = deque()
        self.obstacles.append(Cacti(WIN_WIDTH))

        self.slower_score = 0
        self.score = 0

        self.game_font = pygame.font.SysFont(None, 32, bold=True)

    def update_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.update()

        if self.obstacles[0].X < -120:
            self.obstacles.popleft()
        if self.obstacles[-1].X < WIN_WIDTH - (random.randint(3, 10) * CACTUS_WIDTH):
            self.obstacles.append(Cacti(WIN_WIDTH))

    def events(self):

        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_SPACE:
                self.dino.jump()
                self.started = 1

            if event.type == KEYDOWN and event.key == K_DOWN:
                self.dino.duck()
                self.started = 1

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

    def game_over(self):
        score_message = self.game_font.render(str(self.score), True, (0, 0, 0))
        message = self.game_font.render("GAME OVER!", True, (0, 0, 0))

        for i in range(FPS * 5):

            self.screen.blit(self.background, (0, 0))
            for obstacle in self.obstacles:
                obstacle.draw(self.screen)
            self.dino.draw(self.screen)
            self.screen.blit(score_message, (WIN_WIDTH / 2 - score_message.get_width() / 2, 20))
            self.screen.blit(message, (WIN_WIDTH / 2 - message.get_width() / 2, 50))

            pygame.display.update()
            self.clock.tick(FPS)

    def game_main(self):

        while True:
            self.events()

            if self.started:
                self.dino.update()
                self.update_obstacles()
                if any([obstacle.collides(self.dino) for obstacle in self.obstacles]):
                    self.game_over()
                    break
                self.slower_score += 1
                if self.slower_score > 5:
                    self.score += 1
                    self.slower_score = 0

            self.screen.blit(self.background, (0, 0))
            self.dino.draw(self.screen)
            for obstacle in self.obstacles:
                obstacle.draw(self.screen)

            score_message = self.game_font.render(str(self.score), True, (0, 0, 0))
            self.screen.blit(score_message, (WIN_WIDTH / 2 - score_message.get_width() / 2, 20))

            pygame.display.update()

            self.clock.tick(FPS)

def start():
    new_game = Game()
    new_game.game_main()