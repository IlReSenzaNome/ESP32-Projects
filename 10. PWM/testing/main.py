import network
import socket
import time
import uasyncio as asyncio
from machine import Pin

# Configuración de pines de control
rele_motor = Pin(12, Pin.OUT)  # Relé para controlar el motor
rele_luz_piloto = Pin(13, Pin.OUT)  # Relé para la luz piloto (roja)
boton_reinicio = Pin(14, Pin.IN, Pin.PULL_UP)  # Botón para reiniciar el proceso (en la web no se usa este pin)

# Variables de tiempo
tiempo_motor = 0  # Tiempo de funcionamiento del motor en segundos
tiempo_detencion = 0  # Tiempo que el motor estuvo detenido
umbral_mantenimiento = 300  # Umbral de tiempo para el mantenimiento (5 minutos)
en_mantenimiento = False  # Estado de si el motor necesita mantenimiento

# Variables para el servidor web
ip_esp32 = ""  # Dirección IP del ESP32

# Configuración Wi-Fi
ssid = "NETLIFE_VIVAS"
password = "Vivas1717940272*"

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    print("Conectando a WiFi...")
    while not wlan.isconnected():
        time.sleep(1)
        print(".", end="")
    print("\n✅ Conectado a WiFi")
    ip = wlan.ifconfig()[0]
    print(f"🌐 Dirección IP del ESP32: {ip}")
    return ip

# Conexión Wi-Fi
ip_esp32 = conectar_wifi()

# Función para simular el motor DC
async def simular_motor():
    global tiempo_motor, tiempo_detencion, en_mantenimiento

    while True:
        if not en_mantenimiento:  # Si el motor está en funcionamiento
            tiempo_motor += 1
            print(f"Motor funcionando: {tiempo_motor}s")

            if tiempo_motor >= umbral_mantenimiento and not en_mantenimiento:
                # Si se alcanzó el umbral de mantenimiento
                rele_luz_piloto.value(1)  # Enciende la luz piloto roja
                en_mantenimiento = True  # El motor entra en estado de mantenimiento
                print("🚨 Mantenimiento requerido: El motor ha alcanzado el tiempo máximo.")
            await asyncio.sleep(1)

        else:
            # El motor está detenido, contar el tiempo de detención
            tiempo_detencion += 1
            print(f"Tiempo detenido: {tiempo_detencion}s")
            await asyncio.sleep(1)

# Función para manejar las peticiones HTTP
async def manejar_peticiones(reader, writer):
    global tiempo_motor, tiempo_detencion, en_mantenimiento

    # Leer la solicitud del navegador
    request = await reader.read(1024)
    request = str(request)
    print("Petición HTTP:", request)

    # Responder dependiendo de la petición
    if "GET /reiniciar" in request:
        # Reinicia el contador de tiempo del motor y apaga la luz piloto
        tiempo_motor = 0
        tiempo_detencion = 0
        en_mantenimiento = False
        rele_luz_piloto.value(0)  # Apaga la luz piloto
        rele_motor.value(0)  # Apaga el motor
        respuesta = "Sistema reiniciado."
    elif "GET /apagar" in request:
        # Apaga el motor y la luz piloto
        rele_motor.value(0)
        rele_luz_piloto.value(0)
        respuesta = "Sistema apagado."
    elif "GET /encender" in request:
        # Enciende el motor
        rele_motor.value(1)
        respuesta = "Motor encendido."
    else:
        # Muestra el estado del sistema
        respuesta = f"""
        Tiempo de uso del motor: {tiempo_motor}s<br>
        Tiempo detenido: {tiempo_detencion}s<br>
        {"¡Mantenimiento necesario!" if en_mantenimiento else "Motor en funcionamiento."}
        <br><br>
        <a href="/reiniciar">Reiniciar Sistema</a><br>
        <a href="/apagar">Apagar Sistema</a><br>
        <a href="/encender">Encender Motor</a>
        """

    # Crear la respuesta HTML con CSS
    respuesta_html = f"""\
    HTTP/1.1 200 OK
    Content-Type: text/html

<html>
    <head>
        <meta charset="UTF-8">
        <title>Control de Motor</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background-color: #2c3e50;
                color: #ecf0f1;
                margin: 0;
                padding: 0;
                text-align: center;
            }}
            h1 {{
                font-size: 3em;
                color: #e74c3c;
                margin-top: 20px;
            }}  
            .container {{
                width: 80%;
                margin: 0 auto;
                padding: 20px;
                background-color: #34495e;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
            }}
            p {{
                font-size: 1.2em;
                line-height: 1.5;
            }}
            button {{
                background-color: #e74c3c;
                color: white;
                font-size: 1.2em;
                border: none;
                padding: 10px 20px;
                margin: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s;
            }}
            button:hover {{
                background-color: #c0392b;
            }}
            .status {{
                margin-top: 20px;
                font-size: 1.4em;
            }}
            .maintenance {{
                color: #f39c12;
                font-weight: bold;
            }}
            a {{
                color: #3498db;
                text-decoration: none;
                font-size: 1.1em;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Control de Motor</h1>
            <p>{{ respuesta }}</p>  <!-- Reemplazar {{ respuesta }} en el servidor -->
            <div class="status">
                <h3>Acciones del Sistema</h3>
                <button onclick="window.location.href='/encender'">Encender Motor</button>
                <button onclick="window.location.href='/apagar'">Apagar Motor</button>
                <button onclick="window.location.href='/reiniciar'">Reiniciar Sistema</button>
            </div>
            <div class="status">
                <h3>Estado del Motor</h3>
                <p class="maintenance">{{ 'Motor en Mantenimiento' if en_mantenimiento else 'Motor en Funcionamiento' }}</p>
            </div>
        </div>
    </body>
</html>
    """

    # Enviar respuesta
    await writer.awrite(respuesta_html)
    await writer.aclose()

# Servidor Web Asíncrono
async def servidor():
    servidor_socket = socket.socket()
    servidor_socket.bind(('', 80))
    servidor_socket.listen(1)
    print(f"Servidor escuchando en http://{ip_esp32}:80")
    while True:
        reader, writer = await servidor_socket.accept()
        await manejar_peticiones(reader, writer)

# Ejecutar el servidor y la simulación del motor en paralelo
async def main_program():
    task1 = asyncio.create_task(servidor())  # Servidor web
    task2 = asyncio.create_task(simular_motor())  # Motor simulado
    await asyncio.gather(task1, task2)

# Ejecutar el programa principal
asyncio.run(main_program())
