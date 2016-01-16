""" Display endless waves on the LED display.

    You can press the left button to have the waves go faster,
    the right button to slow down things.

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

def waves(delay):
    
    offset = 0
    while True:
        for row in range(5):
            x = (row + offset) % 8 / 4 * math.pi
            level = int(math.sin(x) * 4 + 4)
            for column in range(5):
                leds[row][column] = level
        display_leds()
        microbit.sleep(delay)
        offset += 1
        if microbit.button_a.is_pressed():
            delay = max(0, delay - 10)
        if microbit.button_b.is_pressed():
            delay += 10

waves(175)
