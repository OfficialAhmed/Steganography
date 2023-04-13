import eel, os
from tkinter import filedialog, Tk
from lib import custom_steganography, custom_cipher, custom_key

steg = custom_steganography.TextIntoImage()
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
    file = filedialog.askopenfilename(parent = root,
        initialdir = os.getcwd(),
        title = f"CHOOSE {file_type.upper()} TO ENCODE|DECODE THE MESSAGE...",
        filetypes = file_types
    )
    return file if file else None


@eel.expose
def encode(text: str, image: str, user_enc_pswd: str) -> tuple:
    try:
        global steg, cipher

        output_image = "output_image.png"
        key = custom_key.Key()
        key.set_globals()

        encrypted = cipher.substitution_cipher_enc(text, user_enc_pswd)

        if steg.encode(image, output_image, encrypted):
            return (True, 'IMAGE GENERATED AS "output_image.png"')
        return (False, 'MESSAGE IS TOO LONG FOR THE IMAGE')

    except Exception as e:
        return (False, str(e))


@eel.expose
def decode(img: str, key: str, pswd: str) -> str:
    global steg, cipher

    print("Decoding ...")
    try:
        text_from_image = steg.decode(img, key, pswd)
        if text_from_image:
            hex_value = eval(text_from_image)
            return f"SECRET MESSAGE: {cipher.substitution_cipher_dec(hex_value)}"
        else:
            print("done ...")
            return "UNABLE TO FIND MESSAGE!"
    except Exception as e:
        print("done ...")
        return f"UNABLE TO DECRYPT MESSAGE!: {e}"

eel.start('index.html')