from machine import Pin, I2C
from time import sleep, ticks_ms
import ssd1306
import hcsr04

trig = 2
echo = 4

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

sensor = hcsr04.HCSR04(trigger_pin=trig, echo_pin=echo)

ledr = Pin(12, Pin.OUT)
ledg = Pin(13, Pin.OUT)
ledb = Pin(14, Pin.OUT)

buttonPin = Pin(27, Pin.IN, Pin.PULL_UP)

current_state = "traffic"  # Estado inicial

# Funciones para controlar las luces
def off_light():
    ledr.off()
    ledb.off()
    ledg.off()

def red_light():
    ledb.off()
    ledr.on()
    ledg.off()

def green_light():
    ledg.on()
    ledr.off()
    ledb.off()

def yellow_light():
    ledb.off()
    ledg.on()
    ledr.on()

def blink_led():
    for _ in range(3):
        yellow_light()
        sleep(0.5)
        off_light()
        sleep(0.5)

    green_light()
    sleep(1)

def traffic_light():
    red_light()
    sleep(1)
    yellow_light()
    sleep(2)
    green_light()
    sleep(3)

def ultimate(curren_state):
    if curren_state == "green":
        green_light()
    elif curren_state == "yellow":
        yellow_light()
    else:
        red_light()
        return "red"
    return curren_state

# Manejar la interrupción del botón
def button_pressed(pin):
    global current_state
    previous_state = current_state  # Guardar el estado previo de la luz

    blink_led()  # Realizar parpadeo de luces
    sleep(2)  # Esperar un tiempo antes de pasar a verde
    current_state = ultimate(current_state)  # Cambiar el estado de las luces
    sleep(2)  # Mantener verde por un tiempo
    
    # Resetear al estado inicial si el estado no cambió
    if current_state == previous_state:
        traffic_light()
        current_state = "traffic"  # Restablecer a "traffic"

# Configurar la interrupción del botón
buttonPin.irq(trigger=Pin.IRQ_FALLING, handler=button_pressed)

# Función de interrupción por distancia
def interuption(distance):
    if distance < 6:
        red_light()  # Si la distancia es menor a 6 cm, poner rojo
    elif distance <= 13:
        blink_led()  # Si está entre 6 y 9 cm, parpadea
    else:
        traffic_light()  # Si está por encima de 9 cm, luces de tráfico

def main():
    global current_state
    last_read_time = ticks_ms()  # Para controlar la tasa de lectura del sensor

    while True:
        # Controlar la tasa de lectura del sensor a intervalos regulares
        if ticks_ms() - last_read_time >= 50:  # Leer el sensor cada 50 ms
            last_read_time = ticks_ms()
            distance = sensor.distance_cm()  # Obtener la distancia

            # Actualizar la pantalla OLED solo cuando cambie el estado
            oled.fill(0)
            oled.text("Distancia en cm: ", 0, 0)
            oled.text(str(distance), 0, 10)
            oled.show()

            # Manejar la interrupción en función de la distancia
            interuption(distance)

        # Pausa corta para evitar uso excesivo del procesador
        sleep(0.01)

if __name__ == "__main__":
    main()




# from machine import Pin, I2C
# from time import sleep, ticks_ms
# import ssd1306
# import hcsr04

# trig = 2
# echo = 4

# i2c = I2C(0, scl=Pin(22), sda=Pin(21))
# oled_width = 128
# oled_height = 64
# oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# sensor = hcsr04.HCSR04(trigger_pin=trig, echo_pin=echo)

# ledr = Pin(12, Pin.OUT)
# ledg = Pin(13, Pin.OUT)
# ledb = Pin(14, Pin.OUT)

# buttonPin = Pin(27, Pin.IN, Pin.PULL_UP)

# current_state = "traffic"  

# def off_light():
#     ledr.off()
#     ledb.off()
#     ledg.off()

# def red_light():
#     ledb.off()
#     ledr.on()
#     ledg.off()

# def green_light():
#     ledg.on()
#     ledr.off()
#     ledb.off()

# def yellow_light():
#     ledb.off()
#     ledg.on()
#     ledr.on()

# def blink_led():
#     for _ in range(3):
#         yellow_light()
#         sleep(0.5)
#         off_light()
#         sleep(0.5)

#     green_light()
#     sleep(1)

# def traffic_light():
#     red_light()
#     sleep(1)
#     yellow_light()
#     sleep(2)
#     green_light()
#     sleep(3)

# def ultimate(curren_state):
#     if curren_state == "green":
#         green_light()
#     elif curren_state == "yellow":
#         yellow_light()
#     else:
#         red_light()
#         return "red"
#     return curren_state



# # Manejar la interrupción del botón
# def button_pressed(pin):
#     global current_state
#     blink_led()  # Realizar parpadeo de luces
#     sleep(2)  # Esperar un tiempo antes de pasar a verde
#     current_state = ultimate(current_state)
#     sleep(2)  # Mantener verde por un tiempo  # Resetear al estado inicial
#     if current_state == ultimate(current_state): 
#         traffic_light()
#         current_state = "traffic"

# # Configurar la interrupción del botón
# buttonPin.irq(trigger=Pin.IRQ_FALLING, handler=button_pressed)

# # Función de interrupción por distancia
# def interuption(distance):
#     if distance < 6:
#         red_light()  # Si la distancia es menor a 6 cm, poner rojo
#     elif distance <= 13:
#         blink_led()  # Si está entre 6 y 9 cm, parpadea
#     else:
#         traffic_light()  # Si está por encima de 9 cm, luces de tráfico

# def main():
#     global current_state
#     last_read_time = ticks_ms()  # Para controlar la tasa de lectura del sensor

#     while True:
#         # Controlar la tasa de lectura del sensor a intervalos regulares
#         if ticks_ms() - last_read_time >= 50:  # Leer el sensor cada 50 ms
#             last_read_time = ticks_ms()
#             distance = sensor.distance_cm()  # Obtener la distancia

#             # Actualizar la pantalla OLED solo cuando cambie el estado
#             oled.fill(0)
#             oled.text("Distancia en cm: ", 0, 0)
#             oled.text(str(distance), 0, 10)
#             oled.show()

#             # Manejar la interrupción en función de la distancia
#             interuption(distance)

#         # Pausa corta para evitar uso excesivo del procesador
#         sleep(0.01)

# if __name__ == "__main__":
#     main()