'''
Created on Sep 17, 2015

@author: Zita
'''
from tkinter import *
from Controller import Controller,ControllerSet,ControllerBox
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from Timer import Timer

import numpy as np

class ControllerFrame(Frame):
    def __init__(self, parent,*args,**kwargs):
        Frame.__init__(self,parent,*args,**kwargs)
        
        self.parent = parent
        
        self.Interface = parent.master.parent
        
        self.u_size = 0
        self.u_matrix = []
        
        self.canvas = Canvas(self)
        self.canvas.pack(side = LEFT, fill = BOTH, expand = True)
        
        
        self.scrollbar = Scrollbar(self)
        self.scrollbar.pack(side = RIGHT, fill = Y, expand = True, anchor = E)
        
        self.scrollbar.configure(command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack_propagate(False)

    def setPlotFrame(self,plotFrame):
        self.plotFrame = plotFrame

    def addU(self):
        u_temp = uFrame(self.canvas,self.u_size)
        u_temp.pack()
        
        self.u_size += 1
        
        self.u_matrix.append(u_temp)

    def deleteU(self):
        if self.u_size > 0:
            self.u_matrix[-1].grid_forget()
            self.u_matrix[-1].destroy()
            del self.u_matrix[-1]
            
            self.u_size -= 1

    def adjustU(self,new_u_size):
        while self.u_size > new_u_size:
            self.deleteU()
            
        while self.u_size < new_u_size:
            self.addU()
            self.updateNames()

    def getControllerBox(self):
        temp_controllerbox = ControllerBox(self.u_size)   
             
        for i in range(self.u_size):
                sp = self.u_matrix[i].getsp()
                un = i
                controllerset = self.u_matrix[i].getControllerSet()
                temp_controllerbox.addControllerSet(un, sp, controllerset)
                
        return temp_controllerbox

    def getTime(self):
        print("Success!")

    def isValid(self):
        for u in self.u_matrix:
            if u.isValid() != True:
                return False
            
        return True

    def updateNames(self):
        unames = self.parent.master.PlantFrame.getunames()
        for i in range(len(self.u_matrix)):
            self.u_matrix[i].updateName()
            
    def getSPchoice_matrix(self):
        
        temp = []
        
        for uframe in self.u_matrix:
            temp.append(uframe.constantSP.get())
            
        return temp
    
    def updateUnames(self):
        for u in self.u_matrix:
            u.updateName()
            u.setSPname()
            
    def bindEntries(self):
        for uF in self.u_matrix:
            uF.bindEntries()
            
    def unbindEntries(self):
        for uF in self.u_matrix:
            uF.unbindEntries()
                
        

class IndividualController(Frame):
    def __init__(self, root,n, controllers,uFrame, *args, **kwargs):
        Frame.__init__(self,root,*args,**kwargs)
        self.n = n
        self.parent = root
        self.controllers = controllers
        self.uFrame = uFrame
        
        self.Interface = root.master.Interface
        
        self.editWindow = controllerEditWindow(self)
        self.editWindow.protocol("WM_DELETE_WINDOW",self.on_Deleted )
        self.editWindow.withdraw()
        self.editWindow.wm_title("Cap Editor")
        
        
        
        self.controllerEntry = Entry(self, width = 12)
        self.controllerEntry.grid(row=0, column=0)
        self.controllerEntry.insert(0,"Controller"+ str(n) )
        
        self.xnEntry = Entry(self,width = 4)
        self.xnEntry.grid(row=0,column=1)
        self.xnEntry.insert(0,"0")
        
        self.kpEntry = Entry(self, width = 4)
        self.kpEntry.grid(row=0, column=2)
        self.kpEntry.insert(0,"0")
        
        self.kiEntry = Entry(self, width = 4)
        self.kiEntry.grid(row=0, column=3)
        self.kiEntry.insert(0,"0")
        
        self.kdEntry = Entry(self, width = 4)
        self.kdEntry.grid(row=0,column=4)
        self.kdEntry.insert(0,"0")
        
        self.editButton = Button(self,text="Edit", command = self.edit)
        self.editButton.grid(row=0,column=5)
        
        self.delButton = Button(self,text="Del", command = self.deleteSelf)
        self.delButton.grid(row=0,column=6)

    def on_Deleted(self):
        self.editWindow.withdraw()
        
    def edit(self):
        self.editWindow.iconify()
        
    def getxn(self):
        try:
            return int(self.xnEntry.get())
        except:
            pass

    def getn(self):
        return self.n

    def getKp(self):
        return float(self.kpEntry.get())

    def getKi(self):
        return float(self.kiEntry.get())

    def getKd(self):
        return float(self.kdEntry.get())

    def getController(self):
        Ki = self.getKi()
        Kp = self.getKp()
        Kd = self.getKd()
        
        controller_dummy = Controller(Ki=Ki, Kp=Kp, Kd=Kd)
        
        controller_dummy.setMax(self.editWindow.getMax())
        controller_dummy.setMin(self.editWindow.getMin())
        
        return controller_dummy
    
    def bindEntries(self):
        self.kdEntry.bind("<FocusIn>", self.KdHandler)
        self.kpEntry.bind("<FocusIn>", self.KpHandler)
        self.kiEntry.bind("<FocusIn>", self.KiHandler)
        

        
    def unbindEntries(self):
        self.kdEntry.unbind("<FocusIn>")
        self.kiEntry.unbind("<FocusIn>")
        self.kpEntry.unbind("<FocusIn>")
        
    def KdHandler(self, event):
        
        [K, un, cn] = self.uFrame.parent.master.Interface.pf.Kset
        if un != None and cn != None: 
            self.uFrame.parent.master.u_matrix[un].controllers[cn].kiEntry.config(bg="white")
            self.uFrame.parent.master.u_matrix[un].controllers[cn].kpEntry.config(bg="white")
            self.uFrame.parent.master.u_matrix[un].controllers[cn].kdEntry.config(bg="white")
        
        un = self.uFrame.parent.master.u_matrix.index( self.uFrame  )   
        cn =  self.controllers.index(self)
        
        self.uFrame.parent.master.Interface.pf.Kset = ['Kd', un, cn]
        
        self.kdEntry.config(bg = 'pink')
        
        self.uFrame.parent.master.unbindEntries()

    def KpHandler(self, event):
        
        [K, un, cn] = self.uFrame.parent.master.Interface.pf.Kset
        if un != None and cn != None: 
            self.uFrame.parent.master.u_matrix[un].controllers[cn].kiEntry.config(bg="white")
            self.uFrame.parent.master.u_matrix[un].controllers[cn].kpEntry.config(bg="white")
            self.uFrame.parent.master.u_matrix[un].controllers[cn].kdEntry.config(bg="white")
            
        un = self.uFrame.parent.master.u_matrix.index( self.uFrame  )   
        cn =  self.controllers.index(self)
        
        self.uFrame.parent.master.Interface.pf.Kset = ['Kp', un, cn]
        
        self.kpEntry.config(bg = 'pink')
        
        self.uFrame.parent.master.unbindEntries()
        
    def KiHandler(self, event):
        
        
        [K, un, cn] = self.uFrame.parent.master.Interface.pf.Kset
        if un != None and cn != None:
            self.uFrame.parent.master.u_matrix[un].controllers[cn].kiEntry.config(bg="white")
            self.uFrame.parent.master.u_matrix[un].controllers[cn].kpEntry.config(bg="white")
            self.uFrame.parent.master.u_matrix[un].controllers[cn].kdEntry.config(bg="white")

        un = self.uFrame.parent.master.u_matrix.index( self.uFrame  )   
        cn =  self.controllers.index(self)
        
        
        
        self.uFrame.parent.master.Interface.pf.Kset = ['Ki', un, cn]
        
        self.kiEntry.config(bg = 'pink')
        
        self.uFrame.parent.master.unbindEntries()
        

    def deleteSelf(self):
        i = self.controllers.index(self)
        self.grid_forget()
        self.destroy()
        del self.controllers[i]
        
        self.Interface.ui.ControllerFrame.updateUnames()
        self.Interface.pf.adjustSP()
    
class controllerEditWindow(Toplevel):
    def __init__(self, parent, *args, **kwargs):
        Toplevel.__init__(self, parent, *args, **kwargs)
        
        self.hasCap = BooleanVar()
        
        self.checkButton = Checkbutton(self, text="Use caps", variable = self.hasCap, command = self.checkcallback)
        self.checkButton.grid(row=0,column=0, columnspan = 2)
        
        self.maxLabel = Label(self, text = "Max:")
        self.maxLabel.grid(row=1,column=0, sticky = E)
        
        self.maxEntry = Entry(self, state=DISABLED)
        self.maxEntry.grid(row=1, column=1)
        
        self.minLabel = Label(self, text="Min:")
        self.minLabel.grid(row=2,column=0)
        
        self.minEntry = Entry(self, state=DISABLED)
        self.minEntry.grid(row=2, column=1)

        
    def checkcallback(self):
        if self.hasCap.get() == False:
            self.maxEntry.config(state=DISABLED)
            self.minEntry.config(state=DISABLED)
        else:
            self.maxEntry.config(state=NORMAL)
            self.minEntry.config(state=NORMAL)
    def getMax(self):
        if self.hasCap.get():
            try:
                return float(self.maxEntry.get())
            except:
                return float('inf')
        else:
            return float('inf')
        
    def getMin(self):
        if self.hasCap.get():
            try:
                return float(self.minEntry.get())
            except:
                return float('-inf')
        else:
            return float('-inf')
    
''''''
class uFrame(Frame):
    def __init__(self,parent,n,*args,**kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        
        self.Interface = parent.master.Interface
        
        self.uname = "u" + str(n)
        self.controllers = []
        self.n_controllers = 0
        self.controller_number = 0
        self.isSPvalid = False
        self.SPname = "SP"
        self.constantSP = BooleanVar()
        self.constantSP.set(True)
        
        self.uLabel = Label(self,text = "u" + str(n) + ":" , width = 10)
        self.uLabel.grid(row=0,column=0, sticky = N+E)
        
        self.kNamesLabel = Label(self,text = "             ( xn, Kp, Ki, Kd )")
        self.kNamesLabel.grid(row=0,column=1)
        
        self.addButtonFrame = Frame(self)
        self.addButtonFrame.grid(row=2,column=1)
        
        self.ControllersFrame = Frame(self)
        self.ControllersFrame.grid(row=1,column=1)
        
        ''' Entry for the above frame'''
        self.addButton = Button(self.addButtonFrame, text="Add Controller", command = self.addController)
        self.addButton.grid(row=0,column=3)
        
        self.spEntry = Entry(self.addButtonFrame, width = 4)
        self.spEntry.grid(row=0,column=1)
        
        self.spEditButton = Button(self.addButtonFrame, text="Edit", command = self.editSP)
        self.spEditButton.grid(row=0,column=2)
        
        self.spLabel = Label(self.addButtonFrame,text="Set Point")
        self.spLabel.grid(row=0,column=0)
        '''End'''
        
        self.editWindow = editWindow(self)
        self.editWindow.protocol("WM_DELETE_WINDOW",self.ifDeleted )
        self.editWindow.withdraw()
        self.editWindow.wm_title("Set Points Editor")

    def setSPname(self, event=None):
        try:
            if self.controllers == []:
                self.SPname = self.uname
                self.spLabel.config(text="Set Point for\n" + self.uname)
                self.Interface.pf.adjustSP()
                return
                
            index_of_xname = self.controllers[-1].getxn()
            xnames = self.parent.master.parent.master.PlantFrame.getxnames()
            self.spLabel.config(text="Set Point for\n" + xnames[index_of_xname])
            self.SPname = xnames[index_of_xname]
        except:
            self.spLabel.config(text="Set Point")
        
        self.Interface.pf.adjustSP()

    def ifDeleted(self):
        self.editWindow.withdraw()

    def editSP(self):
        self.editWindow.iconify()

    def addController(self):
        temp = IndividualController(self.ControllersFrame, self.controller_number, self.controllers,self)
        temp.pack()
        try:
            self.controllers[-2].xnEntry.unbind('<KeyRelease>')
        except:
            pass
        self.controllers.append(temp)
        self.controllers[-1].xnEntry.bind('<KeyRelease>', self.setSPname)
        
        self.setSPname()
        
        self.n_controllers += 1
        self.controller_number += 1
        

    def getControllerSet(self):
        temp_controller_set = ControllerSet()
        
        for indcontroller in self.controllers:
            xn = indcontroller.getxn()
            
            temp_controller_set.addController(xn, indcontroller.getController())
            
        return temp_controller_set

    def getsp(self):
        if self.constantSP.get() == False:
            return float(self.spEntry.get())
        else:
            #print(self.editWindow.get())
            return self.editWindow.get()

    def deleteController(self,n):
        self.controllers[n].pack_forget()
        self.controllers[n].destroy()
        del self.controllers[n]
        
        self.n_controllers -= 1

    def updateName(self):
        try:
            unames = self.Interface.ui.PlantFrame.getunames()
            i = self.parent.master.u_matrix.index(self)
            self.uname = unames[i]
            self.uLabel.config(text=unames[i])
        except:
            pass
    def bindEntries(self):
        for controllers in self.controllers:
            controllers.bindEntries()
            
    def unbindEntries(self):
        for controllers in self.controllers:
            controllers.unbindEntries()
        
        

class editWindow(Toplevel):
    def __init__(self,parent, *args, **kwargs):
        Toplevel.__init__(self,parent,*args,**kwargs)
        
        self.parent = parent
        self.Interface = parent.Interface
        
        self.checkbox = Checkbutton(self, text = "Use custom set points", variable = parent.constantSP, command = self.on_checked)
        self.checkbox.pack()
        self.checkbox.deselect()
        
        
        self.frame = LabelFrame(self,text="Function")
        self.frame.pack()
        
        self.tLabel = Label(self.frame, text="t:")
        self.tLabel.grid(row=0,column=0)
        
        self.tEntry = Entry(self.frame, state = DISABLED)
        self.tEntry.grid(row=0,column=1)
        
        self.yLabel = Label(self.frame, text="y:")
        self.yLabel.grid(row=1,column=0)
        
        self.yEntry = Entry(self.frame, state = DISABLED)
        self.yEntry.grid(row=1,column=1)
        
        
        
        self.plotButton = Button(self, text="Plot", width = 10, command = self.plot)
        self.plotButton.pack(anchor=E)
        
        self.f = Figure(figsize=(5,5))
        self.f.add_subplot(111).grid()
        
        self.canvas = FigureCanvasTkAgg(self.f,self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(fill= BOTH)

    def plot(self):
        
        t = Timer.t
        y = self.toPlot(t)
        
        line = Line2D(t,y)
        
        self.f.axes[0].cla()
        self.f.axes[0].grid()
        self.f.axes[0].add_line(line)
        
        self.f.axes[0].margins(y=0.1)
        self.f.axes[0].set_xlim(0,Timer.t[-1])
        
        self.canvas.show()

    def toPlot(self,t):
        y_out = eval(self.yEntry.get())
        time = eval(self.tEntry.get())
        
        y=np.zeros(len(t))
        
        for i in range(len(t)):
            for j in range(len(time)):
                if t[i] > time[j]:
                    y[i] = y_out[j]
        return y

    def get(self):
        try:
            t = Timer.t
            y = self.toPlot(t)
        except:
            y = []
        return y

    def on_checked(self):
        #self.parent.parent.master.parent.master.PlotFrame.adjustSP()
        if self.parent.constantSP.get():
            self.parent.spEntry.config(state=DISABLED)
            self.yEntry.config(state = NORMAL)
            self.tEntry.config(state = NORMAL)
        else:
            self.tEntry.config(state = DISABLED)
            self.yEntry.config(state = DISABLED)
            self.parent.spEntry.config(state=NORMAL)
        
        

        