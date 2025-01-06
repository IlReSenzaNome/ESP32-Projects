from machine import Pin
import utime

a = Pin(22, Pin.OUT)
b = Pin(21, Pin.OUT)
c = Pin(19, Pin.OUT)
d = Pin(18, Pin.OUT)
e = Pin(5, Pin.OUT)
f = Pin(4, Pin.OUT)
g = Pin(2, Pin.OUT)

def Ssegmentos(A, B, C, D, E, F, G):
    a.value(A)
    b.value(B)
    c.value(C)
    d.value(D)
    e.value(E)
    f.value(F)
    g.value(G)

numeros = [
    (1, 1, 1, 1, 1, 1, 0),  # 0
    (0, 1, 1, 0, 0, 0, 0),  # 1
    (1, 1, 0, 1, 1, 0, 1),  # 2
    (1, 1, 1, 1, 0, 0, 1),  # 3
    (0, 1, 1, 0, 0, 1, 1),  # 4
    (1, 0, 1, 1, 0, 1, 1),  # 5
    (1, 0, 1, 1, 1, 1, 1),  # 6
    (1, 1, 1, 0, 0, 0, 0),  # 7
    (1, 1, 1, 1, 1, 1, 1),  # 8
    (1, 1, 1, 1, 0, 1, 1),  # 9
]

letras = {
    "S": (1, 0, 1, 1, 0, 1, 1),  # S
    "H": (0, 1, 1, 0, 1, 1, 1),  # H
    "I": (0, 1, 1, 0, 0, 0, 0),  # I
    "G": (1, 1, 1, 1, 1, 0, 1),  # G
    "U": (0, 1, 1, 1, 1, 1, 0),  # U
}

while True:
    # Mostrar números del 0 al 9
    for num in numeros:
        Ssegmentos(*num)
        utime.sleep_ms(1200)

    # Mostrar el nombre "SHIGU"
    for letra in "SHIGU":
        Ssegmentos(*letras[letra])
        utime.sleep_ms(1200)
