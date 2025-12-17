# interrupt_repl.py
import serial, time

PORT = "COM3"
BAUD = 115200

s = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(1)
# enviar Ctrl-C
s.write(b'\x03')
time.sleep(0.2)
# pedir lista de archivos
s.write(b"import os\nprint(os.listdir())\n")
time.sleep(0.8)
out = s.read_all()
print(out.decode(errors='ignore'))
s.close()