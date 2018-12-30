
#!/usr/bin/python
"""
  I2C Protocol

    The I2C communication protocol allows two-directional communication with the ESC. The protocol uses a “register map” allowing registers to be written to and read from.
    Throttle Command
    Description

    The throttle command is a 16-bit signed integer. The sign of the value determines the direction of rotation. Note, you must send a value of “0” at startup to initialize the thruster.
    Registers: (0x00-0x01)

        throttle: (write-only)
            -32767 (max reverse) to 32767 (max forward)
            0 is stopped
            No deadband

    Bytes

        Byte 0: throttle_h
        Byte 1: throttle_l

    Data Request
    Description

    The data registers can be read to provide information on voltage, current, RPM, and temperature. All values are 16-bit unsigned integers.
    Registers: (0x02-0x0A)

    pulse_count: (read-only)
        Commutation pulses since last request.
        Calculate rpm with pulse_count/dt*60/motor_pole_count
    voltage: (read-only)
        ADC measurement scaled to 16 bits
        Calculate voltage with voltage/2016
    temperature: (read-only)
        ADC measurement scaled to 16 bits
        Calculate temperature with the Steinhart equation
    current: (read-only)
        ADC measurement scaled to 16 bits
        Calculate current with (current-32767)/891
    identifier: (read-only)
        Identifier bit to test if ESC is alive

    Bytes

        Byte 0: pulse_count_h
        Byte 1: pulse_count_l
        Byte 2: voltage_h
        Byte 3: voltage_l
        Byte 4: temperature_h
        Byte 5: temperature_l
        Byte 6: current_h
        Byte 7: current_l
        Byte 8: 0xab (identifier to check if ESC is alive)


    RPM

    The RPM is sent as pulses since last read, which is the number of commutation cycles since the last time the I2C was polled.
    RPSESC=RPSraw0.5NpolesΔt
    RPMESC=60RPSESC

    The value of Npoles

    depends on the motor. The T100 has 12 poles and the T200 has 14 poles. The RPM measurement does not include direction. You can include direction by adding a negative symbol if the input signal to the ESC is negative.

    A code example follows:

    float rpm() {  
      _rpm = float(_rpm)/((uint16_t(millis())-_rpmTimer)/1000.0f)*60/float(_poleCount);
      _rpmTimer = millis();
    }


   Pymata Example
   pymata-aio/test/i2c/i2c_write/bicolor_display_controller.py

    write
    sboard.i2c_write_request(self.board_address,
    [(self.HT16K33_BLINK_CMD | self.HT16K33_BLINK_DISPLAYON | (b << 1))])

    read
    board.i2c_read_request(DEVICE_ADDRESS, REGISTER, Bytes, Constants.I2C_READ)
"""

from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants

BOARD_LED = 8
board = PyMata3(ip_address = '192.168.0.177', ip_port=3030, ip_handshake='')
#board = PyMata3(com_port='COM3')
# I2c address of the motor "0x29" is the default
DEVICE1_ADDRESS = 42
DEVICE2_ADDRESS = 43
DEVICE3_ADDRESS = 44
DEVICE4_ADDRESS = 45
DEVICE5_ADDRESS = 46
DEVICE6_ADDRESS = 47

# I2c register of the throttle (it is 16 bit/2 byte so treat it like a "word")
THROTTLE1 = 6000
THROTTLE2 = 8000
THROTTLE3 = 6000
THROTTLE4 = 5000
THROTTLE5 = 6000
THROTTLE6 = 6000

def setup():
#   board.set_pin_mode(BOARD_LED, Constants.OUTPUT)
# configure firmata for i2c on an UNO
    board.i2c_config(0)

def loop():
   #    print("LED On")
#    board.digital_write(BOARD_LED, 1)
#    board.sleep(1.0)
    TEMP = 0x02
    #The temperature's I2c regis ter (it's 2 bytes 0x06 and 0x07)
