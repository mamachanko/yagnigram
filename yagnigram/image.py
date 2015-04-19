import math

from PIL import Image, ImageOps


class UnicodeImage(object):
    XTERM_GRAY_OFFSET = 232
    ADJUST_FACTOR = 1.5
    SCALE = 256/24.

    def __init__(self, image, width=100, height=57):
        self.original_image = image
        #self.ratio = .75 / .9
        #self.ratio = .5
        self.dimensions = (width, height)
        self.width, self.height = self.dimensions
        image = self.original_image.resize(self.dimensions, Image.BILINEAR)
        self.image = ImageOps.grayscale(image)
        self.pixels = self.image.load()

    @classmethod
    def from_filename(cls, filename, width=100, height=57):
        image = Image.open(filename)
        return cls(image, width=width, height=height)

    def __repr__(self):
        return '\n'.join(self.get_rows())

    def __unicode__(self):
        return u'\n'.join(self.get_rows())

    def get_rows(self):
        rows = self.as_array
        #height, width = len(rows), len(rows[0])
        #dimensions = '{} x {}'.format(height, width)
        #rows.insert(0, '{:^{width}}'.format(dimensions, width=width))
        return [u''.join(map(unicode, row)) for row in self.as_array]

    def get_pixel(self, x, y):
        return self.as_array[x][y]

    def get_pixel_row(self, x):
        return self.as_array[x]

    @property
    def array_dimensions(self):
        image_array = self.as_array
        return len(image_array), len(image_array[0])

    @property
    def as_array(self):
        try:
            return self._image_array
        except AttributeError:
            self._image_array = self._as_array()
            return self._image_array

    def _as_array(self):
        pixel_values = []
        image_array = []
        for y in range(self.height/4):
            row = []
            background_colour_before, text_colour_before = None, None
            for x in range(self.width/2):

                pixel_octet = []
                for i in range(8):
                    a = x * 2 + ((i & 4) >> 2)
                    b = y * 4 + (i & 3)
                    pixel = self.pixels[a, b]
                    pixel_values.append(pixel)
                    pixel_octet.append(pixel)

                pixel_octet_values = self.get_values_for_pixel_octet(
                    pixel_octet)
                background_color, text_color, braille_char = pixel_octet_values
                row.append(
                    UnicodePixel(braille_char, background_color, text_color)
                )

            image_array.append(row)

        return image_array

    def extract_gray_values(self, pixel_octet):
        lower_bound = self.encode_gray_value(min(pixel_octet))
        upper_bound = self.encode_gray_value(max(pixel_octet), ceil=True)

        return lower_bound, upper_bound

    def distance(self, v1, v2):
        return abs(v1 - v2)

    def encode_gray_value(self, gray_value, ceil=False):
        gray_value /= self.SCALE
        if ceil:
            gray_offset = int(math.ceil(gray_value))
        else:
            gray_offset = int(math.floor(gray_value))
        return self.XTERM_GRAY_OFFSET + gray_offset

    def decode_gray_value(self, gary_value):
        return int((gary_value - self.XTERM_GRAY_OFFSET) * self.SCALE)

    def get_values_for_pixel_octet(self, pixel_octet):
        background_color, maximum_gray = self.extract_gray_values(pixel_octet)

        gray_window = self.distance(maximum_gray, background_color)
        gray_value = gray_window * self.ADJUST_FACTOR
        text_color_offset = int(
            background_color + gray_value) - self.XTERM_GRAY_OFFSET
        text_color_offset = max(0, min(23, text_color_offset))
        text_color = self.XTERM_GRAY_OFFSET + text_color_offset

        braille_char = self.get_braille_char(pixel_octet,
                                             background_color,
                                             maximum_gray)

        return background_color, text_color, braille_char

    def get_braille_char(self, pixel_octet, background_color, maximum_gray):

        def make_dots(current, next):
            is_set = self.is_dot_set(pixel_octet[next],
                                     background_color,
                                     maximum_gray)
            return current | (is_set << next)

        braille_char = reduce(make_dots, range(8), 0)
        braille_char = self.dot(braille_char)

        return braille_char.encode('utf-8')

    def is_dot_set(self, gray_value, background_color, maximum_gray):
        background_color = self.decode_gray_value(background_color)
        maximum_gray = self.decode_gray_value(maximum_gray)

        if self.distance(background_color, maximum_gray) == 0:
            return True

        gray_window = self.distance(background_color, maximum_gray)
        gray_value_offset = self.distance(gray_value, background_color)
        gray_ratio = float(gray_value_offset) / gray_window
        x = math.exp(-gray_window * (gray_ratio - 0.5))
        normalised_distance = 1. / (x + 1)

        return .5 < normalised_distance

    def dot(self, bits):
        bits = (bits & 0b111) |\
               (bits & 0b1110000) >> 0b1 |\
               (bits & 0b1000) << 0b11 |\
               (bits & 0b10000000)
        return unichr(0x2800 + bits)


class UnicodePixel(object):

    def __init__(self, character, background_colour, character_colour):
        self.character = character.decode('utf-8')
        self.background_colour = background_colour
        self.character_colour = character_colour

    @property
    def ansii_sequence(self):
        return u'\033[48;5;{0}m\033[38;5;{1}m{2}\033[0m'.format(
            self.background_colour,
            self.character_colour,
            self.character)

    def __repr__(self):
        raise ValueError('cannot represent as ASCII')

    def __str__(self):
        return self.__str__()

    def __unicode__(self):
        return self.ansii_sequence
