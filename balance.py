""" Display a rain drop on the LED display you can balance by
    moving the microbit.

    You can press the left button to decrease the speed with which
    the drop moves, the right button to increase the speed.

    If you press the left button long enough, the speed of
    the drop will become negative, inversing the direction
    of the drop when moving the microbit.

    MAL 2016-01-17.

"""
import microbit
import math

### Float display class

class FloatDisplay:

    # Array of floating point LED brightness levels (0.0=off, 1.0=on);
    # rows and columns correspond to the LEDs on the Microbit, e.g. 
    # leds[0][2] maps to the second LED in the first row.
    leds = None

    def __init__(self):

        self.clear()
    
    def clear(self):
        
        """ Clear the SmartDisplay.
        
        """
        self.leds = [[0.0]*5 for i in range(5)]

    def display(self):
        
        """ Write the contents of the SmartDisplay to the
            MB image buffer and display it.

            The method applies clipping to keep the brightness
            values within the permitted range.

        """
        img_array = bytearray()
        local_int = int
        for row in self.leds:
            for x in row:
                x = local_int(x * 9.0)
                if x < 0:
                    x = 0
                elif x > 9:
                    x = 9
                img_array.append(x)
        img = microbit.Image(5, 5, img_array)
        microbit.display.show(img)

    def set_dot(self, row, column, level=1.0):

        """ Set a single dot on the display to level.

            Does not clear the other content.

        """
        self.leds[row][column] = level

    def show_point(self, row, column, level=1.0, scale=1.0):
      
        """ This works with floating point row and column and
            interpolates the brightness.
            
            All other display content is cleared.
            
        """
        leds = self.leds
        for led_row in range(5):
            for led_column in range(5):
                # Calculate the squared distance
                d2 = (row - led_row)**2.0 + (column - led_column)**2.0
                # Set brightness based on the distance to the point,
                # using scale for scaling
                leds[led_row][led_column] = level - scale * d2

    def add(self, sd, offset_row=0, offset_column=0):
        
        """ Add the content of the other SmartDisplay to this one.
    
            No overflow checks are done on the values to avoid
            clipping in case additional operations are applied.

        """
        leds = self.leds
        for row in range(5):
            # Make sure we keep within the display bounds
            if offset_row:
                other_row_index = row + offset_row
                if (other_row_index > 4 or 
                    other_row_index < 0):
                    continue
            else:
                other_row_index = row
            our_row = leds[row]
            other_row = sd.leds[other_row_index]
            for column in range(5):
                # Make sure we keep within the display bounds
                if offset_column:
                    other_column = column + offset_column
                    if (other_column > 4 or 
                        other_column < 0):
                        continue
                else:
                    other_column = column
                our_row[column] = (
                    our_row[column] + other_row[other_column])

    def dim(self, factor=0.5):
        
        """ Dim the SmartDisplay content by factor.
        
        """
        leds = self.leds
        for row in range(5):
            row = leds[row]
            for column, x in enumerate(row):
                row[column] *= x * factor

    def scroll_left(self, columns=1, fill_value=0.0):
    
        """ Scroll the display to the left by the given number
            of columns (default is one).
        
        """
        leds = self.leds
        columns = min(columns, 5)
        filler = [fill_value] * columns
        for row in range(5):
            leds[row] = leds[row][columns:] + filler

    def scroll_right(self, columns=1, fill_value=0.0):
    
        """ Scroll the display to the right by the given number
            of columns (default is one).
        
        """
        leds = self.leds
        columns = min(columns, 5)
        filler = [fill_value] * columns
        for row in range(5):
            leds[row] = filler + leds[row][:-columns]

###

def balance(speed):
    x, y, z = 2.0, 2.0, 0.0
    speed = 1.0
    fd = FloatDisplay()
    while True:
        ax, ay, az = microbit.accelerometer.get_values()
        x += (ax / 1024.0) * speed
        if x > 4.0:
            x = 4.0
        if x < 0.0:
            x = 0.0
        y += (ay / 1024.0) * speed
        if y > 4.0:
            y = 4.0
        if y < 0.0:
            y = 0.0
        #z += (az / 1024.0) * speed
        #print ('x:%4f y:%4f z:%4f ax:%4i ay:%4i az:%4i speed:%4f' % (
        #        x, y, z, ax, ay, az, speed))
        fd.clear()
        fd.show_point(y, x, scale=0.75)
        fd.display()
        #microbit.sleep(delay)
        if microbit.button_a.is_pressed():
            speed -= 0.01
            speed = max(-4.0, speed)
        if microbit.button_b.is_pressed():
            speed += 0.01
            speed = min(4.0, speed)

balance(0.5)
