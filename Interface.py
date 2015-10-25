from Inputs import InputTools
from ConstantsFrame import ConstantsFrame
from PlotFrame import PlotFrame
from FileMenu import FileMenu
from FeedbackFrame import FeedbackFrame

from tkinter import *
import tkinter.ttk as ttk


class MainApplication(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        

        
        self.feedback = FeedbackFrame(self, text = "Feedback")
        self.feedback.grid(row=3,column=0, columnspan=6, sticky = W+E+S+N)
        
        self.uc = ConstantsFrame(self,text="Constants")
        self.uc.grid(row=0,column=5, sticky = W+N)
        
        self.ui = InputTools(self, self.uc,self.feedback,text="Inputs")
        self.ui.grid(row=1,column=5, rowspan=2, sticky = W+N+E+S)
        
        self.pf = PlotFrame(self,self.ui,self.feedback, text = "Plot")
        self.pf.grid(row=0,column=0, rowspan=3, columnspan=5, sticky = NSEW)
        

        
        self.ui.setPlotFrame(self.pf)
        
        fm = FileMenu(self,self.parent)
        
        
        for i in range(0,5):
            Grid.columnconfigure(self,i, weight = 1)
            
        for i in range(0,3):
            Grid.rowconfigure(self,i, weight = 1)
            
        
    
if __name__ == "__main__":
    root = Tk()
    m = MainApplication(root)
    
    m.pack(side="top", fill="both", expand= True)
    root.state('zoomed')
    root.wm_title("Zalez Beta - Controller Manager")
    root.mainloop()