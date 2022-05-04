import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from state import State
from button_handler import ButtonHandler
from audio import play_audio

cycle_pin=11
select_pin=13
cancel_pin=15

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

GPIO.setup(cycle_pin, GPIO.IN,GPIO.PUD_UP) # Set pin nth to be an input pin and set initial value to be pulled low (off)
GPIO.setup(select_pin, GPIO.IN,GPIO.PUD_UP) # Set pin nth to be an input pin and set initial value to be pulled low (off)
GPIO.setup(cancel_pin, GPIO.IN,GPIO.PUD_UP) # Set pin nth to be an input pin and set initial value to be pulled low (off)

GPIO.add_event_detect(cycle_pin,GPIO.RISING,bouncetime=500) # Setup event on pin 10 rising edge
GPIO.add_event_detect(select_pin,GPIO.RISING,bouncetime=500) # Setup event on pin 10 rising edge
GPIO.add_event_detect(cancel_pin,GPIO.RISING,bouncetime=500) # Setup event on pin 10 rising edge

print("models Loaded")
play_audio.play("DocumentOCRMode.mp3")

if __name__ == "__main__":
    handler = ButtonHandler()

    while True:
        if GPIO.event_detected(cycle_pin):
            print('cycle_pin_pushed')
            handler.cycle()
            print(f"Currently in {State.name(handler.state)} mode")

        if GPIO.event_detected(select_pin):
            print(f"Currently in {State.name(handler.state)} mode")
            print('select_pin_pushed')
            handler.select()

        if GPIO.event_detected(cancel_pin):
            print('cancel_pin_pushed')
            handler.cancel()

    GPIO.cleanup() # Clean up
