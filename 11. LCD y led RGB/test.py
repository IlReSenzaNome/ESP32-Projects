from machine import Pin, SoftI2C, PWM
import bluetooth
import BLE 
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep

# Pines de los colores RGB
red = Pin(14, Pin.OUT)
green = Pin(12, Pin.OUT)
blue = Pin(13, Pin.OUT)

# Direcciones y configuración del LCD I2C
I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)

# Configuración del Bluetooth y UART
name = 'peor es nada ESP32'
ble = bluetooth.BLE()
uart = BLE.BLEUART(ble, name)

# Variables para controlar la saturación de los colores
saturation_red = 0
saturation_green = 0
saturation_blue = 0

# PWM para controlar la intensidad del color en el LED RGB
pwm_red = PWM(red, freq=1000, duty=0)
pwm_green = PWM(green, freq=1000, duty=0)
pwm_blue = PWM(blue, freq=1000, duty=0)

# Función para actualizar el LED RGB
def update_led():
    pwm_red.duty(saturation_red)
    pwm_green.duty(saturation_green)
    pwm_blue.duty(saturation_blue)

# Función que se ejecuta cuando llega un dato por Bluetooth
def on_rx():
    global saturation_red, saturation_green, saturation_blue

    rx_buffer = uart.read().decode().strip()

    uart.write('ESP32 says: ' + str(rx_buffer) + '\n')

    # Acumular el valor dependiendo del color recibido
    if rx_buffer == 'R':
        saturation_red = min(saturation_red + 10, 1023)  # Asegurarse de que no pase de 1023
    elif rx_buffer == 'G':
        saturation_green = min(saturation_green + 10, 1023)  # Asegurarse de que no pase de 1023
    elif rx_buffer == 'B':
        saturation_blue = min(saturation_blue + 10, 1023)  # Asegurarse de que no pase de 1023
    
    update_led()

    # Mostrar los valores de saturación de cada color en el LCD
    lcd.clear()
    lcd.putstr("R:{:.0f}% G:{:.0f}% B:{:.0f}%".format(
        (saturation_red / 1023) * 100,
        (saturation_green / 1023) * 100,
        (saturation_blue / 1023) * 100
    ))

# Configurar la interrupción del UART para recibir datos
uart.irq(handler=on_rx)

# Inicializar el LCD
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

# Mostrar un mensaje inicial en el LCD
while True:
    lcd.putstr("I2C LCD Tutorial")
    sleep(2)
    lcd.clear()
    lcd.putstr("Esperando comandos...")
    sleep(2)
    lcd.clear()