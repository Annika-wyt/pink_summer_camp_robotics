#!/usr/bin/env python

import fleetmqsdk
import argparse
import atexit
import signal
import socket
import time
import sys
import struct
from threading import Thread, Event
from pathplanning import astar
import numpy as np
from io import BytesIO
import struct
import json


stop_event = Event()

class remote_control():
    def __init__(self):
        self.fleetmq = fleetmqsdk.FleetMQ()

        config, addresses = self.fleetmq.getConfig(True)    
        print("Received config and addresses!")

        self.state = np.array([None, None, None], dtype=np.float32)
        self.map = None

        self.debug = False
        self.end = None

        self.delimiter = b"|abc|"

        self.ready_for_astar_counter = 0
        self.reso = 0
        self.origin = None

        self.sent_path = False

        threads = []
        publishPath = ["fmq/path"]
        subscribeMap = ["svea/map"]
        subscribeState = ["svea/state"]

        publishpath_thread = Thread(target=self.publishPath, args=(publishPath))
        publishpath_thread.start()
        threads.append(publishpath_thread)

        subscribemap_thread = Thread(target=self.subscribeMap, args=(subscribeMap))
        subscribemap_thread.start()
        threads.append(subscribemap_thread)

        subscribestate_thread = Thread(target=self.subscribeState, args=(subscribeState))
        subscribestate_thread.start()
        threads.append(subscribestate_thread)
        
        # Keep main thread running until interrupt
        try:
            # Wait for all threads to complete
            while any(thread.is_alive() for thread in threads):
                for thread in threads:
                    thread.join(timeout=0.01)
        except KeyboardInterrupt:
            stop_event.set()
            print("\nShutting down...")
        
        self.fleetmq.close()

    def subscribeState(self, topic):
        while not stop_event.is_set():  
            raw_msg = self.fleetmq.receiveBytes(topic)
            if raw_msg != None:
                try:
                    parts = raw_msg.split(self.delimiter)
                    x, y, yaw = struct.unpack_from('<ddd', parts[1][-24:])
                    self.state = np.array([x, y, yaw], dtype=np.float32)
                    if self.debug:
                        print(f"Received msg: {self.state}")
                except Exception as e:
                    print(f"Error from subscribe State: {e}")

    def subscribeMap(self, topic):
        while not stop_event.is_set():  
            raw_msg = self.fleetmq.receiveBytes(topic)
            if raw_msg != None:
                try:
                    parts = raw_msg.split(self.delimiter)
                    # decoded = parts[1].decode("utf-8")    
                    decoded = json.loads(parts[1])
                    self.reso = decoded["reso"]
                    width = decoded["width"]
                    height = decoded["height"]
                    origin_x = decoded["origin_x"]
                    origin_y = decoded["origin_y"]
                    self.origin = (origin_x, origin_y)
                    self.map = decoded["data"]
                    self.map = np.array(self.map).reshape((height, width)).tolist()
                    if self.debug:
                        print(f"Received msg: Resolution: {self.reso}, Map: {self.map[-1][-10:]}")
                except Exception as e:
                    print(f"Error from subscribe Map: {e}")

    def publishPath(self, topic):
        while not stop_event.is_set():  
            if self.state.any() != None and self.reso != 0 and self.map != None:
                if self.sent_path:
                    new_end = input("Enter a new end point (e.g. 60,30), or type 'exit' to exit: ")
                    if new_end == "exit":
                        stop_event.set()
                        self.fleetmq.close()
                        exit()
                    self.end = str_to_tuple(new_end)
                    self.end = (int(self.end[1]), int(self.end[0]))
                    get_new_point = False
                    if self.map[self.end[0]][self.end[1]] > 0:
                        for i in range(self.end[0]-2, self.end[0]+2):
                            for j in range(self.end[1]-2, self.end[1]+2):
                                if self.map[i][j] == 0:
                                    get_new_point = True
                                    self.end = (i,j)
                                    break
                            if get_new_point:
                                break
                        if not get_new_point:
                            print(f"NOT VALID END POINTS, END POINT IN AN OBSTACLE")
                    elif self.map[self.end[0]][self.end[1]] == -1:
                        for i in range(self.end[0]-2, self.end[0]+2):
                            for j in range(self.end[1]-2, self.end[1]+2):
                                if self.map[i][j] == 0:
                                    get_new_point = True
                                    self.end = (i,j)
                                    break
                            if get_new_point:
                                break
                        if not get_new_point:
                            print(f"NOT VALID END POINTS, END POINT IN AN UNKNOWN PLACE")
                    if self.map[self.end[0]][self.end[1]] == 0:
                        self.sent_path = False
                        try:
                            if self.end != None:
                                start_x = int((self.state[1] - self.origin[1])/self.reso)
                                start_y = int((self.state[0] - self.origin[0])/self.reso)
                                start = (start_x, start_y)
                                traj = astar(self.map, start, self.end)
                                if self.debug:
                                    print(traj)
                                flat_traj = [val for pair in traj for val in pair]
                                data_len = len(flat_traj)
                                header = struct.pack('<III', 0, 0, data_len)
                                data_section = struct.pack(f'<{data_len}i', *flat_traj)
                                msg_bytes = header + data_section
                                payload = b"std_msgs/Int32MultiArray" + self.delimiter + msg_bytes
                                for i in range(2):
                                    self.fleetmq.publishBytes(topic, payload)
                                    time.sleep(0.1)
                                if self.debug:
                                    print(f"payload: {payload}")
                                if len(flat_traj) != 0:
                                    self.sent_path = True
                        except Exception as e:
                            print(f"Error from publish Path: {e}")
                self.sent_path = True
                time.sleep(1)
            

def main(args=None):
    remote_control()

def str_to_tuple(s):
    try:
        x, y = map(float, s.split(','))
        return (x, y)
    except:
        raise argparse.ArgumentTypeError("Must be in the form 'x,y'")

if __name__ == '__main__':
    main()