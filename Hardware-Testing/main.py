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

