import socket


class Server:
    def __init__(self, list_of_animals):
        self.socket = socket.socket()
        self.port = 7002
        self.host = '192.168.137.1'
        self.list_of_animals = list_of_animals
        self.list_of_devices = ''
        self.last_message = ''
        self.conn = ''
        self.escaped = {}
    
    def establish_connection(self):
        self.socket.bind((self.host, self.port))
        print('Listening...')
        self.socket.listen()
        self.conn, addr = self.socket.accept()
        data = self.conn.recv(2048)
        message = data.decode('utf-8')
        currDev = ''
        # Because we receive one long string, it needs to be split up into a list of devices.
        if len(message) >= 24:
            for letter in message:
                currDev += letter
                if len(currDev) == 12:
                    self.list_of_devices += [currDev]
                    currDev = ''
        else:
            self.list_of_devices = [message]
        self.last_message = message
        print(self.list_of_devices)

    def start(self):
        self.establish_connection()


if __name__ == '__main__':
    list_of_animals = ['44e69ef39342'] 
    while True:
        Server0 = Server(list_of_animals)
        Server0.start()
        print('Done!')
