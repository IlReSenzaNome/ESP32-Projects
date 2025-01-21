import math
import time
from machine import Pin, DAC

# Configuración del DAC en el pin 25 (puedes usar pin 26 también)
dac = DAC(Pin(25))

# Parámetros de la señal sinusoidal
frecuencia = 1  # Frecuencia de la señal sinusoidal en Hz
amplitud = 255  # Amplitud máxima para DAC (0-255 para 8 bits)
offset = 128     # Desplazamiento (para que la onda no sea negativa)

# Tiempo de muestreo (intervalo entre muestras)
sample_rate = 20  # Muestras por segundo (0.01 s entre muestras)

# Generar la señal sinusoidal y controlar la intensidad del LED
while True:
    for i in range(360):  # 360 grados en una vuelta
        angulo = math.radians(i)
        valor_seno = math.sin(angulo)
        valor_dac = int(amplitud * (valor_seno + 1) / 2)  # Normaliza a 0-255
        dac.write(valor_dac)
        time.sleep(1 / sample_rate)
