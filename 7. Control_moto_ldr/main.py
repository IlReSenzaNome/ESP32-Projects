import machine
import ssd1306
import time

# Configura los pines para I2C
i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21))

# Inicializa la pantalla OLED
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Configura el pin de entrada analógica para el sensor LDR
adc = machine.ADC(machine.Pin(35))

# Configura los pines para el controlador de motor L298N
ena = machine.PWM(machine.Pin(23))
in1 = machine.Pin(18, machine.Pin.OUT)
in2 = machine.Pin(19, machine.Pin.OUT)

# Configura la frecuencia del PWM
ena.freq(1000)

while True:
    # Limpia la pantalla
    oled.fill(0)
    
    # Lee la entrada analógica del sensor LDR
    valor_ldr = adc.read()
    
    # Muestra el valor del sensor LDR en la pantalla OLED
    oled.text('LDR: {}'.format(valor_ldr), 0, 0)
    oled.show()

    # Convierte el valor del sensor LDR en un valor de velocidad para el motor DC
    velocidad_motor = valor_ldr // 4  # Asume que el valor máximo del LDR es 1023

    # Configura la dirección del motor DC
    in1.value(1)
    in2.value(0)

    # Configura la velocidad del motor DC
    ena.duty(velocidad_motor)

    # Espera 1 segundo antes de la próxima lectura
    time.sleep(1)