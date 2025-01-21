# Creditos: TechToTinker

#Cargamos las librerias
import machine
import time

# Definimos el pin del servomotor
p23 = machine.Pin(23, machine.Pin.OUT)
servo1 = machine.PWM(p23)

# Definimos el ancho de pulso
servo1.freq(50)

#Inicializamos el servo en 0 grados
servo1.duty(0)

# Implementamos la funcion map de arduino de 0 to 180 degrees
# Y desde 20 a 120 pwm 
def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Creamos la funcion servo
# Para usar el servo de acuerdo a los angulos
def servo(pin, angle):
    pin.duty(map(angle, 0, 180, 20, 120))

"""
# Para rotar el servo a 0 grados
servo(servo1, 0)
time.sleep(0.5)
# Para rotar el servo a 90 grados
servo(servo1, 90)
time.sleep(0.5)
# Para rotar el servo a 180 grados
servo(servo1, 180)
time.sleep(0.5)
# Ciclo para rotar el servo de 0 a 180
# De 10 en 10 grados

"""    
for i in range(0, 180, 10):
    servo(servo1, i)
    time.sleep(0.5)

# from machine import Pin, I2C
# from time import sleep
# import TCS34725
# import ssd1306

# # Inicializa I2C
# i2c = I2C(0, sda=Pin(21), scl=Pin(22))

# # Verificar dispositivos I2C
# devices = i2c.scan()

# # Direcciones I2C comunes
# TCS34725_ADDR = 0x29  # Dirección por defecto del sensor TCS34725
# SSD1306_ADDR = 0x3C   # Dirección por defecto de la pantalla OLED

# # Variables de estado
# sensor_conectado = TCS34725_ADDR in devices
# pantalla_conectada = SSD1306_ADDR in devices

# try:
#     # Inicializa la pantalla OLED si está conectada
#     if pantalla_conectada:
#         oled = ssd1306.SSD1306_I2C(128, 64, i2c)
#         oled.fill(0)
#         if sensor_conectado:
#             oled.text("Sensor conectado", 0, 0)
#         else:
#             oled.text("Sensor NO conectado", 0, 0)
#         oled.text("Pantalla conectada", 0, 10)
#         oled.show()
#     else:
#         print("Pantalla OLED no conectada.")
# except Exception as e:
#     print(f"Error al inicializar la pantalla: {e}")

# # Inicializa el sensor si está conectado
# if sensor_conectado:
#     try:
#         sensor = TCS34725.TCS34725(i2c)
#     except Exception as e:
#         print(f"Error al inicializar el sensor: {e}")
# else:
#     print("Sensor TCS34725 no conectado.")

# sensor = TCS34725.TCS34725(i2c)

# # Bucle principal
# if sensor_conectado and pantalla_conectada:
#     while True:
#         # Lee los valores del sensor
#         r, g, b, c = sensor.read('raw')

#         # Muestra los valores en la consola
#         print('Rojo: {}, Verde: {}, Azul: {}, Claro: {}'.format(r, g, b, c))

#         # Muestra los valores en la pantalla OLED
#         oled.fill(0)
#         oled.text('Rojo: {}'.format(r), 0, 0)
#         oled.text('Verde: {}'.format(g), 0, 10)
#         oled.text('Azul: {}'.format(b), 0, 20)
#         oled.text('Claro: {}'.format(c), 0, 30)
#         oled.show()

#         sleep(1)
# else:
#     print("Conexión incompleta. Verifica hardware.")

