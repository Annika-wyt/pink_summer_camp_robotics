import fleetmqsdk
from threading import Thread, Event
import time
import struct
import numpy as np
import json
from copy import deepcopy

class fleetmqClass:
    def __init__(self, **kwargs):
        self.fleetmq = fleetmqsdk.FleetMQ()

        config, addresses = self.fleetmq.getConfig(True)    
        # print("Received config and addresses!")

        self.delimiter = b"|abc|"

        self.subscribeTopic = ['fmq/remote_control']

        self.opposites = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left"
        }

        self.stop_event = Event()

        self.threads = []

        self.vx = 0
        self.vy = 0
        self.direction = 0
        self.action = "right"
        self.boundary = 0.7

        self.debug = False
        subscribThread = Thread(target=self.subscribeMap, args=(self.subscribeTopic))
        subscribThread.daemon = True
        subscribThread.start()
        self.threads.append(subscribThread)

    def subscribeMap(self, topic):
        while not self.stop_event.is_set():  
            raw_msg = self.fleetmq.receiveBytes(topic)
            if raw_msg != None:
                try:
                    parts = json.loads(raw_msg.split(self.delimiter)[1].decode('utf-8'))
                    self.vx = parts["vx"]
                    self.vy = parts["vy"]
                    # direction = self.vy/np.linalg.norm(np.sqrt(self.vx**2 + self.vy**2))
                    # if direction <= -self.boundary:
                        # self.action = "left" if "left" != self.opposites[self.action] else self.action
                    # elif direction >= self.boundary:
                        # self.action = "right" if "right" != self.opposites[self.action] else self.action
                    # elif self.vx <= 0 and abs(direction) < self.boundary:
                        # self.action = "down" if "down" != self.opposites[self.action] else self.action
                    # elif self.vx >= 0 and abs(direction) < self.boundary:
                        # self.action = "up" if "up" != self.opposites[self.action] else self.action
                    if self.vy <= -self.boundary:
                        self.action = "left" if "left" != self.opposites[self.action] else self.action
                    elif self.vy >= self.boundary:
                        self.action = "right" if "right" != self.opposites[self.action] else self.action
                    if self.vx <= -(1-self.boundary):
                        self.action = "down" if "down" != self.opposites[self.action] else self.action
                    elif self.vx >= 1-self.boundary:
                        self.action = "up" if "up" != self.opposites[self.action] else self.action
                except Exception as e:
                    print(f"Error from subscribe: {e}")

    def getAction(self):
        return self.action
    
def main():
    fmq = fleetmqClass()
    while True:
        try:
            pass
        except KeyboardInterrupt:
            fmq.threads.stop()
            break


if __name__ == "__main__":
    main()