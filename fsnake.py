""" Display a vivid snake on the LED display.

    You can press the left button to have the snake move faster,
    the right button to slow down things.

    This version using floating point numbers for the dots
    which allows for a nice fading tail.

    MAL 2016-01-07.

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

    def show_point(self, row, column, level=1.0, scale=5.0):
      
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

def snake(delay, segments=9):
    
    fd = FloatDisplay()
    while True:
        for i in range(segments):
            fd.scroll_left()
            fd.dim(0.9)
            x = i * 2*math.pi / segments
            y = math.sin(x)
            row = round(2 + 2 * y)
            fd.set_dot(row, 4)
            fd.display()
            microbit.sleep(delay)
        if microbit.button_a.is_pressed():
            delay = max(0, delay - 10)
        if microbit.button_b.is_pressed():
            delay += 10

snake(100)
