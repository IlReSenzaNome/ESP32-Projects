from machine import Pin, PWM
import time
import bluetooth
import BLE

# Configuración de Bluetooth
name = 'ESP32 - L293D'
ble = bluetooth.BLE()
uart = BLE.BLEUART(ble, name)

# Configuración de pines
ENABLE1_PIN = 32  
INPUT1_PIN = 33   
INPUT2_PIN = 25   

enable1 = PWM(Pin(ENABLE1_PIN), freq=1000)  
input1 = Pin(INPUT1_PIN, Pin.OUT)           
input2 = Pin(INPUT2_PIN, Pin.OUT)           

# Función para controlar la dirección y velocidad del motor
def motor_control(direction, speed):
    duty = int((speed / 100) * 1023)  # Convertir porcentaje a ciclo de trabajo
    print(f"[MOTOR] Dirección: {direction}, Velocidad: {speed}%")

    if direction == "left":
        input1.value(1)
        input2.value(0)
    elif direction == "right":
        input1.value(0)
        input2.value(1)
    else:
        input1.value(0)
        input2.value(0)

    enable1.duty(duty)

# Función para manejar datos recibidos por Bluetooth
def on_rx():
    rx_buffer = uart.read().decode().strip().replace("\x00", "")  # Eliminar caracteres nulos
    print("[BLUETOOTH] Comando recibido:", rx_buffer)
    uart.write(f'ESP32 recibió: {rx_buffer}\n')

    # Comprobar el comando recibido y actuar en consecuencia
    if rx_buffer == "left":
        motor_control("left", 50)
    elif rx_buffer == "right":
        motor_control("right", 50)
    elif rx_buffer == "stop":
        motor_control("stop", 0)
    else:
        print("[ERROR] Comando no válido:", rx_buffer)
        uart.write("Comando no válido\n")


# Configurar interrupciones Bluetooth
uart.irq(handler=on_rx)

# Función para realizar una prueba del Bluetooth
def test_bluetooth():
    print("[TEST] Iniciando prueba de Bluetooth...")
    uart.write("[TEST] Bluetooth inicializado. Por favor, responde con cualquier mensaje.\n")
    print("[TEST] Esperando respuesta por Bluetooth durante 10 segundos...")
    start_time = time.ticks_ms()

    while time.ticks_diff(time.ticks_ms(), start_time) < 10000:
        if uart.any():
            rx_test = uart.read().decode().strip()
            print("[TEST] Respuesta recibida:", rx_test)
            uart.write(f"[TEST] Respuesta recibida correctamente: {rx_test}\n")
            return
    
    print("[TEST] No se recibió respuesta dentro del tiempo esperado.")
    uart.write("[TEST] No se recibió respuesta.\n")

# Función principal
def main():
    print("[SYSTEM] Sistema iniciado. Configuración completa.")
    test_bluetooth()  # Realizar la prueba de Bluetooth

    try:
        while True:
            time.sleep(1)  # Mantener el bucle activo para recibir comandos
            print("[STATUS] Esperando comandos por Bluetooth...")
    except KeyboardInterrupt:
        print("[SYSTEM] Interrupción detectada. Deteniendo motor...")
        motor_control("stop", 0)
        print("[SYSTEM] Motor detenido. Saliendo del sistema...")

# Punto de entrada
if __name__ == "__main__":
    main()
