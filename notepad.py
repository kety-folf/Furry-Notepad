from sys import modules
from tkinter.constants import NO
import PySimpleGUI as sg
import io
import os
import tkinter
import  base64
from PySimpleGUI.PySimpleGUI import popup_get_text
import blowfish
from tkinter import filedialog
def encrypt(text,key):
    key_b = bytes(key, 'utf-8')
    cipher = blowfish.Cipher(key_b)
    iv = b'\x19\xcc\xc7\x86R\xa1\xcb\xa6'
    text_b = bytes(text, 'ISO-8859-1')
    text_encrypted = b"".join(cipher.encrypt_cfb(text_b, iv))
    text_encrypted = base64.b64encode(text_encrypted)
    text_encrypted = text_encrypted.decode('ISO-8859-1')
    return text_encrypted

def decrypt(text_encrypted,key):
    key_b = bytes(key,'utf-8')
    cipher = blowfish.Cipher(key_b)
    iv = b'\x19\xcc\xc7\x86R\xa1\xcb\xa6'
    text_encrypted = base64.b64decode(text_encrypted)
    text = b"".join(cipher.decrypt_cfb(text_encrypted, iv))
    text = text.decode('ISO-8859-1')
    return text

def main():
    menu_def =  [['File', ['Open text', 'Open encrypted text', 'Save text', 'Save encrypted text']]]
    layout = [[sg.Menu(menu_definition=menu_def)],[sg.Multiline(key="textbox",size=(1000,1000))]]
    window = sg.Window(title="Furry notepad", layout=layout, resizable=True, size=(400,400))
    while True:#gui event loop
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Open text':
            file_path = filedialog.askopenfilename(filetypes=[('Text file (*.txt)','*.txt')])
            with open(file_path) as f:
                text = f.read()
                window['textbox'].update(text)

        elif event == 'Open encrypted text':
           key = sg.popup_get_text(message="enter encryption code",title="enter code", password_char="*")
           file = filedialog.askopenfilename(filetypes=[('folf encrypted file (*.folf)','*.folf')])
           with open(file) as f:
               encrypted_text = f.read()
               text = decrypt(encrypted_text, key)
               window['textbox'].update(text)

        elif event == 'Save text':
            save_file = filedialog.asksaveasfile(mode='w',filetypes=[('Text file (*.txt)','*.txt')])
            if save_file is None:
                return
            save_file.write(values['textbox'])
            save_file.close()

        elif event == 'Save encrypted text':
            key = sg.popup_get_text(message="enter encryption code",title="enter code", password_char="*")
            encrypted_text = encrypt(values['textbox'], key)
            save_file = filedialog.asksaveasfile(mode='w',filetypes=[('Folf encrypted file (*.folf)','*.folf')])
            if save_file is None:
                return
            save_file.write(encrypted_text)
            save_file.close()
            

if __name__ == '__main__':
    main()