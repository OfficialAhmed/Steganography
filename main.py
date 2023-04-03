from lib import custom_steganography, custom_cipher, custom_key
from time import perf_counter

def main() -> None:
    algo_type = input("e or d: ")
    key = custom_key.Key()
    key.set_globals()
    steg = custom_steganography.TextIntoImage()
    cipher = custom_cipher.SubstitutionCipher()

    if algo_type == "e":
        # encode 
        input_image = "assets\\cover_image.png"
        output_image = "assets\\output_image.png"
        text = input("Enter secret Msg: ")

        print("Encrypting...")
        encrypted = cipher.substitution_cipher_enc(text)

        print("Encoding...")
        t1 = perf_counter()
        steg.encode(input_image, output_image, encrypted)
        print(f"Finished Encoding in {perf_counter()-t1}")

    
    else:
        # decode
        input_image = "assets\\output_image.png"
        key_name = input("enter the key file name [without extension]: ")

        print("Decoding ...")
        try:
            text_from_image = steg.decode(input_image, key_name)
            if text_from_image:
                hex_value = eval(text_from_image)
                print(f"SECRET MESSAGE: {cipher.substitution_cipher_dec(hex_value)}")
            else:
                print("UNABLE TO FIND MESSAGE!")
        except Exception as e:
            print(f"UNABLE TO DECRYPT MESSAGE!: {e}")

            
if __name__ == "__main__":
    main()
