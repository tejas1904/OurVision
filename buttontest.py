import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from button_handler import ButtonHandler
import os
from time import sleep

focus=162
value = (focus<<4) & 0x3ff0
dat1 = (value>>8)&0x3f
dat2 = value & 0xf0

cycle_pin=33    #button "1"
select_pin=31   #button "2"
cancel_pin=37 #button "3"
other_pin = 35 #button "4"

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

GPIO.setup(cycle_pin, GPIO.IN,GPIO.PUD_UP) # Set pin nth to be an input pin and set initial value to be pulled low (off)
GPIO.setup(select_pin, GPIO.IN,GPIO.PUD_UP) # Set pin nth to be an input pin and set initial value to be pulled low (off)
GPIO.setup(cancel_pin, GPIO.IN,GPIO.PUD_UP) # Set pin nth to be an input pin and set initial value to be pulled low (off)
GPIO.setup(other_pin, GPIO.IN,GPIO.PUD_UP) # Set pin nth to be an input pin and set initial value to be pulled low (off)

GPIO.add_event_detect(cycle_pin,GPIO.RISING,bouncetime=500) # Setup event on pin 10 rising edge
GPIO.add_event_detect(select_pin,GPIO.RISING,bouncetime=500) # Setup event on pin 10 rising edge
GPIO.add_event_detect(cancel_pin,GPIO.RISING,bouncetime=500) # Setup event on pin 10 rising edge
GPIO.add_event_detect(other_pin,GPIO.RISING,bouncetime=500) # Setup event on pin 10 rising edge

debug = False
if __name__ == "__main__":
    handler = ButtonHandler()
    #handler.select()
    #sleep(5)
    while True:
        if debug:inp = int(input("option 1,2 or 3:"))
        if  GPIO.event_detected(cycle_pin):
            print('cycle_pin_pushed')
            # print(f"Currently in {State.name(handler.state)} mode")

        if   GPIO.event_detected(select_pin):
            # print(f"Currently in {name(handler.state)} mode")
            print('select_pin_pushed')

        if  GPIO.event_detected(cancel_pin):
            print('cancel_pin_pushed')
        if  GPIO.event_detected(other_pin):
            print('oterh pin pressed')

GPIO.cleanup() # Clean up
