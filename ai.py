import pickle
import pygame
import os
import neat
import random
from game_engine import Game
from dinosaur import Dinosaur
from environment import Cacti
from environment import Fly
from collections import deque
from settings import *


class AIGame(Game):
    def __init__(self):
        super().__init__()
        self.config_file = os.path.join(os.path.dirname(__file__), 'config-feedforward.txt')
        self.x = 0

    def eval_genome(self, genomes, config):
        """
        Runs the simulation of the current population of dinos and
        sets their fitness based on how far they get in the game.

        :return: None
        """
        # Obstacles
        obstacles = deque()
        obstacles.append(Cacti(WIN_WIDTH))

        # Creating lists holding the genome itself, the NN associated with the genome and the
        # dino object that uses that network to play
        nets = []
        gen = []
        dinos = []

        for genome_id, genome in genomes:
            genome.fitness = 0  # start with fitness level of 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            dinos.append(Dinosaur(WIN_WIDTH / 16))
            gen.append(genome)

        self.score = 0

        # Run until the user asks to quit
        run = True
        while run and len(dinos) > 0 and self.score <= 50:

            self.screen.blit(self.background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    run = False
                    with open('long', 'wb') as f:
                        pickle.dump(nets[0], f)
                    pygame.quit()
                    quit()
                    break

            obstacle_ind = 0
            if len(dinos) > 0:
                if len(obstacles) > 1 and dinos[0].X > obstacles[0].X + CACTUS_THICC:
                    # determine whether to use the first or second
                    # obstacle on the screen for neural network input
                    obstacle_ind = 1

            for i, dino in enumerate(dinos):  # give each dino a fitness of 0.1 for each frame it stays alive
                gen[i].fitness += 0.05
                dino.update()

                # send dino location, distance from next obstacle, what kind of obstacle it is and
                # determine from network whether to jump or not
                output = nets[dinos.index(dino)].activate(
                    (dino.Y, abs(dino.X + AIDINO_WIDTH - obstacles[obstacle_ind].X), obstacles[obstacle_ind].is_cactus))

                # use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
                if output[0] > 0.5:
                    dino.jump()

            # Update object positions and check for collisions
            reward = False
            for obstacle in obstacles:
                for dino in dinos:
                    # Check for collisions
                    if obstacle.collides(dino):
                        gen[dinos.index(dino)].fitness -= 1
                        nets.pop(dinos.index(dino))
                        gen.pop(dinos.index(dino))
                        dinos.pop(dinos.index(dino))

                    dino.draw(self.screen)

                if obstacle.X + CACTUS_THICC < dino.X:
                    reward = True

                obstacle.update()
                obstacle.draw(self.screen)

            if obstacles[0].X < -120:
                obstacles.popleft()
            if obstacles[-1].X < WIN_WIDTH - (random.randint(3, 10) * CACTUS_WIDTH):
                if random.randint(0, 1):
                    obstacles.append(Cacti(WIN_WIDTH))
                else:
                    obstacles.append(Fly(WIN_WIDTH))

            if reward:
                # give more reward for avoiding an obstacle
                for genome in gen:
                    genome.fitness += 5

            pygame.display.update()

            self.clock.tick(FPS)

        obstacles.clear()

    def run(self):
        """
        Runs the NEAT algorithm to train a neural network to play our game.

        :return: None
        """
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                    self.config_file)

        # Create the population, which is the top-level object for a NEAT run.
        p = neat.Population(config)

        # Add a stdout reporter to show progress in the terminal.
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)

        # Run for up to 30 generations.
        winner = p.run(self.eval_genome, 30)

        # Save the winner.
        with open('winner', 'wb') as f:
            pickle.dump(winner, f)

        # show final stats
        print('\nBest genome:\n{!s}'.format(winner))


def AIstart():
    new_game = AIGame()
    new_game.run()
    pygame.display.set_mode(SIZE)