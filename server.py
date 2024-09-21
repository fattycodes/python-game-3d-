from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3
from direct.task import Task
import socket
import threading
import pickle

class GameServer(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.players = {}  # Dictionary to store player data

        # Start the server thread
        threading.Thread(target=self.start_server, daemon=True).start()

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 12345))
        server_socket.listen(5)

        while True:
            client_socket, addr = server_socket.accept()
            print(f'Connection from {addr}')
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                player_data = pickle.loads(data)
                self.players[client_socket] = player_data
                self.broadcast_players()
            except:
                break

        client_socket.close()

    def broadcast_players(self):
        for player_socket in self.players:
            player_data = pickle.dumps(self.players)
            player_socket.send(player_data)
    def broadcast_players(self):
    # Create a dictionary of all player states
     all_players_data = {str(player_socket): player_data for player_socket, player_data in self.players.items()}
     for player_socket in self.players:
        player_data = pickle.dumps(all_players_data)
        player_socket.send(player_data)


# Run the server
server = GameServer()
server.run()
