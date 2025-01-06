import time
from machine import Pin, I2C
from tcs34725 import TCS34725
import ssd1306
from gorilla_rgb import GORILLACELL_RGB

i2c_bus = I2C(0, sda=Pin(21), scl=Pin(22))
tcs = TCS34725(i2c_bus)
rgb = GORILLACELL_RGB(25, 26, 27)

while True:
    red, grn, blu = tcs.read('dec')
    rgb.set_rgb(red, grn, blu)


# # The following lines of code should be tested in the REPL:
# #
# # 1. To print the raw data:
# print('raw: {}'.format(tcs.read('raw')))
# #
# # 2. To print the RGB data:
# print('rgb: {}'.format(tcs.read('rgb')))
# #
# # 3. To print the RGB data in decimal form:
# print('dec: {}'.format(tcs.read('dec')))
# #
# # 4. To print the RGB data in hex form:
# print('hex: {}'.format(tcs.read('hex')))
# #
# # 5. To print the color temperature in ^Kelvin and
# #    the luminosity in lux
# print('lux: {}'.format(tcs.read('lux')))


# print('I2C adresse: '+hex(i2c.scan()[0]))
# print('I2C adresse: '+str(i2c.scan()[0]))

# from machine import Pin, PWM
# import time

# # Configurar los pines de los servomotores
# servo1 = PWM(Pin(14))  # Pin GPIO para el servo 1
# servo2 = PWM(Pin(15))  # Pin GPIO para el servo 2

# # Configurar la frecuencia de los servomotores (50Hz es común para servos)
# servo1.freq(50)
# servo2.freq(50)

# def set_servo_angle(servo, angle):
#     """Convierte el ángulo (0-180) a un valor de PWM (500-2500 microsegundos)."""
#     pulse_width = int(500 + (angle / 180.0) * 2000)  # Mapeo de 0-180 a 500-2500
#     servo.duty_u16(int(pulse_width / 20 * 65535 / 1000))  # PWM duty cycle de 16 bits

# # Bucle para mover los servos
# try:
#     while True:
#         set_servo_angle(servo1, 90)
#         set_servo_angle(servo2, 0)
        

# except KeyboardInterrupt:
#     print("Programa interrumpido.")
