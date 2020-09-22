import sys
import socket

def read_words() -> list:
	"""
	Return list of words from the words.txt file.
	"""
	words = []
	file = open("words.txt") 
	word = file.readline()
	while word:
		word = word.strip()

		words.append(word)
		word = file.readline()
	return words


begin_string = """

    In this tricky game we have randomized a word out of a given wordlist.
    Your job is to guess that word.
    On each guess we will provide you number of characters you were correct with,
    without any indication upon what characters or their position.
    You have multiple limitations though:
    - On each run a new word is randomized.
    - You have 15 tries.
    - We are limiting the connection to 30 seconds.

    To block bruteforce we will show you the next cat and wait...
                                _
                               | \
                               | |
                               | |
         |\                    | |
        /, ~\                 / /
        X     `-.....-------./ /
        ~-. ~  ~              |
           \             /    |    <------------- Louie The Cat
            \  /_     ___\   /
            | /\ ~~~~~   \ |
            | | \        || |
            | |\ \       || )
           (_/ (_/      ((_/

    GO !
"""

port = 2222

class Netcat:
    """ Python 'netcat like' module """

    def __init__(self, ip, port):

        self.buff = ""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((ip, port))

    def read(self, length = 1024):

        """ Read 1024 bytes off the socket """

        return self.socket.recv(length)
 
    def read_until(self, data):

        """ Read data into the buffer until we have data """

        while not data in self.buff:
            self.buff += self.socket.recv(1024)
 
        pos = self.buff.find(data)
        rval = self.buff[:pos + len(data)]
        self.buff = self.buff[pos + len(data):]
 
        return rval
 
    def write(self, data):

        self.socket.send(data)
    
    def close(self):

        self.socket.close()

server = Netcat("0.0.0.0", 2222)
while True:
    data = server.read()
    if data:
        print(data)