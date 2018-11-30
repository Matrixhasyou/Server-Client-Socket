import socket
import datetime
from threading import Thread
import json

class Server:
    """
        SERVER (set HOST, set PORT)
        by default: localhost:10000 listen 5
    """
    def __init__(self, host="127.0.0.1", port=10000, listen=5):
        self.host = socket.gethostbyname(host)
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                  #Set socket
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)                #Socket reuses same addr, without waiting for time out
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(listen)
            
    def __str__(self):
        return "Server started at {}:{}".format(self.host, self.port)
        
    def start_server(self):
        """
            Main function that starts server
        """
        print(self)
        print("Waiting for clients...")
        while True:
            connection, address = self.server_socket.accept()
            ip, port = str(address[0]), str(address[1])
            print("Connected with " + ip + ":" + port)
            try:
                Thread(target=self.client_thread, args=[connection,]).start()                   #start thread of client_tread
            except:
                print("Thread did not start.")

    def client_thread(self, conn):
        """
            func that contains CLIENT THREAD and listen to it
        """
        while True:
            client_input, print_input = self.get_client_input(conn)                             #get json from client          
            if client_input != None:
                print(print_input)
                msg = self.set_msg(client_input["id"])
                serialized = json.dumps(msg, ensure_ascii=False).encode("utf-8")                #send json to client
                conn.sendall(serialized)

    def get_client_input(self, conn):
        """
            helper func to read and deserialized JSON data
            *need improvemen, may leak for long json*
        """       
        data = conn.recv(2048)
        try:
            deserialized = json.loads(data.decode('utf-8'))
        except (TypeError, ValueError):
            return None, None
        return deserialized, "Client #{1} reply: {0}".format(str(deserialized), str(deserialized["id"]))

    def set_msg(self, client_id):
        """
            func that builds server reply
        """
        return {"id": client_id,
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d T%H:%M:%S.%f")}

if __name__ == "__main__":
    
    #Start server
    server = Server(listen=4)
    server.start_server()
