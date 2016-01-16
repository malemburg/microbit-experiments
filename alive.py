""" Display a heartbeat on the LED display.

    You can press the left button to get the MB more excited,
    the right button to calm things down.

    MAL 2016-01-06.

"""
import microbit
import math

# Array of LED brightness levels (0=off, 8=on); rows and columns
# correspond to the LEDs on the Microbit, e.g. leds[0][2] maps
# to the second LED in the first row.
leds = tuple(bytearray(5) for i in range(5))

def display_leds():
    
    img_array = bytearray()
    for row in leds:
        img_array.extend(row)
    img = microbit.Image(5, 5, img_array)
    microbit.display.show(img)

def set_point(row, column, level=9, scale=5.0):

    for led_row in range(5):
        for led_column in range(5):
            d2 = (row - led_row)**2.0 + (column - led_column)**2.0
            leds[led_row][led_column] = int(max(level - scale * d2, 0))

def heartbeat(delay):
    
    while True:
        for i in range(10):
            set_point(2, 2, scale=(i + 1)/2)
            display_leds()
            microbit.sleep(delay)    
        if microbit.button_a.is_pressed():
            delay = max(0, delay - 10)
        if microbit.button_b.is_pressed():
            delay += 10

heartbeat(100)
