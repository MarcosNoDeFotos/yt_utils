import tkinter as tk
import tkinter.font as tkFont
import os, sys
from tkinter import filedialog

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(os.path.dirname(current))
sys.path.append(parent)
import utils

def MessageInfo(titulo, contenido):
    root = tk.Toplevel();
    root.grab_set()
    root.focus_set()
    #setting title
    root.title(titulo)
    #setting window size
    width=746
    height=711
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(alignstr)
    root.resizable(width=False, height=False)

    txtEditor=tk.Text(root, wrap=tk.WORD)
    
    txtEditor["borderwidth"] = "1px"
    ft = tkFont.Font(family="Arial",size=10)
    txtEditor["font"] = ft
    txtEditor["fg"] = "#333333"
    txtEditor.place(x=10,y=10,width=719,height=647)
    txtEditor.insert(tk.END, contenido);
    txtEditor.insert(tk.END, "\n\n\n");
    

    lstScrollbarY = tk.Scrollbar(txtEditor, orient="vertical");
    lstScrollbarY.config(command=txtEditor.yview)
    lstScrollbarY.pack(side="right", fill="y")  

    lstScrollbarX = tk.Scrollbar(txtEditor, orient="horizontal");
    lstScrollbarX.config(command=txtEditor.xview)
    lstScrollbarX.pack(side="bottom", fill="x")

    txtEditor.config(yscrollcommand=lstScrollbarY.set);
    txtEditor.config(xscrollcommand=lstScrollbarX.set);

    txtEditor.focus_set();
    return root, txtEditor
   