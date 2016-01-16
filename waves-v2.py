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
leds = [[0] * 5 for i in range(5)]

def display_leds_image_string():

    # Timing: 72912 ms for 1000 iterations
    img_string = '\n'.join(''.join('%i' % column
                                    for column in row)
                            for row in leds)
    img = microbit.Image(img_string)
    microbit.display.show(img)

def display_leds_image_array():
    
    # Timing: 30420 ms for 1000 iterations
    img_array = bytearray()
    for row in leds:
        img_array.extend(bytearray(row))
    img = microbit.Image(5, 5, img_array)
    microbit.display.show(img)

def display_leds_set_pixel():
    
    # Timing: 35358 ms for 1000 iterations
    for row in range(5):
        for column in range(5):
            # Note: The Microbit uses different indexing for LEDs
            microbit.display.set_pixel(column, row, leds[row][column])

#display_leds = display_leds_image_string
display_leds = display_leds_image_array
#display_leds = display_leds_set_pixel

def waves(delay):
    
    for offset in range(1000):
        for row in range(5):
            for column in range(5):
                x = (row + offset) % 8 / 4 * math.pi
                leds[row][column] = int(
                    math.sin(x) * 4 + 4)
        display_leds()
        microbit.sleep(delay)
        offset += 1
        #print ('Offset: %i' % offset)
        #print ('Offset: {}'.format(offset))
        if microbit.button_a.is_pressed():
            delay = max(0, delay - 10)
        if microbit.button_b.is_pressed():
            delay += 10

#waves(100)
t0 = microbit.running_time()
waves(0)
t1 = microbit.running_time()
print ('Ran for %i ms' % (t1 - t0))
