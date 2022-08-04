import board
import tca9548a
import time
import adafruit_vl53l1x

# Create I2C bus as normal
i2c = board.I2C()  # uses board.SCL and board.SDA

# Create the TCA9548A object and give it the I2C bus
tca = tca9548a.TCA9548A(i2c, debug=True)
total = 0


for channel in range(8):
    needs_unlock = True
    if tca[channel].try_lock():
        print("Channel {}:".format(channel), end="")
        addresses = tca[channel].scan()
        for address in addresses:
            if address == 0x29:
                print('found lidar____________________________________________________________________________________')
                total += 1
                print('unlocking channel')
                tca[channel].unlock()
                needs_unlock = False
                print('grabbing sensor')
                sensor_i2c = adafruit_vl53l1x.VL53L1X(tca[channel], 0x29)  # Pass child bus instead of parent.
                print('start measuring')
                sensor_i2c.start_ranging()
                print('record data')
                # while True:
                for i in range(1):  # Place holder to get multiple samples if desired.
                    print('check sensor ready')
                    if sensor_i2c.data_ready:
                        print('get distance')
                        distance = sensor_i2c.distance
                        if distance:
                            print('reading', distance)
                        print('clearing interrupt')
                        sensor_i2c.clear_interrupt()
                    time.sleep(0.1)
    if needs_unlock:
        print('unlocking channel')
        tca[channel].unlock()
print('total modules found:', total)
