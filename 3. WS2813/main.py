import machine
import neopixel

pixels = neopixel.NeoPixel(machine.Pin(16), 8)

colours = "00FFF0"

c0 = int("0x" + colours[0 : 2])
c1 = int("0x" + colours[2 : 4])
c2 = int("0x" + colours[4 : 6])

colour = (c0, c1, c2)
 
pixels.fill(colour)
pixels.write()