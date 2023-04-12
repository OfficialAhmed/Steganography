import secrets
import datetime
from numpy import random
from lib.custom_aes import AESCipher as AES

class Key:
    """
        - Parent Class handle Key encryption and decryption
        - PIXEL_DISTANCE: A pixel will be modified if the remainder of its RGB values divided by PIXEL_DISTANCE is equal to 1
            > PIXEL_DISTANCE = 5 
            > RGB = (100, 105, 110) -> To be modified 
            > RGB = (100, 105, 103) -> To be ignored because 103 not divisible by PIXEL_DISTANCE 
        - Without the right encoded PIXEL_DISTANCE the message cannot be retrived 
    """

    # Global vars for class childs
    SECRET_KEY = ""
    PIXEL_DISTANCE = 0
    DEC_KEY = ""


    def __init__(self) -> None:
        self.decrypted_key = ""
    

    def set_globals(self) -> None:
        """ 
            init only once to have the same values for all children classes 
        """
        Key.PIXEL_DISTANCE = self.generate_pixel_distance()
        Key.SECRET_KEY = self.generate_secret_key()


    def get_secret_key(self) -> str:
        return Key.SECRET_KEY
    

    def get_pixel_distance(self) -> int:
        return Key.PIXEL_DISTANCE


    def set_pixel_distance(self, distance: int):
        Key.PIXEL_DISTANCE = distance


    def generate_pixel_distance(self) -> int:
        return random.randint(5, 21)
    

    def get_decrypted_key(self) -> str:
        return Key.DEC_KEY
    

    def set_decrypted_key(self, k):
        Key.DEC_KEY = k
    

    def generate_secret_key(self, key_length: int = 12) -> str:
        """ 
            Randomly generate a key of length 12 for shifting letters, and 1 number for pixel distance

            Note: for extra layer of security 'secrets lib' used for hardware random number generator (HRNG)
            over pseudorandom number generator (PRNG) 
            ASCII random range (10 - 255) 
        """
        return "".join([f"{secrets.randbelow(245) + 10}_" for _ in range(key_length)]) + str(self.get_pixel_distance())


    def store_secret_key(self, pswd: str) -> bool:
        """
            Encrypt key with (PBE) AES algo. then save it as .key extension
        """
        now = datetime.datetime.now()
        timestamp = now.strftime("%m_%d %H_%M_%S")

        with open(f"{timestamp}.bin", "wb") as file:

            aes = AES(pswd)
            encrypted_text = aes.encrypt(self.get_secret_key())
            file.write(encrypted_text.encode())
    

    def get_key_from_file(self, key_file_name: str, pswd: str) -> str:
        """
            Decrypt key AES and return the plainText
        """
        with open(f'{key_file_name}.bin', 'rb') as file:

            encrypted_text = file.read().decode()
            aes = AES(pswd)
            decrypted_text = aes.decrypt(encrypted_text)

            if decrypted_text:
                self.set_decrypted_key(decrypted_text)
                return decrypted_text
            
        return "UNABLE TO RETRIEVE MESSAGE!"
