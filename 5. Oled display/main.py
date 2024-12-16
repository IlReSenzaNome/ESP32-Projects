import machine
import ssd1306
import time

# Configura los pines para I2C
i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21))

# Inicializa la pantalla OLED
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)


while True: 
    oled.fill(0)
    oled.text("Texto de prueba", 0, 0)
    oled.show()

# # Configura el pin del LED incorporado
# led = machine.Pin(2, machine.Pin.OUT)

# # Muestra "Hola Mundo" en la pantalla OLED
# oled.fill(0)
# oled.text('Hola Mundo', 0, 0)
# oled.show()

# # Enciende el LED
# led.on()

# # Espera 10 segundos
# time.sleep(10)

# # Apaga el LED
# led.off()