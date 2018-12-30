#--------------ROV 2018 CONTROL PROGRAM--------------#

#import modules
import pygame
import math as m
import numpy as np
import time
from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants

#initialize pygame
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

#open socket for control board
board = PyMata3(ip_address = '192.168.0.177', ip_port=3030, ip_handshake='')

#arrays and constants
address = [42, 43, 44, 45, 46, 47]
max_throttle = [5000, 7500, 15000, 20000, 25000, 30000]
t = [0] * 6
last_t = [0] * 6
delta = [0] * 6
throttle = [0] * 6
dead_rad = 0.1
pi = m.pi
shift_count = 0
last_shift = 0
max_accel = 0.125
release_pin = 9

#arm ESCs
board.i2c_config(0)
for i in range (0, 6):
    board.i2c_write_request(address[i], [0, 0, 0])

board.set_pin_mode(release_pin, Constants.OUTPUT)

#main loop
while True:

        #read joystick
        pygame.event.get()

        #store values
        jx = joystick.get_axis(0)
        jy = -joystick.get_axis(1)
        jz = joystick.get_axis(3)
        up = -joystick.get_axis(2)
        turn = joystick.get_button(6)
        shift = joystick.get_button(10)
        release = joystick.get_button(0)

        #apply circular dead zone with radius = dead_rad
        if (jx)**2 + (jy)**2 < (dead_rad)**2:
            jx = 0
            jy = 0
        else:
            jx = jx
            jy = jy

        #find primary and secondary motor speeds (a and b)
        theta_j = m.atan2(jy, jx) + pi
        index = int(theta_j/(pi/4))

        while theta_j > pi/2:
            theta_j = theta_j - pi/2

        theta_t = abs(theta_j - pi/4)

        if abs(jx) >= abs(jy):
            a = abs(jx)
        else:
            a = abs(jy)

        b = a * m.tan(theta_t)

        #find throttle for each thruster
        seq = [-b, b, a, a, b, -b, -a, -a]

        if turn == 0:    
                #CHANGE NEGATIVE SIGNS AFTER REWIRING!!! - ALL OF THESE WOULD NORMALLY BE POSITIVE
                t[0] = -seq[index]
                t[1] = seq[(index+2)%8]
                t[2] = seq[(index+4)%8]
                t[3] = -seq[(index+6)%8]
                t[4] = up
                t[5] = up
        if turn == 1:
                #CHANGE NEGATIVE SIGNS AFTER REWIRING!!! - t[0] AND t[2] WOULD NORMALLY BE NEGATIVE
                t[0] = -jz
                t[1] = -jz
                t[2] = jz
                t[3] = jz
                t[4] = up
                t[5] = up

        #toggle max throttle multiplier on button press
        if shift == 1 and last_shift == 0:
            shift_count += 1
            
        multiplier = max_throttle[shift_count%len(max_throttle)]
        
        last_shift = shift

        #limit acceleration, apply multiplier, and send I2C command
        
        for i in range (0, 6):
            delta[i] = t[i] - last_t[i]

            if delta[i] > (max_accel):
                delta[i] = max_accel
            if delta[i] < (-max_accel):
                delta[i] = -max_accel

            t[i] = last_t[i] + delta[i]
            last_t[i] = t[i]

            throttle[i] = int(t[i] * multiplier)
            board.i2c_write_request(address[i], [0, throttle[i]>>8, throttle[i]])

        if release == 0:
            board.digital_write(release_pin, 0)
            board.sleep(0.5)
        if release == 1:
            board.digital_write(release_pin, 1)
            board.sleep(0.5)
            
        board.sleep(0.1)
        
        print (throttle)
