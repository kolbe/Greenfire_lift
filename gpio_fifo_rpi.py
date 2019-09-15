#!/usr/bin/python
import RPi.GPIO as gpio
import time
import os
import select
import atexit

FIFO = "/var/run/gpio.fifo"

usage = '''
  Creates and reads from a fifo to receive limited GPIO commands.
'''

up = 17 #"LCD-CLK"
down = 18 #"LCD-D23"

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

gpio.setup(up, gpio.OUT, initial=1)
gpio.setup(down, gpio.OUT, initial=1)

def send(cmd):
   gpio.output(cmd, gpio.LOW)
   time.sleep(.3)
   gpio.output(cmd, gpio.HIGH)

@atexit.register
def cleanup():
    try:
        os.unlink(FIFO)
    except:
        pass

os.setegid(116)
os.umask(0000)

def main():
    os.mkfifo(FIFO)
    while True:
        with open(FIFO) as fifo:
           line = fifo.readline().rstrip()
           print repr(line)
           if line == "u":
              send(up)
           elif line == "d":
              send(down)
           elif line == "q":
              exit()
           fifo.close()

main()
