import socket


class Server:
    """ The host or 'server' for the esp32.

        Takes 3 arguments:\n
        list_of_animals, a list of the animals that need to be tracked.\n
        host_ip, the (string) ip of the host/server (where this code is ran)\n
        host_port, the port to create the socket on."""

    def __init__(self, list_of_animals, host_ip, host_port):
        self.socket = socket.socket()
        self.host = host_ip
        self.port = host_port
        self.socket.bind((self.host, self.port))
        self.conn = ''
        self.list_of_animals = list_of_animals
        self.list_of_devices = []
        self.last_message = ''

    def establish_connection(self):
        """ Listens for a connection.
        """
        print('Listening...')
        self.socket.listen()
        self.conn, addr = self.socket.accept()
        print('Received connection', addr)

    def receive_data(self, conn):
        """Receive and process initial data (requires a connection before running.)"""
        data = conn.recv(2048)
        message = data.decode('utf-8')
        currDev = ''
        if message != self.last_message and message != '':
            if len(message) >= 24:
                for letter in message:
                    currDev += letter
                    if len(currDev) == 12:
                        self.list_of_devices += [currDev]
                        currDev = ''
            else:
                self.list_of_devices = [message]
        print(self.list_of_devices)

    def run_server(self):
        """ run_server runs the server... (makes a connection and loops receive_data())"""
        self.establish_connection()
        while True:
            self.receive_data(self.conn)


list_of_animals = []
server1 = Server(list_of_animals, '192.168.137.1', 8003)
if __name__ == "__main__":
    server1.run_server()
