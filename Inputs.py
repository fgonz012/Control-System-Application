'''
Created on Sep 11, 2015

@author: Zita
'''
from tkinter import *
import tkinter.ttk as ttk
import numpy as np
from Plant import Plant
from PlantFrame import PlantFrame
from ControllerFrame import ControllerFrame

class InputTools(LabelFrame):
    def __init__(self, parent, cf,feedback, *args, **kwargs):
        LabelFrame.__init__(self, parent, *args,**kwargs)
        
        self.parent = parent
        
        self.cf = cf
        self.plotFrame = None
        self.feedbackFrame = feedback
        ''' Make the Notebook'''
        self.n = ttk.Notebook(self)
        self.n.pack(fill="both", expand = True)
        

        
        self.ControllerFrame = ControllerFrame(self.n)
        self.ControllerFrame.pack(fill = "both", expand = True)

        self.PlantFrame = PlantFrame(self.n,cf,self.ControllerFrame,feedback)
        self.PlantFrame.pack(fill="both", expand = True)

        self.n.add(self.PlantFrame, text="Plant")
        self.n.add(self.ControllerFrame, text="Controller")
        
        

    def getInput(self):
        return self.PlantFrame.getInput()

    def getPlant(self):
        return self.PlantFrame.getPlant()       
   
    def getControllerBox(self):
        return self.ControllerFrame.getControllerBox()
    
    def getX(self,t, Ki = None):
        return self.PlantFrame.getX(t, Ki)
    
    def setPlotFrame(self,PlotFrame):
        self.PlotFrame = PlotFrame
        self.PlantFrame.setPlotFrame(PlotFrame)
        self.ControllerFrame.setPlotFrame(PlotFrame)
        
    def checkAndValidatePlant(self):
        self.PlantFrame.updateU()