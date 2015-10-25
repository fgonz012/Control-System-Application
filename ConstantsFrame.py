'''
Created on Sep 11, 2015

@author: Zita
'''

from tkinter import *

class ConstantsFrame(LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        LabelFrame.__init__(self,parent,*args,**kwargs)
        
        
        self.Constants_Text = Text(self, width =40, height=20)
        self.Constants_Text.pack(fill= "both", expand = True)
        self.Constants_Text.insert(1.0,"R = 1\nL = 0.5\nK = 0.01\nb = 0.1\nJ = 0.01")
        
    def getText(self):
        return self.Constants_Text.get(1.0,END)