import network
import socket
import time

# Configuración del modo Access Point
def iniciar_ap():
    ap = network.WLAN(network.AP_IF)
    ap.config(essid='ESP32_AP', password='1234567890')  # Cambia el nombre y la contraseña si lo deseas
    ap.active(True)
    ap.ifconfig(('192.168.100.1', '255.255.255.0', '192.168.100.1', '8.8.8.8'))  # Establece la IP estática
    print("Modo AP iniciado. Dirección IP:", ap.ifconfig()[0])
    return ap

# Verificar si el ESP32 ya está conectado a una red WiFi
def verificar_conexion_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if wlan.isconnected():
        print("Ya está conectado a la red WiFi:", wlan.ifconfig()[0])
        return True
    return False

# Función para crear una página web con escáner de QR
def crear_web():
    html = """
    <html>
        <head>
            <title>Conectar a WiFi</title>
            <script src="https://cdn.jsdelivr.net/npm/jsqr/dist/jsQR.js"></script>
            <script>
                function iniciarEscaneo() {
                    var video = document.createElement("video");
                    document.body.appendChild(video);
                    navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
                    .then(function(stream) {
                        video.srcObject = stream;
                        video.setAttribute("playsinline", true); // Requerido para iOS
                        video.play();
                        requestAnimationFrame(scanQRCode);
                    });
                    
                    function scanQRCode() {
                        if (video.readyState === video.HAVE_ENOUGH_DATA) {
                            var canvas = document.createElement("canvas");
                            var context = canvas.getContext("2d");
                            canvas.height = video.videoHeight;
                            canvas.width = video.videoWidth;
                            context.drawImage(video, 0, 0, canvas.width, canvas.height);
                            var imageData = context.getImageData(0, 0, canvas.width, canvas.height);
                            var code = jsQR(imageData.data, canvas.width, canvas.height, {
                                inversionAttempts: "dontInvert",
                            });
                            if (code) {
                                alert("Código QR detectado: " + code.data);
                                var qrData = code.data;
                                var form = document.getElementById('wifi-form');
                                var input = document.createElement('input');
                                input.type = 'hidden';
                                input.name = 'qr_data';
                                input.value = qrData;
                                form.appendChild(input);
                                form.submit();
                                video.srcObject.getTracks().forEach(track => track.stop()); // Detener la cámara
                            } else {
                                requestAnimationFrame(scanQRCode);
                            }
                        } else {
                            requestAnimationFrame(scanQRCode);
                        }
                    }
                }
            </script>
        </head>
        <body>
            <h1>Escanea el código QR para conectarte a una red WiFi</h1>
            <button onclick="iniciarEscaneo()">Iniciar escaneo de QR</button>
            <form id="wifi-form" action="/conectar" method="POST">
                <p>Escanea un código QR y se conectará automáticamente.</p>
            </form>
        </body>
    </html>
    """
    return html

# Función para manejar la solicitud de conexión a WiFi
def manejar_conexion(request):
    if "qr_data" in request:
        qr_data = request["qr_data"]
        ssid, password = qr_data.split(",")  # Asume que el QR tiene el formato: SSID,Contraseña
        conectar_wifi(ssid, password)
        return "<html><body><h1>Conectado correctamente!</h1></body></html>"
    return "<html><body><h1>Error en el QR</h1></body></html>"

# Conectar a una red WiFi con SSID y contraseña
def conectar_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando a la red WiFi...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(1)
        print('Conectado a la red WiFi:', ssid)
        print('Dirección IP:', wlan.ifconfig()[0])

# Crear el servidor HTTP
def iniciar_servidor():
    addr = socket.getaddrinfo('192.168.100.1', 80)[0][-1]  # Servir la página en 192.168.100.1
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('Escuchando en', addr)
    while True:
        cl, addr = s.accept()
        print('Cliente conectado desde', addr)
        request = cl.recv(1024)
        request = str(request)
        
        if '/conectar' in request:
            # Extraer los datos del formulario (qr_data)
            qr_data = request.split('qr_data=')[1].split('&')[0]
            respuesta = manejar_conexion({'qr_data': qr_data})
            cl.send('HTTP/1.1 200 OK\r\n')
            cl.send('Content-Type: text/html\r\n\r\n')
            cl.send(respuesta)
        else:
            cl.send('HTTP/1.1 200 OK\r\n')
            cl.send('Content-Type: text/html\r\n\r\n')
            cl.send(crear_web())
        
        cl.close()

# Función principal que controla la lógica de conexión
def main():
    if verificar_conexion_wifi():
        print("Conectado a WiFi, no es necesario crear un AP.")
        return
    else:
        print("No conectado a ninguna red WiFi. Creando un AP...")
        iniciar_ap()
        iniciar_servidor()

# Ejecutar la función principal
main()