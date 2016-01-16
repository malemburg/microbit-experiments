""" Display a vivid snake on the LED display.

    You can press the left button to have the snake move faster,
    the right button to slow down things.

    MAL 2016-01-06.

"""
import microbit
import math

### Smart disply class

class SmartDisplay:

    # Array of LED brightness levels (0=off, 8=on); rows and columns
    # correspond to the LEDs on the Microbit, e.g. leds[0][2] maps
    # to the second LED in the first row.
    leds = None

    def __init__(self):

        self.clear()
    
    def clear(self):
        
        """ Clear the SmartDisplay.
        
        """
        self.leds = [bytearray(5) for i in range(5)]

    def display(self):
        
        """ Write the contents of the SmartDisplay to the
            MB image buffer and display it.
            
        """
        img_array = bytearray()
        for row in self.leds:
            img_array.extend(row)
        img = microbit.Image(5, 5, img_array)
        microbit.display.show(img)

    def set_dot(self, row, column, level=9):

        """ Set a single dot on the display to level.

            Does not clear the other content.

        """
        self.leds[row][column] = level

    def show_point(self, row, column, level=9, scale=5.0):
      
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
                leds[led_row][led_column] = int(
                    max(level - scale * d2, 0))

    def add(self, sd, offset_row=0, offset_column=0):
        
        """ Add the content of the other SmartDisplay to this one.
        
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
                # Make sure we don't overflow
                our_row[column] = min(
                    our_row[column] + other_row[other_column], 9)

    def dim(self, factor=0.5):
        
        """ Dim the SmartDisplay content by factor.
        
        """
        leds = self.leds
        for row in range(5):
            row = leds[row]
            for column in range(5):
                row[column] = round(row[column] * factor)

    def scroll_left(self, columns=1):
    
        """ Scroll the display to the left by the given number
            of columns (default is one).
        
        """
        leds = self.leds
        columns = min(columns, 5)
        filler = bytearray(columns)
        for row in range(5):
            leds[row] = leds[row][columns:] + filler

###

def snake(delay, segments=9):
    
    sd = SmartDisplay()
    while True:
        for i in range(segments):
            sd.scroll_left()
            sd.dim(0.8)
            x = i * 2*math.pi / segments
            y = math.sin(x)
            row = round(2 + 2 * y)
            sd.set_dot(row, 4)
            sd.display()
            microbit.sleep(delay)
        if microbit.button_a.is_pressed():
            delay = max(0, delay - 10)
        if microbit.button_b.is_pressed():
            delay += 10

snake(100)
