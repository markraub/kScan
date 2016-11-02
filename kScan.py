import ibutton 
import os
import json
import sane
from PIL import Image


def transferFile(user, homedir, imageName):

	if user is not None and homedir is not None and image is not None:
		
		imagepath = "/scans/" + imageName
		status = os.system('scp ' + imagepath + user + "@shell.csh.rit.edu:" + homedir + ".scan/"
		print(status)

def takeScan():

	ver = sane.init()
	print("SANE Version: " + ver)
	
	devices = sane.get_devices()
	
	sel_dev = sane.open(devices[0][0])

	sel_dev.start()

	print("Starting device")
	print("Scanning...")

	im = sel_dev.snap()

	im.save('test_pil.jpeg')
