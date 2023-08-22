#  Basic structure for writing code in uP
#  Libraries
import machine
import time
#  Variable
delay = 500 # ms
#  Configuration GPIO pin I/O
botton = machine.Pin(15, machine.Pin.IN) #  digital INPUT
led = machine.Pin(2, machine.Pin.OUT) #  digital OUTPUT
#  Code 
while True:
    if(botton.value() == 0):
        led.on()
        time.sleep_ms(delay)
        led.off()
        time.sleep_ms(delay)

