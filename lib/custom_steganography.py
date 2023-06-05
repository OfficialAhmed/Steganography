import os, cv2, binascii
import numpy as np
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
                in order to help encode a secret message within it. without producing artifiacts
                By randomly modifying one of the RGB channel, while encoding the message.
                To make it seamless and difficult for the human eye to detect the difference within the image.
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
        if channel >= 128:
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

    def __init__(self) -> None:
		
        self.temp_location = "assets\\image2image\\"

        self.ENCODED_NAME = f'{self.temp_location}encoded_image.jpg'
        self.DECODED_COVER = f'{self.temp_location}decoded_cover.jpg'
        self.DECODED_HIDDEN = f'{self.temp_location}decoded_hidden.jpg'

        self.COMPRESS_COVER_OUTPUT = f'{self.temp_location}cover_compressed.jpg'
        self.COMPRESS_HIDDEN_OUTPUT = f'{self.temp_location}hidden_compressed.jpg'

        self.cover_width = 0
        self.cover_height = 0
        self.compression_in_fraction = None


    def set_compression(self, compression: int):
        self.compression_in_fraction = compression / 100


    def compress_cover_image(self, cover):	
		# Reduce cover image size and creates one image: compressed cover image

        SIZE_1 = 1034	
        SIZE_2 = 900	
        SIZE_3 = 700	
        SIZE_4 = 500	
        SIZE_5 = 250	

        pic = Image.open(cover)
        width, height = pic.size

		
        if self.compression_in_fraction == 1:

            if width > 1000 and height > 1000:

                new_width = SIZE_1
                new_height = int(height * (SIZE_1 / width))

            elif( width  >= 1000 or height >= 1000):  

                new_width = SIZE_2
                new_height = int(height * (SIZE_2 / width)) 

            elif(500 < width < 1000 and 500 < height < 1000 ) or (500 < width < 1000 or 500 < height < 1000 ) :

                new_width = SIZE_3
                new_height = int(height * (SIZE_3 / width))

            elif(250 <= width <=500 and 250 <= height <=500 ) or (250 <= width <=500 or 250 <= height <=500 ) :

                new_width = SIZE_4
                new_height = int(height * (SIZE_4 / width))

            else:

                new_width = SIZE_5
                new_height = int(height * (SIZE_5 / width))

        else:

            new_width = int(width * self.compression_in_fraction)
            new_height = int(height * self.compression_in_fraction)

        self.cover_width = new_width
        self.cover_height = new_height

        pic = pic.resize((new_width, new_height), Image.ANTIALIAS)
        pic.save(self.COMPRESS_COVER_OUTPUT)
		

    def compress_hidden_image(self, image):
		# Compress and greyscale the hidden image

        hidden_image = Image.open(image)

        # hidden image will be resized using the cover dimensions
        hidden_image = hidden_image.resize((self.cover_width, self.cover_height), Image.ANTIALIAS)
        hidden_image = hidden_image.convert('L')
        hidden_image.save(self.COMPRESS_HIDDEN_OUTPUT)


    def encrypt(self) -> bool:

        cover = cv2.imread(self.COMPRESS_COVER_OUTPUT)
        hidden = cv2.imread(self.COMPRESS_HIDDEN_OUTPUT)

        # Generate a random sequence of pixel positions
        positions = [(i, j) for i in range(hidden.shape[0]) for j in range(hidden.shape[1])]
        random.shuffle(positions)

        for idx, (i, j) in enumerate(positions):
            for l in range(3):
                v1 = format(cover[i][j][l], '08b')
                v2 = format(hidden[i][j][l], '08b')
                v3 = v1[:4] + v2[:4]
                cover[i][j][l] = int(v3, 2)

                # Check if we have embedded all the hidden data
                if idx == hidden.shape[0] * hidden.shape[1] - 1:
                    break

            if idx == hidden.shape[0] * hidden.shape[1] - 1:
                break

        return cv2.imwrite(self.ENCODED_NAME, cover)
			

    def decrypt(self, image_to_decode) -> bool:		

        image = cv2.imread(image_to_decode)
        width, height = image.shape[0], image.shape[1]
        cover = np.zeros((width, height, 3), np.uint8)
        hidden = np.zeros((width, height, 3), np.uint8)

        # Generate the same random sequence of pixel positions
        positions = [(i, j) for i in range(hidden.shape[0]) for j in range(hidden.shape[1])]
        random.shuffle(positions)

        for idx, (i, j) in enumerate(positions):
            for l in range(3):
                v1 = format(image[i][j][l], '08b')
                v2 = v1[:4] + chr(random.randint(0, 1) + 48) * 4
                v3 = v1[4:] + chr(random.randint(0, 1) + 48) * 4
                cover[i][j][l] = int(v2, 2)
                hidden[i][j][l] = int(v3, 2)

                # Check if we have extracted all the hidden data
                if idx == hidden.shape[0] * hidden.shape[1] - 1:
                    break

            if idx == hidden.shape[0] * hidden.shape[1] - 1:
                break
        
        if cv2.imwrite(self.DECODED_COVER, cover) and cv2.imwrite(self.DECODED_HIDDEN, hidden):
            return True
        return False
        

    def delete_temp_images(self):
        #  Remove all temp images generated during the encoding process 
        temp = ( self.COMPRESS_COVER_OUTPUT, self.COMPRESS_HIDDEN_OUTPUT )

        try:
            for i in temp:
                os.remove(i)
        except Exception as e:
            # If cannot remove ignore it
            pass
            