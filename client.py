from direct.showbase.ShowBase import ShowBase
import socket
import threading
import pickle
from panda3d.core import Vec3

class GameClient(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect(('localhost', 12345))
        self.player_data = {'position': Vec3(0, 0, 0)}
        threading.Thread(target=self.listen_server, daemon=True).start()

    def listen_server(self):
        while True:
            data = self.server_socket.recv(1024)
            players = pickle.loads(data)
            print(players)  # Handle player data

    def update_player(self):
        # Update player data and send to server
        self.player_data['position'] += Vec3(1, 0, 0)  # Example movement
        data = pickle.dumps(self.player_data)
        self.server_socket.send(data)
    
# Run the client
if __name__ == "__main__":
    client = GameClient()
    client.run()
