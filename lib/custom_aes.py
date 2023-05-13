from Crypto.Cipher import AES
import base64

class AESCipher:
    """
        Password-based encryption (PBE)
        Encrypting and decrypting a plaintext using only a password provided by the user 
    """

    def __init__(self, user_password: str) -> None:
        
        self.key = user_password.encode('utf-8')
        self.block_size = AES.block_size


    def encrypt(self, plaintext: str) -> str:

        plaintext_in_bytes = plaintext.encode('utf-8')
        plaintext_padded = plaintext_in_bytes + (self.block_size - len(plaintext_in_bytes) % self.block_size) * b"\0"
        cipher = AES.new(self.key, AES.MODE_ECB)
        ciphertext = cipher.encrypt(plaintext_padded)

        return base64.b64encode(ciphertext).decode('utf-8')


    def decrypt(self, ciphertext: str) -> str:

        try:

            ciphertext_in_bytes = base64.b64decode(ciphertext.encode('utf-8'))
            cipher = AES.new(self.key, AES.MODE_ECB)
            plaintext_padded = cipher.decrypt(ciphertext_in_bytes)
            plaintext = plaintext_padded.rstrip(b"\0").decode("utf-8", "ignore")

            return plaintext
        
        except: return ""
