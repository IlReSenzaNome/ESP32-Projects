from machine import Pin, DAC, PWM, SoftI2C
import time
import network
import socket
# from ssd1306 import SSD1306_I2C

# Inicializar DAC para el motor DC
# motor_dac = DAC(Pin(26))  # Usamos el canal DAC2 en GPIO 26

# Inicializar LED controlado por PWM
led_pwm = PWM(Pin(13))
led_pwm.freq(1000)
led_brightness = 0  # Brillo inicial del LED (0-100%)

# Inicializar PWM para el servomotor
servo_pwm = PWM(Pin(23))
servo_pwm.freq(50)
servo_angle = 90  # Ángulo inicial del servomotor

# Configuración de pantalla OLED
WIDTH = 128
HEIGHT = 64
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Configuración WiFi
SSID = "NETLIFE_VIVAS"
PASSWORD = "Vivas1717940272*"

# Función para conectar al WiFi
def connect_wifi():
    oled.fill(0)
    oled.text("Conectando a WiFi...", 0, 0)
    oled.show()
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    while not wlan.isconnected():
        time.sleep(1)
    
    ip_address = wlan.ifconfig()[0]
    oled.fill(0)
    oled.text("Conectado a WiFi!", 0, 0)
    oled.text(f"IP: ", 0, 10)
    oled.text(ip_address, 0, 20)
    oled.show()
    return ip_address

# Función para mapear valores (útil para el servomotor)
def map_value(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Configurar velocidad del motor (usando DAC)
def set_motor_speed(level):
    global motor_speed
    motor_speed = level
    # Convertir nivel a voltaje (0-255 para el DAC)
    # Mapeo el nivel (0, 10, 20, ..., 100) a un valor de 0 a 255
    voltage = int((level * 255) / 100)  # Mapeo el nivel de 0-100 al rango 0-255
    # motor_dac.write(voltage)  # Establecer voltaje en el DAC

# Configurar brillo del LED
def set_led_brightness(brightness):
    global led_brightness
    led_brightness = brightness
    duty = int((brightness / 100) * 65535)
    led_pwm.duty_u16(duty)

# Configurar ángulo del servomotor
def set_servo_angle(angle):
    global servo_angle
    servo_angle = angle
    duty = map_value(angle, 0, 180, 1000, 9000)  # Ajustar a rango PWM de ESP32
    servo_pwm.duty_u16(duty)

# Actualizar la pantalla OLED
def update_oled():
    oled.fill(0)
    oled.text("M:{0}% L:{1}% S:{2}°".format(motor_speed, led_brightness, servo_angle), 0, 0)
    oled.show()

# Iniciar servidor web
def start_server():
    addr = connect_wifi()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((addr, 80))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        request = conn.recv(1024).decode()

        # Controlar el motor DC
        if "/motor?speed=" in request:
            try:
                level = int(request.split("/motor?speed=")[1].split(" ")[0])
                if 0 <= level <= 100 and level % 10 == 0:
                    set_motor_speed(level)
                    update_oled()
            except:
                pass

        # Controlar el LED
        if "/led?brightness=" in request:
            try:
                brightness = int(request.split("/led?brightness=")[1].split(" ")[0])
                if 0 <= brightness <= 100:
                    set_led_brightness(brightness)
                    update_oled()
            except:
                pass

        # Controlar el servomotor
        if "/servo?angle=" in request:
            try:
                angle = int(request.split("/servo?angle=")[1].split(" ")[0])
                if 0 <= angle <= 180:
                    set_servo_angle(angle)
                    update_oled()
            except:
                pass

        # Cargar HTML
        with open("index.html", "r") as file:
            html = file.read()
        conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + html)
        conn.close()

# Configuración inicial
set_motor_speed(0)
set_led_brightness(led_brightness)
set_servo_angle(servo_angle)
oled.fill(0)
oled.text("Iniciando...", 0, 0)
oled.show()

# Iniciar servidor
start_server()