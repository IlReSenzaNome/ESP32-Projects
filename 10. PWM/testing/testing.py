# test_serial_open.py
import serial
PORT="COM3"
try:
    s = serial.Serial(PORT, 115200, timeout=1)
    print("Abierto", PORT)
    s.close()
except Exception as e:
    print("ERROR:", repr(e))