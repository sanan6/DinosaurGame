import socket
from _thread import start_new_thread
import pickle
import time
from settings import *


class Server(object):
    """
    The class for hosting a game server.
    """
    def __init__(self, address, port, server_size):
        """
        Initialize a server object.

        :param address: local ip address of the server machine
        :param port: port to open the server on
        :param server_size: number of players expected
        """
        self.address = address
        self.port = port
        self.server_size = server_size
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.players = []  # list to contain current data of all players
        self.running_threads = 0
        self.game_started = 0

    def threaded_client(self, conn, player_id):
        """
        Handle communication with one client.

        :param conn: socket object corresponding to the client
        :param player_id: unique identifier of the player
        :return: None
        """
        conn.sendall(pickle.dumps([self.server_size]))
        print("Connected")
        while not self.game_started:
            if self.server_size-self.running_threads == 0:
                time.sleep(1)
                self.game_started = 1
            data = pickle.loads(conn.recv(2048))
            conn.sendall(pickle.dumps(self.make_packet(player_id)))
        while True:
            try:
                data = pickle.loads(conn.recv(2048))
                self.players[player_id] = data

                if not data:
                    print("Disconnected")
                    break

                conn.sendall(pickle.dumps(self.make_packet(player_id)))
            except:
                break

        print("Lost connection")
        conn.close()
        self.running_threads -= 1

    def run(self):
        """
        Start the server.

        :return: None
        """
        try:
            self.soc.bind((self.address, self.port))
        except socket.error as e:
            str(e)

        self.soc.listen(SERVER_SIZE)
        print("Waiting for a connection, Server Started")

        current_player = 0

        while True:
            if current_player < self.server_size:
                connection, address = self.soc.accept()
                print("Connected to:", address)
                self.players.append(-1)

                start_new_thread(self.threaded_client, (connection, current_player))
                self.running_threads += 1
                current_player += 1
            elif self.running_threads == 0:
                break

    def make_packet(self, player_id):
        """
        Create information packet to be sent to a client.

        :param player_id: identifier of the recipient player
        :return: the created packet
        """
        player_data = []
        for i in range(self.running_threads):
            if player_id != i:
                player_data.append(self.players[i])
        return [self.game_started, self.server_size-self.running_threads, player_data]


if __name__ == '__main__':
    while True:
        server = Server(address=SERVER_ADDRESS, port=PORT, server_size=SERVER_SIZE)
        server.run()