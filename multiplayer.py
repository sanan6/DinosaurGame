import pygame
import socket
import pickle
import sys
import random
from pygame.locals import *
from game_engine import Game
from dinosaur import Dinosaur
from environment import Cacti
from settings import *

class MultiplayerGame(Game):
    def __init__(self):
        super().__init__()
        self.connection = Network(SERVER_ADDRESS, PORT)
        self.other_players = []
        self.num_other_players = self.connection.first_packet[0] - 1
        self.seed_gen = seed_generator(self.connection.first_packet[1])
        for i in range(self.num_other_players):
            self.other_players.append(Dinosaur(other=True))
        self.obstacles.pop()
        self.obstacles.append(Cacti(WIN_WIDTH))

    def events(self):
        """
        Manages the user inputs

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

    def game_main(self):
        """
        Main function of multiplayer game.

        :return: None
        """

        while True:
            self.events()

            # Update object positions and check for collisions
            if self.started:
                player_data = self.connection.send(self.dino.Y)[2]
                for i in range(self.num_other_players):
                    self.other_players[i].Y = player_data[i]

                self.dino.update()
                self.update_obstacles(next(self.seed_gen))
                if any([pipe.collides(self.dino) for pipe in self.obstacles]):
                    self.game_over()
                    break
                self.slower_score += 1
                if self.slower_score > 5:
                    self.score += 1
                    self.slower_score = 0

            self.screen.blit(self.background, (0, 0))
            for player in self.other_players:
                player.draw(self.screen)
            self.dino.draw(self.screen)
            assert isinstance(self.obstacles, object)
            for obstacle in self.obstacles:
                obstacle.draw(self.screen)

            score_message = self.game_font.render(str(self.score), True, (0, 0, 0))
            self.screen.blit(score_message, (WIN_WIDTH / 2 - score_message.get_width() / 2, 20))

            if not self.started:
                packet = self.connection.send(self.dino.Y)
                self.started = packet[0]
                needed_players = packet[1]
                server_message = self.game_font.render(str(needed_players) + " more player needed", True, (0, 0, 0))
                self.screen.blit(server_message, (WIN_WIDTH / 2 - server_message.get_width() / 2, 50))

            pygame.display.update()

            self.clock.tick(FPS)

def seed_generator(seed):
    """
    Generate random ints.

    :return: generated random int
    """
    random.seed(seed)
    while True:
        yield random.randint(-41369, 41269)

class Network:
    """
    Class to handle network communication.
    """
    def __init__(self, server, port):
        """
        Initialize a connection with the server.

        :param server: ip address of the server
        :param port: port where the game is hosted
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.target_address = (self.server, self.port)
        self.client.settimeout(10)
        self.first_packet = self.connect()

    def connect(self):
        """
        Connect to target server.

        :return: First packet sent by server.
        """
        try:
            self.client.connect(self.target_address)
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print("Socket error: ", e)
            raise

    def send(self, data):
        """
        Send data in a serialized form to server, and receive response packet.

        :param data: data to be serialized and sent
        :return: response packet sent by the server
        """
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print("Socket error: ", e)

def multiplayer_run():
    """
    This is called when we push the multiplayer button. It initiates the game.

    :return: None
    """
    game = MultiplayerGame()
    game.game_main()
    pygame.display.set_mode(SIZE)
