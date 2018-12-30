
from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants

import pygame
import math

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

BOARD_LED = 8
board = PyMata3(ip_address = '192.168.0.177', ip_port=3030, ip_handshake='')

DEVICE1_ADDRESS = 42
DEVICE2_ADDRESS = 43
DEVICE3_ADDRESS = 44
DEVICE4_ADDRESS = 45
DEVICE5_ADDRESS = 46
DEVICE6_ADDRESS = 47

THROTTLE1 = 5000
THROTTLE2 = 10000
THROTTLE3 = 15000
 
pi = math.pi
dead = 0.1

shiftcount = 1

def setup():
    
    board.i2c_config(0)
    print("initialize the motor")
    board.i2c_write_request(DEVICE1_ADDRESS, [0, 0,  0])
    board.i2c_write_request(DEVICE2_ADDRESS, [0, 0,  0])
    board.i2c_write_request(DEVICE3_ADDRESS, [0, 0,  0])
    board.i2c_write_request(DEVICE4_ADDRESS, [0, 0,  0])
    board.i2c_write_request(DEVICE5_ADDRESS, [0, 0,  0])
    board.i2c_write_request(DEVICE6_ADDRESS, [0, 0,  0])
    board.sleep(2.0)

setup()

while True:

    pygame.event.get() #don't forget this

    jx = joystick.get_axis(0)
    jy = -joystick.get_axis(1)
    jz = joystick.get_axis(3)

    up = -joystick.get_axis(2)

    turn = joystick.get_button(6)
    shift = joystick.get_button(10) 

    #dead zone is circle with radius = dead
    if ((jx)**2 + (jy)**2) >= (dead)**2:
        jx = jx
        jy = jy
    else:
        jx = 0
        jy = 0

    if (abs(jz) >= dead):
        jz = jz
    else:
        jz = 0

    #angle referenced to positive x-axis
    if (jx > 0) and (jy > 0):
        theta_j = math.atan(jy / jx)
    elif (jx < 0):
        theta_j = math.atan(jy / jx) + pi
    elif (jx > 0) and (jy < 0):
        theta_j = math.atan(jy / jx) + (2 * pi)
    elif (jx == 0):
        if (jy > 0):
            theta_j = pi/2
        elif (jy < 0):
            theta_j = 3*pi/2
        elif (jy == 0):
            theta_j = 0

    #angle to the nearest diagonal axis
    if (0 <= theta_j < pi/2):
        theta_t = abs(pi/4 - theta_j)
    elif (pi/2 <= theta_j < pi):
        theta_t = abs(3*pi/4 - theta_j)
    elif (pi <= theta_j < 3*pi/2):
        theta_t = abs(5*pi/4 - theta_j)
    elif (3*pi/2 <= theta_j < 2*pi):
        theta_t = abs(7*pi/4 - theta_j)

    #vector sum of a and b adds up to j/jmax
    if (abs(jx) >= abs(jy)):
        a = abs(jx)
        b = abs(jx * math.tan(theta_t))
    elif (abs(jx) < abs(jy)):
        a = abs(jy)
        b = abs(jy * math.tan(theta_t))

    #probably not necessary
    if (b < 0.01):
        b = 0

    if (turn == 1):
        if jz >= 0:
            m1 = -jz
            m2 = jz
            m3 = -jz
            m4 = jz
        if jz < 0:
            m1 = jz
            m2 = -jz
            m3 = jz
            m4 = -jz

    if (turn == 0):
        if 0 <= theta_j <= pi/4:
            m1 = -b
            m2 = a
            m3 = b
            m4 = -a

        if pi/4 < theta_j <= pi/2:
            m1 = b
            m2 = a
            m3 = -b
            m4 = -a

        if pi/2 < theta_j <= 3*pi/4:
            m1 = a
            m2 = b
            m3 = -a
            m4 = -b

        if 3*pi/4 < theta_j <= pi:
            m1 = a
            m2 = -b
            m3 = -a
            m4 = b

        if pi < theta_j <= 5*pi/4:
            m1 = b
            m2 = -a
            m3 = -b
            m4 = a

        if 5*pi/4 < theta_j <= 3*pi/2:
            m1 = -b
            m2 = -a
            m3 = b
            m4 = a

        if 3*pi/2 < theta_j <= 7*pi/4:
            m1 = -a
            m2 = -b
            m3 = a
            m4 = b

        if 7*pi/4 < theta_j <= 2*pi:
            m1 = -a
            m2 = b
            m3 = a
            m4 = -b
            
    if abs(up) <= dead:
        up = 0
    else:
        up = up
        
    m5 = up
    m6 = up

    if (shift == 1 and prevshift == 0):
        switch = 1
    else:
        switch = 0

    if switch == 1:
        shiftcount = shiftcount + 1
    else:
        shiftcount = shiftcount

    if shiftcount == 4:
        shiftcount = 1

    if shiftcount == 1:
        max_throttle = THROTTLE1
    if shiftcount == 2:
        max_throttle = THROTTLE2
    if shiftcount == 3:
        max_throttle = THROTTLE3

    prevshift = shift

    write1 = -int(m1*max_throttle)
    write2 = int(m2*max_throttle)
    write3 = int(m3*max_throttle)
    write4 = int(m4*max_throttle)
    write5 = -int(m5*max_throttle)
    write6 = -int(m6*max_throttle)

    print(write1, write2, write5)
    
    
    board.i2c_write_request(DEVICE1_ADDRESS, [0, write1>>8,  write1])
    board.i2c_write_request(DEVICE2_ADDRESS, [0, write2>>8,  write2])
    board.i2c_write_request(DEVICE3_ADDRESS, [0, write3>>8,  write3])
    board.i2c_write_request(DEVICE4_ADDRESS, [0, write4>>8,  write4])
    board.i2c_write_request(DEVICE5_ADDRESS, [0, write5>>8,  write5])
    board.i2c_write_request(DEVICE6_ADDRESS, [0, write6>>8,  write6])
            

    
        
        

    
