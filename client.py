import socket
import datetime, time
from threading import Thread
import json, struct
from uuid import uuid4 as uuid


class Client(Thread):
    """
        CLIENT (set ID, set HOST, set PORT, set WORKING TIME)
        by default: localhost:10000 sends 10 requests
    """
    def __init__(self, host="127.0.0.1", port=10000, working_time=10):
        self.client_id = str(uuid())
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.msg = {}
        self.work_for_sec = working_time
        
        Thread.__init__(self)                                                                       #init parent Thread
        self.daemon = True
        self.start()
        
    def __str__(self):
        return "Client #{} started.".format(self.client_id)
        
    def run(self):
        """
            Override thread func RUN()
        """
        print(self)
        self.client_socket.connect((self.host, self.port))
        while self.work_for_sec != 0:
            
            self.set_msg()
            serialized = json.dumps(self.msg, ensure_ascii=False).encode("utf-8")                   #send json to server
            self.client_socket.sendall(serialized)

            reply = self.get_server_input()                                                         #recieve json from server
            if reply != None:
                print(reply)

            time.sleep(1)                                                                           #wait for 1 sec                                )
            self.work_for_sec -= 1
        self.client_socket.close()
            
    def get_server_input(self):
        """
            helper func to read and deserialized JSON data
            *need improvemen, may leak for long json*
        """  
        data = self.client_socket.recv(2048)
        try:
            deserialized = json.loads(data.decode('utf-8'))
        except (TypeError, ValueError):
            return None
        
        return "Server reply: {}".format(str(deserialized))

    def set_msg(self):
        """
            func that builds JSON message for server
        """
        self.msg = {"id": self.client_id,
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d T%H:%M:%S.%f")}
    
if __name__ == '__main__':
    # Start num_of_clients Client threads
    num_of_clients = 5
    clients = [Client() for _ in range(num_of_clients)]
