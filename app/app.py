import tkinter as tk
from tkinter import filedialog, Text
import os
import pandas as pd
import plotly.express as px
from PIL import ImageTk,Image



# frame = tk.Frame(root, bg='grey')
# frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
root = tk.Tk()
root.resizable(False, False)
canvas = tk.Canvas(root, height=520, width=730, bg='#2d305c')
canvas.pack()
def addApp():
    filename = filedialog.askopenfilename(initialdir='/', title="Select File", 
                filetypes=(("Comma-separated values","*.csv"),("all files","*")))
    if(filename!=""):
        #Wczytywanie danych
        data = pd.read_csv(filename)
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        #Tworzenie i zapis wykresu
        fig = px.line(data, x="timestamp", y=['water'], title='Water consumption ', template = 'plotly_dark')
        fig.write_image("fig1.png")
        root.img = img = ImageTk.PhotoImage(Image.open("fig1.png"))
        width=canvas.winfo_width()
        height=canvas.winfo_height()
        canvas.create_image((width/2,height/2), image=img, anchor='center')


openFile = tk.Button(root, text= "Open File", padx=10, pady=5,
                                        fg='white', bg='#2d305c', command=addApp)
openFile.pack()

root.mainloop()