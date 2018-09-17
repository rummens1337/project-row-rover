import smbus
import time
MotorR = [7, 3, 0xa5, 1, 3, 0xa5, 2]  # High speed left backwards + right forward
MotorL = [7, 3, 0xa5, 2, 3, 0xa5, 1]  # High speed left forwards + right backwards
MotorHF = [7, 3, 0xa5, 2, 3, 0xa5, 2]  # High speed forward left + right; add explanation
MotorST = [7, 0, 0, 0, 0, 0, 0]  # Stop left + right; add explanation
MotorHR = [7, 3, 0xa5, 1, 3, 0xa5, 1]  # High speed reverse left + right; add explanation
adress = 0x32  # I2c address of the motorcontroller



bus = smbus.SMBus(1)
for i in range(1000):
	Moto = [7, 3, i, 1, 3, i, 2]
	bus.write_i2c_block_data(adress, 0, Moto)
	time.sleep(0.01)

while 1:
	test = input("enter input:\n")
	if test == 'q':
		bus.write_i2c_block_data(adress, 0, MotorST)
	if test == 's':
		bus.write_i2c_block_data(adress, 0, MotorHR)
	if test == 'w':
		bus.write_i2c_block_data(adress, 0, MotorHF)
	if test == 'a':
		bus.write_i2c_block_data(adress, 0, MotorL)
	if test == 'd':
		bus.write_i2c_block_data(adress, 0, MotorR)
