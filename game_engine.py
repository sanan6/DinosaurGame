import pygame
from pygame.locals import *
from pygame.mixer import Sound
from dinosaur import Dinosaur
from settings import *
import sys
from collections import deque
from environment import Cacti
from environment import Fly
import random

class Game(object):
    """
    The brain behind everything that goes on during a game
    """
    def __init__(self):
        """
        Create the game
        """
        pygame.init()

        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode(SIZE_GAME)

        self.started = 0

        # loading of sounds
        self.death_sound = Sound("assets/sounds/death2.wav")
        self.score_sound = Sound("assets/sounds/score2.wav")
        self.score_sound.set_volume(0.1)

        # background
        self.background = pygame.image.load('assets/images/background.png').convert()
        self.background = pygame.transform.scale(self.background, SIZE_GAME)

        # starting Dino
        self.dino = Dinosaur(WIN_WIDTH / 16)
        self.screen.blit(self.background, (0, 0))
        self.dino.draw(self.screen)
        pygame.display.flip()

        # First Obstacles
        self.obstacles = deque()
        self.obstacles.append(Cacti(WIN_WIDTH))

        # Scores
        self.slower_score = 0
        self.score = 0

        # Fonts
        self.game_font = pygame.font.SysFont(None, 32, bold=True)

    def update_obstacles(self, seed = None):
        """
        Creates a new obstacle (cactus or pterodactyl) randomly.

        :param seed: random generation is based on a shared seed from the server
        :return: None
        """
        for obstacle in self.obstacles:
            obstacle.update()

        if seed:
            random.seed(seed)
        if self.obstacles[0].X < -120:
            self.obstacles.popleft()
        if self.obstacles[-1].X < WIN_WIDTH - (random.randint(3, 10) * CACTUS_WIDTH):
            if random.randint(0, 1):
                self.obstacles.append(Cacti(WIN_WIDTH))
            else:
                self.obstacles.append(Fly(WIN_WIDTH, 120 + (random.randint(0, 2) * 100)))

    def events(self):
        """
        Handles the inputs coming from the user. It is pushing the space button to jump,
        and push and letting go the down arrow to make the dino duck during the button hold.

        :return: None
        """
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_SPACE:
                self.dino.jump()
                self.started = 1

            if event.type == KEYDOWN and event.key == K_DOWN:
                self.dino.duck()
                self.started = 1

            if event.type == KEYUP and event.key == K_DOWN:
                self.dino.un_duck()

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

    def game_over(self):
        """
        Handles the game_over by stopping the dino, and playing the death sound.
        The last frame of the game is still drawn just like in the original game.

        :return: None
        """
        score_message = self.game_font.render(str(self.score), True, (0, 0, 0))
        message = self.game_font.render("GAME OVER!", True, (0, 0, 0))
        Sound.play(self.death_sound)

        for i in range(FPS * 3):

            self.screen.blit(self.background, (0, 0))
            for obstacle in self.obstacles:
                obstacle.draw(self.screen, is_alive = False)
            self.dino.draw(self.screen, is_alive = False)
            self.screen.blit(score_message, (WIN_WIDTH / 2 - score_message.get_width() / 2, 20))
            self.screen.blit(message, (WIN_WIDTH / 2 - message.get_width() / 2, 50))

            pygame.display.update()

            self.clock.tick(FPS)

    def game_main(self):
        """
        This is called when a new game is initiated. This updates the screen, checks for collision,
        and counts the score.

        :return: None
        """

        while True:
            self.events()

            # Update object positions and check for collisions
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

            if self.score > 0:
                if self.score % 100 == 0:
                    Sound.play(self.score_sound)

            pygame.display.update()

            self.clock.tick(FPS)

def start():
    """
    This is called when we push the single player button. It initiates the game.

    :return: None
    """
    new_game = Game()
    new_game.game_main()
    pygame.display.set_mode(SIZE)
