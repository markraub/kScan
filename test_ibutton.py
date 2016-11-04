import get_user as guh
import os
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

def tester(varID):
	
	print(guh.read_ibutton(varID))

def get_ibutton():

	os.system('modprobe wire timeout=1 slave_ttl=5')
	os.system('modprobe w1-gpio')
	os.system('modprobe w1-smem')

	GPIO.setup(24,GPIO.OUT)
	base_dir = '/sys/devices/w1_bus_master1/w1_master_slaves'
	delete_dir = '/sys/devices/w1_bus_master1/w1_master_remove'
	GPIO.output(24,True)
	
	while True:
	
		data = open(base_dir, "r")
		ibutton = data.read()
		data.close()
		if ibutton != 'not found.\n':
			GPIO.output(24,False)
			time.sleep(3)
			print(ibutton)
			tester(ibutton)
			d = open(delete_dir, "w")
			d.write(ibutton)
			d.close()
			GPIO.output(24, True)

	GPIO.cleanup()
	
get_ibutton()









