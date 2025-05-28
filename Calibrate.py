#!/usr/bin/env python3
import serial
import select
import sys
import time
import os

weight = 500

def calibrate():

    flag = True
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    i = 1
    string =''
    splitt = []
    k = 0
    while (k < 3):
     #       line = ser.readline().decode('ascii').rstrip()
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            input_str = sys.stdin.readline().strip()
            ser.write(input_str.encode())
        if ser.in_waiting > 0:
            line = ser.readline().decode('ascii').rstrip()
            print(line)
            try:    
                splitt = line.split()
                if "New" in line:
                    string += str(splitt[-1])
                    string += '\n'
                    k += 1
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(f"Exception: {e}", exc_tb.tb_lineno)
                time.sleep(1)
    ser.close()
    f = open("Kalibreringsfaktorer.txt", "w")
    f.write(string)
    f.close()
    

if __name__ == '__main__':
    calibrate()
