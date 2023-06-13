"""

    This file holds methods, ready to be called by JS 
    when interacted by the UI

"""

import eel, os
from tkinter import filedialog, Tk
from lib import custom_steganography, custom_cipher, custom_key

text_into_image_steg = custom_steganography.TextIntoImage()
image_into_image_steg = custom_steganography.ImageIntoImage()
cipher = custom_cipher.SubstitutionCipher()

eel.init('interface')

@eel.expose
def get_file(file_type) -> str|None:

    if file_type == "key":
        file_types = [("Binary files", "*.bin")]

    elif file_type == "image":
        file_types = [("Image files", "*.jpg;*.jpeg;*.png")]


    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    file = filedialog.askopenfilename(
        parent = root,
        initialdir = os.getcwd(),
        title = f"CHOOSE {file_type.upper()} TO ENCODE|DECODE THE MESSAGE...",
        filetypes = file_types
    )

    return file if file else None

@eel.expose
def encode_text(text: str, image: str, user_enc_pswd: str) -> tuple:

    try:
        global text_into_image_steg, cipher

        output_image = "assets\\text2image\\output_image.png"
        key = custom_key.Key()
        key.set_globals()

        encrypted = cipher.substitution_cipher_enc(text, user_enc_pswd)

        if text_into_image_steg.encode(image, output_image, encrypted):

            return (True, f'IMAGE GENERATED AS "{output_image}"')
        
        return (False, 'MESSAGE IS TOO LONG FOR THE IMAGE')

    except Exception as e:
        return (False, str(e))

@eel.expose
def decode_text(img: str, key: str, pswd: str) -> str:

    global text_into_image_steg, cipher

    try:

        text_from_image = text_into_image_steg.decode(img, key, pswd)

        if text_from_image:

            hex_value = eval(text_from_image)
            return f"SECRET MESSAGE: {cipher.substitution_cipher_dec(hex_value)}"
        
        else:

            return "UNABLE TO FIND MESSAGE!"
        
    except Exception as e:

        return f"UNABLE TO DECRYPT MESSAGE!: {e}"

@eel.expose
def encode_image(cover, secret, compression_ration):

    try:

        image_into_image_steg.set_compression(int(compression_ration))
        image_into_image_steg.compress_cover_image(cover)
        image_into_image_steg.compress_hidden_image(secret)
        result = image_into_image_steg.encrypt()
        image_into_image_steg.delete_temp_images()

        return (result, )
    
    except Exception as e:
        return (False, str(e))

@eel.expose
def decode_image(image):
    try:
        return (image_into_image_steg.decrypt(image),)
    
    except Exception as e:
        return (False, str(e))


eel.start('index.html')