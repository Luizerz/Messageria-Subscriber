
import stomp 
import json 
from time import sleep


class Client() :
    def __init__(self, id: str, callback, position: int): 
        self.conn = stomp.Connection()
        self.callback = callback
        self.connect()
        self.connected = True
        self.listener()
        self.subscribe('/topic/sensor' + id)
        self.data = None
        self.position = position
        while self.connected:
            sleep(0)

    def connect(self): 
        self.conn.connect('admin', 'password', wait=True)
    def disconnect(self): 
        self.conn.disconnect()
    def subscribe(self, destination: str):
        self.conn.subscribe(destination = destination, id = 1, ack='auto')
    def listener(self):
        self.conn.set_listener('', self.ClientInner(self))
        
    class ClientInner(stomp.ConnectionListener):
        def __init__(self, client):
            self.client = client
        def on_error(self, frame):
            print('received an error "%s"' % frame.body)

        def on_message(self, frame):
            self.client.data = json.loads(frame.body)
            self.client.callback(self.client.data, self.client)
