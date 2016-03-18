#!/usr/bin/python
"""
    Utility to detect the source code encoding of a Python file.

    Supports Python 2.7 and 3.

    Copyright (c) 2016, Marc-Andre lemburg; mailto:mal@lemburg.com
    See the documentation for further information on copyrights,
    or contact the author. All Rights Reserved.

    License: MIT

"""
import sys
import re

# Debug output ?
_debug = True

# PEP 263 RE
PEP263 = re.compile(b'^[ \t]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)',
                    re.MULTILINE)

# Default to assume in case no encoding is given
DEFAULT_ENCODING = sys.getdefaultencoding()

# UTF-8 BOM
UTF8_BOM = b'\xef\xbb\xbf'

###

def detect_source_encoding(code, buffer_size=400):

    """ Detect and return the source code encoding of the Python code
        given in code.
        
        code must be given as bytes.
        
        The function uses a buffer to determine the first two code lines
        with a default size of 400 bytes/code points.  This can be adjusted
        using the buffer_size parameter.
        
    """
    # Get the first two lines
    first_two_lines = b'\n'.join(code[:buffer_size].splitlines()[:2])
    # BOMs override any source code encoding comments
    if first_two_lines.startswith(UTF8_BOM):
        return 'utf-8-sig'
    # .search() picks the first occurrence
    m = PEP263.search(first_two_lines)
    if m is None:
        return DEFAULT_ENCODING
    return m.group(1).decode('ascii')

# Tests

def _test():

    l = (
  (b"""\
# No encoding
""", DEFAULT_ENCODING),
  (b"""\
# coding: latin-1
""", 'latin-1'),
  (b"""\
#!/usr/bin/python
# coding: utf-8
""", 'utf-8'),
  (b"""\
coding=123
# The above could be detected as source code encoding
""", DEFAULT_ENCODING),
  (b"""\
# coding: latin-1
# coding: utf-8
""", 'latin-1'),
  (b"""\
# No encoding on first line
# No encoding on second line
# coding: utf-8
""", DEFAULT_ENCODING),
  (UTF8_BOM + b"""\
# No encoding
""", 'utf-8-sig'),
  (UTF8_BOM + b"""\
# BOM and encoding
# coding: utf-8
""", 'utf-8-sig'),
  (UTF8_BOM + b"""\
# BOM and wrong encoding
# coding: latin-1
""", 'utf-8-sig'),
    )
    for code, encoding in l:
        if _debug:
            print ('=' * 72)
            print ('Checking:')
            print ('-' * 72)
            print (code.decode('latin-1'))
            print ('-' * 72)
        detected_encoding = detect_source_encoding(code)
        if _debug:
            print ('detected: %s, expected: %s' % 
                   (detected_encoding, encoding))
        assert detected_encoding == encoding
        # Check that the code compiles
        try:
            compile(code, 'stdin', 'exec')
        except SyntaxError:
            if encoding == 'utf-8-sig':
                pass


if __name__ == '__main__':
    _test()
