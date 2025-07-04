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


stop_event = Event()

class remote_control():
    def __init__(self, end):
        self.fleetmq = fleetmqsdk.FleetMQ()

        config, addresses = self.fleetmq.getConfig(True)    
        print("Received config and addresses!")

        self.state = np.array([None, None, None], dtype=np.float32)
        self.map = None

        self.debug = False
        self.end = end #(38, 53)

        self.delimiter = b"|abc|"

        self.ready_for_astar_counter = 0
        self.reso = 0
        self.origin = None


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
                    parts = raw_msg.split(b"|")
                    x, y, yaw = struct.unpack_from('<ddd', parts[2][-24:])
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
                    parts = raw_msg.split(b"|")
                    self.reso, width, height, origin_x, origin_y = struct.unpack_from('<fII dd', parts[2], 27)
                    self.origin = (origin_x, origin_y)
                    data_len = struct.unpack_from('<I', parts[2][95:99])[0]
                    self.map = list(struct.unpack_from(f'<{data_len}b', parts[2][99:]))
                    self.map = np.array(self.map).reshape((height, width)).tolist()
                    if self.debug:
                        print(f"Received msg: Resolution: {self.reso}, Map: {self.map[-1][-10:]}")
                except Exception as e:
                    print(f"Error from subscribe Map: {e}")

    def publishPath(self, topic):
        while not stop_event.is_set():  
            if self.state.any() != None and self.reso != 0 and self.map != None:
                try:
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
                    self.fleetmq.publishBytes(topic, payload)
                    if self.debug:
                        print(f"payload: {payload}")
                except Exception as e:
                    print(f"Error from publish Path: {e}")

                time.sleep(1)

def main(args=None):
    parser = argparse.ArgumentParser(description='FMQ Remote Path Planner')
    parser.add_argument('--end', type=str_to_tuple, help="End point as 'x,y'")
    args = parser.parse_args()
    remote_control(args.end)

def str_to_tuple(s):
    try:
        x, y = map(float, s.split(','))
        return (x, y)
    except:
        raise argparse.ArgumentTypeError("Must be in the form 'x,y'")

if __name__ == '__main__':
    main()