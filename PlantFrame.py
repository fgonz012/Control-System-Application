'''
Created on Sep 17, 2015

@author: Zita
'''

from tkinter import *
import numpy as np
from Plant import Plant
from Timer import Timer

class PlantFrame(Frame):
    
    def __init__(self, parent,cf,controllerFrame,feedback, *args, **kwargs):
        Frame.__init__(self,parent,*args,**kwargs)
        
        self.parent = parent
        
        self.cf = cf
        self.controllerFrame = controllerFrame
        self.plotFrame = None
        self.feedBackFrame = feedback
        
        self.colors = ['r','g','b','purple','brown']
        
        entry_width = 30
        
        self.TopLabel = Label(self, text = "x' = Ax + Bu", pady = 10)
        self.TopLabel.grid(row = 0, column = 0, columnspan = 2)
        
        
        self.A_matrix_label = Label(self, text = "[A] matrix:")
        self.A_matrix_label.grid(row=1, column =0, pady = 10, sticky = E)
        
        
        self.A_matrix_entry = Entry(self,width = entry_width, validate = "focusout", validatecommand = self.runA)
        self.A_matrix_entry.grid(row = 1, column = 1, sticky = W)
        self.A_matrix_entry.insert(0,"[[-R/L, -K/L],[ K/J, -b/J]]")
        
        self.errorA = Label(self, fg = "red")
        self.errorA.grid(row=1,column=2, sticky=W)
        
        self.B_matrix_label = Label(self, text = "[B] matrix:")
        self.B_matrix_label.grid(row=2,column=0, pady = 10, sticky = E)
        
        self.B_matrix_entry = Entry(self, width = entry_width,validate='focusout', validatecommand = self.runB)
        self.B_matrix_entry.grid(row=2,column=1, sticky = W)
        self.B_matrix_entry.insert(0,"[[1/L],[0]]")
        
        self.errorB = Label(self)
        self.errorB.grid(row=2,column=2 ,sticky = W)
        
        self.xnames_label = Label(self, text = "Names of \noutputs (x):")
        self.xnames_label.grid(row=3,column=0, pady = 10, sticky = E)
        
        self.xnames_entry = Entry(self, width = entry_width,state = DISABLED, validate = "focusout", validatecommand = self.runXNames)
        self.xnames_entry.grid(row=3, column=1, sticky = W)
        
        self.errorXnames = Label(self)
        self.errorXnames.grid(row=3,column=2, sticky = W)
        
        self.unames_label = Label(self,text = "Names of \ninputs (u):")
        self.unames_label.grid(row=4,column=0,sticky=E)
        
        self.unames_entry = Entry(self,width = entry_width, state = DISABLED, validate = "focusout", validatecommand = self.runUNames)
        self.unames_entry.grid(row=4,column=1,sticky=W)
        
        self.errorUnames = Label(self)
        self.errorUnames.grid(row=4,column=2)
        
        self.ic_label = Label(self, text ="IC matrix:")
        self.ic_label.grid(row=5,column=0, sticky = E)
        
        self.ic_entry = Entry(self)
        self.ic_entry.grid(row=5,column=1, pady=10, sticky = W)
        self.ic_entry.insert(0,"[0,0]")
        
        self.errorIC = Label(self)
        self.errorIC.grid(row=5,column=2)
        
        for i in range(0,5):
            Grid.rowconfigure(self,i,weight=1)
            
        for i in range(0,2):
            Grid.columnconfigure(self,i,weight=1)
           
    def validateA(self, event = None):
        
        
        try: exec( self.cf.getText())
        except:
            self.errorA.config(text = "Constants Invalid")
            return True
        
        try: A = np.array(eval(self.A_matrix_entry.get() ))
        except:
            self.errorA.config(text = "Invalid")
            return True
            
        try: len(A)
        except: 
            self.errorA.config(text = "Must be a matrix")
            return True
            
        if A.shape[0] == 0:
            self.errorA.config(text = "Can't be empty")
            return True
            
        if len(A.shape) == 1 and A.shape[0] == 1:
            self.errorA.config(text = "No Errors")
            return True
            
        if len(A.shape) > 2:
            self.errorA.config(text = "Must be 1D or 2D")
            return True
        
        if A.shape[0] == 1 and len(A) != 1:
            self.errorA.config(text = "Must be square")
            return True
        
        try: A.shape[1]
        except:
            if A.shape[0] != 1:
                self.errorA.config(text = "Must be square")
                return True
            
        if A.shape[0] != A.shape[1]:
            self.errorA.config(text = "Must be square")
            return True
        
        self.errorA.config(text = "No Errors")
            
                
        return True
    def getInput(self):
        exec( self.cf.getText())
        try:
            A = np.array(eval(self.A_matrix_entry.get() ))
            B = np.array(eval(self.B_matrix_entry.get() ))
            ic = np.array(eval(self.ic_entry.get()))
            return {"A":A,"B":B,"ic":ic}
        except:
            return {"A":0,"B":0,"ic":0}
    
    def getPlant(self):
        exec( self.cf.getText())
        
        try:
            A = np.array(eval(self.A_matrix_entry.get() ))
        except:
            A = 0
        try:
            B = np.array(eval(self.B_matrix_entry.get() ))
        except:
            B=0
        try:
            C = eval(self.C_matrix_entry.get() )
        except:
            C = 0
        try:
            u = eval(self.u_entry.get())
        except:
            u = 0
        try:
            ic = np.array(eval(self.ic_entry.get()))
        except:
            ic = [0]
        
        return Plant(ic,A=A,B=B)
    def get_color(self, i=[0]):
        color = self.colors[ i[0]%len(self.colors) ]
        i[0] += 1
        
        
        return color
    def getxsize(self):
        A = self.getA()
        return len(A)
    
    def getusize(self):
        B = self.getB()
        return B.shape[1]
    
    def getic(self):
        return np.array(eval(self.ic_entry.get()))
    def getA(self):
        exec( self.cf.getText())
        return np.array(eval(self.A_matrix_entry.get()))
    
    def getB(self):
        exec( self.cf.getText())
        return np.array(eval(self.B_matrix_entry.get()))
    
    def getA_string(self):
        return self.A_matrix_entry.get()
    
    def getB_string(self):
        return self.B_matrix_entry.get()
    
    def getxnames(self):
        try:
            return eval(self.xnames_entry.get())
        except: 
            A = self.getA()
            names_length = len(A)
            temp = []
            
            for i in range(names_length):
                temp.append("x" + str(i) )
                
            return temp
        
    def getunames(self):
        try:
            return eval(self.unames_entry.get())
        except:
            B = self.getB()
            names_length = B.shape[1]
            temp = []
            
            for i in range(names_length):
                temp.append("u" + str(i))
                
            return temp
        
    def getX(self,t, Kset = None):
        
        # Kset is of the form [ 'Ki', un, cn, Kvalue] where un = U number and cn is controller number
        
        plant = self.getPlant()
        controller = self.controllerFrame.getControllerBox()
        if Kset != None:
            chosenK = Kset[0]
            un = Kset[1]
            cn = Kset[2]
            newK = Kset[3]
            if chosenK == 'Ki':
                controller.setKi(un,cn,newK)
            elif chosenK == 'Kp':
                controller.setKp(un,cn,newK)
            elif chosenK == 'Kd':
                controller.setKd(un,cn,newK)
            
        columns = len(self.getA())
        
        rows = len(t)
        
        res = np.zeros( (rows,columns) )
        res[0] = self.getic()
        
        i = 0
        
        columns = self.getB().shape[1]
        
        u_res = np.zeros( (rows,columns) )
        #u_res[0] = [0]
        
        while( Timer.update() ):
            u = controller.get(res[i])
            
            res[Timer.i] = plant.get(u)
            i += 1
            u_res[i] = u
        return (res,u_res)
    
    def setPlotFrame(self,plotFrame):
        self.plotFrame = plotFrame
        
                
    def runA(self):
        try:
            exec(self.cf.getText())
            
            A = np.array(eval(self.A_matrix_entry.get() ))
            
            size_x = len(A)
            
            
            self.xnames_entry.config(state = NORMAL)
            #self.plotFrame.setNamesX(self.getxnames())
            #self.plotFrame.adjustX(size_x)
            
            self.errorA.config(text="")
            self.xnames_entry.delete(0,END)
            self.xnames_entry.insert(0,'["Current", "Omega"]')
        except:
            self.xnames_entry.config(state = DISABLED)
            self.plotFrame.clearX()
            
        return True
        
    def runB(self):
        try:
            exec(self.cf.getText())
            B = np.array(eval(self.B_matrix_entry.get() ))
            size_u = B.shape[1]
            

        except Exception as e:
            
            self.unames_entry.config(state = DISABLED)
            self.plotFrame.clearU()
            return True

        self.unames_entry.config(state = NORMAL)
            
        #self.plotFrame.setNamesU(self.getunames())
        #self.plotFrame.adjustU(size_u)
        self.controllerFrame.adjustU(size_u)
            
        self.errorB.config(text="")
            
        self.unames_entry.delete(0,END)
        self.unames_entry.insert(0,'["Voltage"]')
        self.controllerFrame.updateUnames()
        return True
    
    def runXNames(self):
        exec(self.cf.getText())
            
        A = np.array(eval(self.A_matrix_entry.get() ))
            
        size_x = len(A)
            
        #self.plotFrame.setNamesX(self.getxnames())
        #self.plotFrame.adjustX(size_x)
        
        return True
            
    def runUNames(self):
        exec(self.cf.getText())
            
        B = np.array(eval(self.B_matrix_entry.get() ))
            
        size_u = B.shape[1]
            
        #self.plotFrame.setNamesU(self.getunames())
        #self.plotFrame.adjustU(size_u)
        self.parent.master.ControllerFrame.updateNames()
        
        return True