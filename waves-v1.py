""" Display endless waves on the LED display.

    Note: The waves will slow down a lot once the offset reaches
    values above about 250. The offset is printed to the console.
    The script stops with a MemoryError when reaching an offset
    of 500.

    According to Damien George, the slow down is due to the math.sin()
    function starting to use different math to scale down the argument
    when it reaches 202. The memory error is due to a memory leak
    caused by the debug print().

    MAL 2016-01-06.

"""
import microbit
import math

# Array of LED brightness levels (0=off, 8=on); rows and columns
# correspond to the LEDs on the Microbit, e.g. leds[0][2] maps
# to the second LED in the first row.
leds = [[0] * 5 for i in range(5)]

def display_leds():
    
    for row in range(5):
        for column in range(5):
            # Note: The Microbit uses different indexing for LEDs
            microbit.display.set_pixel(column, row, leds[row][column])

def waves(delay):
    
    offset = 0
    while True:
        for row in range(5):
            for column in range(5):
                leds[row][column] = int(
                    math.sin((row + offset) / 4 * math.pi) * 4 + 4)
        display_leds()
        microbit.sleep(delay)
        offset += 1
        print ('Offset: %i' % offset)

waves(100)
