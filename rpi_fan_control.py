import RPi.GPIO as GPIO
import getopt, sys
from vcgencmd import vcgencmd
from time import sleep       

#default confguration
vPin = 26
vTemp = 60
vVerb = False

try:
    opts, args = getopt.getopt(sys.argv[1:], "p:t:v", ["pin=", "temp=", "verbose"])
except getopt.GetoptError:
    print ("Usage: rpi_fan_control.py -p <GPIO pin #> -t <temperature> [-v <verbose>]")
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-p", "--pin"):
        vPin = int(arg)         #fan pin, хөргүүр сэнсний удирдах хөл
    elif opt in ("-t", "--temp"):
        vTemp = float(arg)     #highest temperature value which fan starts rotating
                                #Сэнсийг эргүүлж эхлэх хамгийн өндөр температурын утга
    elif opt in ("-v", "--verbose"):
        vVerb = True     #highest temperature value which fan starts rotating

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(vPin, GPIO.OUT)

while True:
    try:
        vCpu_temp = vcgencmd.measure_temp()
        vCpu_freq = vcgencmd.measure_clock('arm') / 1000000     #converting Hz o MHz, Герцийг Мега герцрүү хөрвүүлж урт тоог хураангуйлж байна

        if vTemp < vCpu_temp:
            GPIO.output(vPin, GPIO.HIGH)
        else:
            GPIO.output(vPin, GPIO.LOW)
        
        if vVerb == True: 
            print ("CPU temp:%2.1fc, freq:%2.1fMHz" % (vCpu_temp, vCpu_freq))
            sys.stdout.write("\033[F") #back to previous line 
            sys.stdout.write("\033[K") #clear line
        
        sleep(1)
    
    except KeyboardInterrupt:
        sys.stdout.write("\033[F") #back to previous line 
        sys.stdout.write("\033[K") #clear line
        print ("rpi_fan_control.py's been terminated")
        sys.exit(0)