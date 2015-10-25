'''
Created on Sep 11, 2015

@author: Zita
'''

from tkinter import *

class FileMenu(Frame):
    def __init__(self, parent, root, *args, **kwargs):
        Frame.__init__(self,parent,*args,**kwargs)
        
        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New")
        
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)