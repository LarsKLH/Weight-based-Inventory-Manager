import pyfirmata2 as pf2
import time
import numpy as np
import customtkinter as ctk
import datetime
import threading as th
import sqlite3

pin_map = {0 : 'stethoscope',
    1 : 'otoscope',
    2 : 'syringe',
    3 : 'scalpel',
    4 : 'gloves',
    5 : 'bandages'}





if __name__ == "__main__":    
    pass
    

"""
class AnalogPin:
    def __init__(self, sr):
        port = '/dev/ttyACM0'
        self.samplingRate = sr # sampling rate in Hz
        self.timestamp = 0
        self.board = pf2.Arduino(port)

        for i in range(6):
            self.board.analog[i].mode = pf2.INPUT
            #self.board.analog[i].enable_reporting()

        self.samples = [[] for i in range(6)]
        
    def start(self):
        self.board.analog[0].register_callback(self.Callback)
        self.board.samplingOn(1000 / self.samplingRate)
        for i in range(6):
            self.board.analog[i].enable_reporting()

    def Callback(self, data):
        self.samples[0].append(data)
        for i in range(1, 6):
            self.samples[i].append(self.board.analog[i].read())

        print("%f,%f" % (self.timestamp, data))
        self.timestamp += (1 / self.samplingRate)

    def stop(self):
        self.board.exit()
        #medians = [np.median(i) for i in self.samples]
        #return medians
        return [100 for i in range(6)] #returning 100 for testing purposes


"""
