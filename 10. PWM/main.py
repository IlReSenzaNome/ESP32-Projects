from machine import Pin, PWM, I2C
import time
import network
import socket
from ssd1306 import SSD1306_I2C

# Configuración de componentes físicos
button_up = Pin(14, Pin.IN, Pin.PULL_UP)  # Botón para aumentar velocidad
button_down = Pin(27, Pin.IN, Pin.PULL_UP)  # Botón para disminuir velocidad
leds = [Pin(32, Pin.OUT), Pin(33, Pin.OUT), Pin(25, Pin.OUT)]  # LEDs de velocidad

# Inicializar PWM para el ventilador
fan_pwm = PWM(Pin(26))
fan_pwm.freq(25000)
fan_speed = 0  # Velocidad inicial del ventilador (0 = 0%, 1 = 50%, 2 = 100%)

# Inicializar PWM para el servomotor (Pin 23)
p23 = Pin(23, Pin.OUT)
servo1 = PWM(p23)
servo1.freq(50)
servo_angle = 90  # Ángulo inicial del servomotor

# Función para mapear de 0 a 180 grados y de 20 a 120 PWM
def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Función para controlar el servo
def servo(pin, angle):
    pin.duty(map(angle, 0, 180, 20, 120))

# Configuración de pantalla OLED
WIDTH = 128
HEIGHT = 64
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Configuración WiFi
SSID = "kevin"
PASSWORD = "123456789"

# Función para conectar al WiFi y mostrar en OLED
def connect_wifi():
    oled.fill(0)
    oled.text("Conectando a WiFi...", 0, 0)
    oled.show()
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    while not wlan.isconnected():
        print("Conectando al WiFi...")
        time.sleep(1)
    
    ip_address = wlan.ifconfig()[0]
    print("Conectado al WiFi:", ip_address)
    
    # Mostrar conexión exitosa en OLED
    oled.fill(0)
    oled.text("Conectado a WiFi!", 0, 0)
    oled.text(f"IP: ", 0, 10)
    oled.text(f"{ip_address}", 0, 20)
    oled.show()
    
    return ip_address

# Función para configurar la velocidad del ventilador
def set_fan_speed(level):
    global fan_speed
    fan_speed = level
    duty = int((level / 2) * 65535)
    fan_pwm.duty_u16(duty)
    for i in range(3):
        leds[i].value(1 if i == level else 0)

# Función para configurar el ángulo del servomotor
def set_servo_angle(angle):
    global servo_angle
    servo_angle = angle
    servo(servo1, angle)  # Mueve el servo al ángulo deseado

# Actualizar la pantalla OLED
def update_oled():
    oled.fill(0)
    oled.text("Ventilador:", 0, 0)
    oled.text(f"Vel: {fan_speed * 50}%", 0, 10)
    oled.text("Servo:", 0, 30)
    oled.text(f"Ang: {servo_angle}", 0, 40)
    oled.show()

# Manejo de botones
def handle_buttons():
    global fan_speed
    if not button_up.value():  # Botón para aumentar velocidad
        if fan_speed < 2:
            set_fan_speed(fan_speed + 1)
            update_oled()
            time.sleep(0.3)  # Evitar rebotes
    if not button_down.value():  # Botón para disminuir velocidad
        if fan_speed > 0:
            set_fan_speed(fan_speed - 1)
            update_oled()
            time.sleep(0.3)  # Evitar rebotes

# Iniciar servidor web
def start_server():
    addr = connect_wifi()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((addr, 80))
    s.listen(5)
    print("Servidor iniciado en:", addr)

    while True:
        conn, addr = s.accept()
        print("Conexión de:", addr)
        request = conn.recv(1024).decode()
        print("Solicitud:", request)

        # Controlar el ventilador desde el servidor
        if "/fan?speed=" in request:
            try:
                level = int(request.split("/fan?speed=")[1].split(" ")[0])
                if 0 <= level <= 2:
                    set_fan_speed(level)
                    update_oled()
            except:
                pass

        # Controlar el servomotor desde el servidor
        if "/servo?angle=" in request:
            try:
                angle = int(request.split("/servo?angle=")[1].split(" ")[0])
                if 0 <= angle <= 180:
                    set_servo_angle(angle)
                    update_oled()
            except:
                pass

        # Respuesta del servidor
        html = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Control Ventilador y Servo</title></head>
        <body>
            <h1>Control de Ventilador y Servomotor</h1>
            <h2>Velocidad Ventilador: {fan_speed * 50}%</h2>
            <form action="/fan">
                <label>Velocidad:</label>
                <input type="range" name="speed" min="0" max="2" step="1" value="{fan_speed}">
                <input type="submit" value="Ajustar">
            </form>
            <h2>Ángulo Servomotor: {servo_angle}</h2>
            <form action="/servo">
                <label>Ángulo:</label>
                <input type="range" name="angle" min="0" max="180" step="1" value="{servo_angle}">
                <input type="submit" value="Ajustar">
            </form>
        </body>
        </html>
        """
        conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + html)
        conn.close()

# Configuración inicial
set_fan_speed(fan_speed)
set_servo_angle(servo_angle)

# Mostrar mensaje inicial en OLED
oled.fill(0)
oled.text("Iniciando...", 0, 0)
oled.show()

# Iniciar servidor
start_server()

# Bucle principal
while True:
    handle_buttons()
    time.sleep(0.1)
