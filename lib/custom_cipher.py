from lib.custom_key import Key

class SubstitutionCipher(Key):
    """ 
        Polyalphabetic Substitution Cipher Encryption-Decryption using a key of different shifting number for each letter
        limit: length no more than 1-byte or 255-bits ascii
    """
    
    def __init__(self) -> None:
        pass


    def substitution_cipher_dec(self, message: str) -> str:

        result = ""
        key_index = 0

        decoded_key = self.get_decrypted_key().split("_")
        key = decoded_key[:-1]

        # To be able to read the right pixels to decode the msg
        # we store the number in pixel distance from the key
        self.pixel_distance = decoded_key[-1]

        for char in message:
            shifted_number = (ord(char) - int(key[key_index]))
            
            # Shifting range (0-256) = 1-byte only
            shifted_number %= 256
            char = chr(shifted_number)

            result += char
            key_index = (key_index + 1) % len(key)

        return repr(result)


    def substitution_cipher_enc(self, message: str, pswd: str) -> str:

        result = ""
        key_index = 0
        key = self.get_secret_key().split("_")[:-1]

        for char in message:
            shifted_number = (ord(char) + int(key[key_index]))
            
            # Shifting range (0-256) = 1-byte only
            shifted_number %= 256
            char = chr(shifted_number)

            result += char
            key_index = (key_index + 1) % len(key)

        self.store_secret_key(pswd)

        return repr(result)
    
