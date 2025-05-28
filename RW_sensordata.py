#!/usr/bin/env python3
import serial
import Systemlogger_module as slog
import sqlite3
from datetime import datetime as dt
#import keyboard
import serial
import select
import sys
import time
import os


item_map = {
    0:'Mini-Spike Filter',
    1: 'Clear Sight Wipe',
    2: 'Syringe'
    }


def read_sensordata():
    #try:
     #   keyboard.add_hotkey('shift+c', lambda: ser.write('c'.encode()))
      #  keyboard.add_hotkey('shift+t', lambda: ser.write('t'.encode()))
       # keyboard.add_hotkey('shift+n', lambda: ser.write('n'.encode()))
        #keyboard.add_hotkey('shift+r', lambda: ser.write('r'.encode()))
        #keyboard.add_hotkey('shift+y', lambda: ser.write('y'.encode()))
        #keyboard.add_hotkey('shift+1', lambda: ser.write('1'.encode()))
        #keyboard.add_hotkey('shift+2', lambda: ser.write('2'.encode()))
        #keyboard.add_hotkey('shift+3', lambda: ser.write('3'.encode()))
    #except Exception as e:
     #   print(f'Exception raised: {e}')

    log.add("Reading data from serial port...")
    flag = False
    avg = [[],[],[]]
    liste = []
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    f = open("Kalibreringsfaktorer.txt", "r")
    calfac = f.readline()
    f.close()
    b = 1
    k = 0
    while (k<10):
         if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            input_str = sys.stdin.readline().strip()
            ser.write(input_str.encode())
        if ser.in_waiting > 0:
            line = ser.readline().decode('ascii').rstrip() # Hver datalinje eks "nr1 0.4" = id og vekt
            '''if line == "Starting...":
                ser.write('c'.encode())'''
            if "number" in line:
                ser.write(str(b).encode())
                b += 1
            '''if "Now" in line:
                ser.write(calfac[b-1].encode())
            if "EEPROM" in line:
                ser.write('n'.encode())'''
            try:
                liste = line.split()
                print(liste)
                if liste[0] == "data":
                    avg[int(liste[1])].append(float(liste[2]))
                    k += 1
            except Exception as e:
                flag = True
                print(f"Exception raised: {e}")
                print(ser.readline().decode('ascii').rstrip())
                continue
            
    ser.close()

    vekt = [sum(i)/len(i) for i in avg] # tar gjennomsnittet av de gjennomsnittlige vektene
    if not flag:
        log.add("Data read successfully.")
    else:
        log.add("Error in reading data from the serial port.")

    log.addp("Data: ")
    for i,l in enumerate(vekt):
        log.addp(f"{item_map[i]}: {l} ")
    
    #print(vekt, flag)
    return vekt, flag

def write_sensordata(line):
    log.addp("writing to database...")
    database_path = 'Storage_solution_DB.db'
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        action = '''
            UPDATE Storage
            SET tot_weight = ?
            WHERE storage_id = ?
        '''
        for i,l in enumerate(line):
            cursor.execute(action, (l, item_map[i]))

        conn.commit()
        #conn.close()
    log.add("Writing completed.")
        

def print_table():
    with sqlite3.connect('Storage_solution_DB.db') as conn:
        cursor = conn.cursor()
        action = '''
            SELECT * FROM Storage
        '''
        cursor.execute(action)
        for row in cursor.fetchall():
            print(row)
        

if __name__ == "__main__":
    logname = "Sensorsystemlog"
    filename = "RW_sensordata.py"
    log = slog.logger(logname + ".log")
    log.add(filename + " started " + dt.now().strftime('%Y-%m-%d %H.%M.%S'))
    log.add(60*"-")

    line, flag = read_sensordata()
    if not flag:
        write_sensordata(line)
    else:
        print("Error in reading data from the serial port.")

    #print_table()
    
    