#    print("Is the BlueESC Alive?")
#    print(board.i2c_read_request(DEVICE_ADDRESS, TEMP, 9, Constants.I2C_READ))
#    print("Probably not in a real unit...")
#    board.sleep(1.0)

    board.i2c_write_request(DEVICE1_ADDRESS, [0, 0,  0])
    board.i2c_write_request(DEVICE2_ADDRESS, [0, 0,  0])
    board.i2c_write_request(DEVICE3_ADDRESS, [0, 0,  0])
    board.i2c_write_request(DEVICE4_ADDRESS, [0, 0,  0])
    board.i2c_write_request(DEVICE5_ADDRESS, [0, 0,  0])
    board.i2c_write_request(DEVICE6_ADDRESS, [0, 0,  0])
    
    board.sleep(2.0)

    board.i2c_write_request(DEVICE1_ADDRESS, [0, 0,  0])
	board.i2c_write_request(DEVICE2_ADDRESS, [0, 0,  0])
	board.i2c_write_request(DEVICE3_ADDRESS, [0, 0,  0])
	board.i2c_write_request(DEVICE4_ADDRESS, [0, 0,  0])
    board.i2c_write_request(DEVICE5_ADDRESS, [0, 4000>>8,  4000])
    board.i2c_write_request(DEVICE6_ADDRESS, [0, 4000>>8,  4000])


    board.sleep(2.0)




    '''print("initialize the motor")
    board.i2c_write_request(DEVICE1_ADDRESS, [0, 0,  0])
    board.i2c_write_request(DEVICE2_ADDRESS, [0, 0,  0])
    board.i2c_write_request(DEVICE3_ADDRESS, [0, 0,  0])
    board.i2c_write_request(DEVICE4_ADDRESS, [0, 0,  0])
    board.i2c_write_request(DEVICE5_ADDRESS, [0, 0,  0])
    board.i2c_write_request(DEVICE6_ADDRESS, [0, 0,  0])
    board.sleep(2.0)
    board.i2c_write_request(DEVICE1_ADDRESS, [0, -THROTTLE1>>8, -THROTTLE1])
    board.i2c_write_request(DEVICE2_ADDRESS, [0, -THROTTLE2>>8, -THROTTLE2])
    board.i2c_write_request(DEVICE3_ADDRESS, [0, -THROTTLE3>>8, -THROTTLE3])
    board.i2c_write_request(DEVICE4_ADDRESS, [0, -THROTTLE4>>8, -THROTTLE4])
    board.i2c_write_request(DEVICE5_ADDRESS, [0, -THROTTLE5>>8, -THROTTLE5])
    board.i2c_write_request(DEVICE6_ADDRESS, [0, -THROTTLE6>>8, -THROTTLE6])

#    board.i2c_write_request(DEVICE_ADDRESS, [0x00 | 0x00 | 0x00])
    board.sleep(2.0)

    print("turn on the motor forward")
    board.i2c_write_request(DEVICE1_ADDRESS, [0, 0,  0])
    board.i2c_write_request(DEVICE2_ADDRESS, [0, 0,  0])
    board.i2c_write_request(DEVICE3_ADDRESS, [0, 0,  0])
    board.i2c_write_request(DEVICE4_ADDRESS, [0, 0,  0])
    board.i2c_write_request(DEVICE5_ADDRESS, [0, 0,  0])
    board.i2c_write_request(DEVICE6_ADDRESS, [0, 0,  0])
    board.sleep(2.0)
    board.i2c_write_request(DEVICE1_ADDRESS, [0, THROTTLE1>>8, THROTTLE1])
    board.i2c_write_request(DEVICE2_ADDRESS, [0, THROTTLE2>>8, THROTTLE2])
    board.i2c_write_request(DEVICE3_ADDRESS, [0, THROTTLE3>>8, THROTTLE3])
    board.i2c_write_request(DEVICE4_ADDRESS, [0, THROTTLE4>>8, THROTTLE4])
    board.i2c_write_request(DEVICE5_ADDRESS, [0, THROTTLE5>>8, THROTTLE5])
    board.i2c_write_request(DEVICE6_ADDRESS, [0, THROTTLE6>>8, THROTTLE6])
    board.sleep(2)'''
#    board.i2c_write_request(DEVICE_ADDRESS, [0x00 | 9000])
#    board.sleep(5)
#    print("the motor has stopped due to inactivity")
#    board.sleep(3)
#    print("starting...")
#   print("initialize the motor")
#   board.i2c_write_request(DEVICE_ADDRESS, [THROTTLE | 0x0000])
#    board.i2c_write_request(DEVICE_ADDRESS, [THROTTLE | 0x00])
#    board.i2c_write_request(DEVICE_ADDRESS, [THROTTLE | 0xFF])
#    board.i2c_write_request(DEVICE_ADDRESS, [THROTTLE | 0x0
#    board.sleep(4)
#    print("reversing...")
#    board.i2c_write_request(DEVICE_ADDRESS, [THROTTLE, -6000])
#    board.sleep(8)

"""
#  print("LED Off")
#  board.digital_write(BOARD_LED, 0)
#  board.sleep(1.0)
"""
if __name__ == "__main__":
    setup()
    while True:
        loop()


