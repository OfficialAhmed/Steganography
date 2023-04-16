import binascii
from PIL import Image
from numpy import random

from lib.custom_key import Key

class TextIntoImage(Key):

    def __init__(self) -> None:
        self.altered_pixels = []


    def modify_pixel(self, value):
        """ 
            Modify a single RGB channel of a pixel
        """
        pixel_threshold = 128

        for _ in range(self.get_pixel_distance() + 1):
            if value % self.get_pixel_distance() == 1:
                return value
            
            if value >= pixel_threshold:
                value -= 1
            else:
                value += 1


    def modify_pixel_colors(self, red: int, green: int, blue: int) -> tuple:
        return map(self.modify_pixel, [red, green, blue])


    def normalize_and_hide(self, input_path: str, output_path: str, message: str):
        """
            Imag Normalization: 
                The purpose of this method is to produce some noise into a blank image 
                in order to help encode a secret message within it. without producing artifiacts
                By randomly modifying one of the RGB in a pixel, while encoding the message.
                To make it difficult for the naked eye to detect the difference within the image now.
        """
        img = Image.open(input_path)
        img = img.convert('RGB')
        
        size = img.size

        new_img = Image.new('RGB', size)

        base = 0
        HEX_BASE = 16
        hex_offset = [] # The pixels where msg will be encoded in

        for hex_char in self.to_hex(message):
            hex_offset.append(int(hex_char, HEX_BASE) + base)
            base += HEX_BASE

        hex_idx = 0 # ciphered msg tracker
        altered_pixels = []

        for column in range(img.size[1]):
            for row in range(img.size[0]):
                r, g, b = img.getpixel((row, column))

                # Normalize pixel if not in the hex offset, otherwise encode one single character
                current_pixel_index = row + column*img.size[0]
                if hex_idx < len(hex_offset) and hex_offset[hex_idx] == current_pixel_index:
                    r, g, b = self.modify_pixel_colors(r, g, b)
                    hex_idx += 1
                    altered_pixels.append((row, column))
                    
                else:
                    r, g, b = self.normalize_pixel(r, g, b)

                new_img.putpixel((row, column), (r, g, b))
                
        bits_left_to_encode = len(hex_offset) - len(altered_pixels)

        if bits_left_to_encode == 0:
            new_img.save(output_path, "PNG")
            return True
        return False
    

    def encode(self, input_image: str, normalized_image: str, ciphered_text: str) -> bool:
        result = self.normalize_and_hide(input_image, normalized_image, ciphered_text)

        return True if result else False


    def decode(self, image_path: str, key_file_name: str, pswd: str) -> str:
        decoded_key = self.get_key_from_file(key_file_name, pswd).split("_")
        self.set_pixel_distance(int(decoded_key[-1]))
        return self.read_text(image_path)


    def read_text(self, path: str) -> str:
        """ 
            read secret text from image 
        """

        img = Image.open(path)

        counter = 0
        result = []
        for column in range(img.size[1]):
            for row in range(img.size[0]):
                r, g, b = img.getpixel((row, column))
                if self.is_pixel_modified(r, g, b):
                    result.append(counter)
                counter += 1
                if counter == 16:
                    counter = 0
        return self.to_str(''.join([hex(_)[-1:] for _ in result]))


    def normalize_pixel(self, red: int, green: int, blue: int) -> tuple:
        """
            Randomly change the RGB pixel bits
        """
        if self.is_pixel_modified(red, green, blue):
            seed = random.randint(1, 4)
            if seed == 1:
                red = self.normalize_channel(red)
            if seed == 2:
                green = self.normalize_channel(green)
            if seed == 3:
                blue = self.normalize_channel(blue)
        return red, green, blue


    def normalize_channel(self, channel: int) -> int:
        """ 
            Averaging the pixle noise
            by Keeping pixel closer to threshold 128 which is the avg of pixel limit 255 
        """
        pixel_threshold = 128 # middle of 255 
        if channel >= pixel_threshold:
            channel -= 1
        else:
            channel += 1
        return channel


    def is_pixel_modified(self, red: int, green: int, blue: int) -> bool:
        """ 
            If RGB values divided by the DIST has remainder, the pixel contain a message bit
        """
        distance = self.get_pixel_distance()
        return red % distance == green % distance == blue % distance == 1


    def to_hex(self, input: str) -> str:
        return binascii.hexlify(input.encode()).decode()


    def to_str(self, input: str) -> str:
        return binascii.unhexlify(input).decode()



class ImageIntoImage:
    """
        Nasser Code is here
    """
    pass


