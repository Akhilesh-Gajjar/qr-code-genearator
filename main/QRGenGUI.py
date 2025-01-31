import tkinter as tk
from tkinter import *
from tkinter import filedialog
import pyqrcode

root = tk.Tk()
root.title("QR Code Generator")
root.geometry('1000x650')
root.configure(bg='cyan')

lbl1 = Label(root, 
             text="Welcome to QR Code Generator", 
             font=("Ariel", 18), 
             bg='cyan')
lbl1.pack()

lbl2 = Label(root, 
             text="Please Enter the text that you would like to convert to QR Code!", 
             font=("Ariel", 12), 
             bg='cyan')
lbl2.pack()

txt = Entry(root, 
            width=60, 
            font=("Ariel", 14))
txt.pack()

lbl3 = Label(root, 
             bg='cyan')
lbl3.pack()

def gen_qr():
    global qr, qrimg
    if len(txt.get()) == 0:
        lbl_qrimg.config(text="Unable to generate QR Code, as no Input was Entered",
                         font=("Ariel", 16),
                         bg='cyan')
    else:
        qr = pyqrcode.create(txt.get())
        if len(txt.get()) <= 100:
            qrimg = BitmapImage(data=qr.xbm(scale=7))
        else:
            qrimg = BitmapImage(data=qr.xbm(scale=4))
    
        lbl3.config(text="  Generated QR Code : ", 
                    font=("Ariel", 16), 
                    bg='cyan')
        lbl_qrimg.config(image=qrimg,
                         bg='cyan')

        # Enable the save button
        save_btn.config(state=NORMAL)

def save_qr():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        qr.png(file_path, scale=6)

lbl_qrimg = Label(root, 
                  bg='cyan')
lbl_qrimg.pack()

btn = Button(root, 
             text="Submit", 
             fg="Black", 
             width=20, 
             height=2, 
             bg='sky blue', 
             command=gen_qr)
btn.pack(pady=10)  # Added vertical padding

save_btn = Button(root, 
                  text="Save QR Code", 
                  fg="Black", 
                  width=20, 
                  height=2, 
                  bg='sky blue', 
                  command=save_qr, 
                  state=DISABLED)
save_btn.pack(pady=10)  # Added vertical padding

root.mainloop()
