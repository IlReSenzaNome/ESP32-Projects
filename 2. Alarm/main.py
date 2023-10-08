#  Basic structure for writing code in uP
#  Libraries
import machine
import time
#  Variable
delay = 1000 # ms
#  Configuration GPIO pin I/O
botton = machine.Pin(15, machine.Pin.IN) #  digital INPUT
led = machine.Pin(2, machine.Pin.OUT) #  digital OUTPUT
buzzer = machine.Pin(4, machine.Pin.OUT)
#  Code 
while True:
    led.on()
    buzzer.off()
    if(botton.value() == 0):
        led.off()
        buzzer.on()
        time.sleep_ms(delay)