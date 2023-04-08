# FIXME: Need to retrieve image path to use it, the name is not enough.

import eel
from lib import custom_steganography, custom_cipher, custom_key
from time import perf_counter

steg = custom_steganography.TextIntoImage()
cipher = custom_cipher.SubstitutionCipher()
eel.init('interface')

@eel.expose
def encode(text: str, input_image: str, user_enc_pswd: str):
    global steg, cipher

    output_image = "output_image.png"
    key = custom_key.Key()
    key.set_globals()

    encrypted = cipher.substitution_cipher_enc(text, user_enc_pswd)

    # t1 = perf_counter()
    # print(f"Finished Encoding in {perf_counter()-t1}")
    print("encoding ...")
    return steg.encode(input_image, output_image, encrypted)


@eel.expose
def decode(img: str, key: str):
    global steg, cipher

    print("Decoding ...")
    try:
        text_from_image = steg.decode(img, key)
        if text_from_image:
            hex_value = eval(text_from_image)
            return f"SECRET MESSAGE: {cipher.substitution_cipher_dec(hex_value)}"
        else:
            print("UNABLE TO FIND MESSAGE!")
    except Exception as e:
        print(f"UNABLE TO DECRYPT MESSAGE!: {e}")

# def mn() -> None:
#     algo_type = input("e or d: ")
#     steg = custom_steganography.TextIntoImage()
#     cipher = custom_cipher.SubstitutionCipher()

#     if algo_type == "e":
#         # encode 
#         input_image = "assets\\cover_image.png"
#         output_image = "assets\\output_image.png"
#         text = input("Enter secret Msg: ")

#         print("Encrypting...")
#         encrypted = cipher.substitution_cipher_enc(text)

#         print("Encoding...")
#         t1 = perf_counter()
#         steg.encode(input_image, output_image, encrypted)
#         print(f"Finished Encoding in {perf_counter()-t1}")

    
#     else:
#         # decode
#         input_image = "assets\\output_image.png"
#         key_name = input("enter the key file name [without extension]: ")

#         print("Decoding ...")
#         try:
#             text_from_image = steg.decode(input_image, key_name)
#             if text_from_image:
#                 hex_value = eval(text_from_image)
#                 print(f"SECRET MESSAGE: {cipher.substitution_cipher_dec(hex_value)}")
#             else:
#                 print("UNABLE TO FIND MESSAGE!")
#         except Exception as e:
#             print(f"UNABLE TO DECRYPT MESSAGE!: {e}")

eel.start('index.html')