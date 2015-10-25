'''
Created on Sep 11, 2015

@author: Zita
'''
from tkinter import *

import matplotlib
from Controller import ControllerBox
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator
from Timer import Timer
from matplotlib import animation
import numpy as np
import math

TIME_PTS = 300


class scaleFrame(Frame):
    def __init__(self, parent, uFrame = None,name = "",*args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        
        self.uframe = uFrame
        self.name = name
        
        self.nameLabel = Label(self, text = name)
        self.nameLabel.grid(row=0, column = 0, columnspan = 6)
        
        self.KpLabel = Label(self, text = "Kp")
        self.KpLabel.grid( row = 1, column = 3)
        
        self.KiLabel = Label(self, text = "Ki")
        self.KiLabel.grid( row = 1, column = 4)
        
        self.KdLabel = Label(self, text = "Kd")
        self.KdLabel.grid( row=1, column=5)
        
        self.Kp2Label = Label(self, text = "Kp")
        self.Kp2Label.grid( row = 2, column = 0)
        
        self.Ki2Label = Label(self, text = "Ki")
        self.Ki2Label.grid(row=3, column=0)
        
        self.Kd2Label = Label(self, text = "Kd")
        self.Kd2Label.grid( row =4, column = 0)
        
        self.KpRangeEntry = Entry(self, width = 7)
        self.KpRangeEntry.grid(row=2, column=1, sticky = N+E)
        
        self.KiRangeEntry = Entry(self, width = 7)
        self.KiRangeEntry.grid(row=3, column = 1)
        
        self.KdRangeEntry = Entry(self, width = 7)
        self.KdRangeEntry.grid(row=4,column=1)
        
        self.Ki = DoubleVar()
        self.Kp = DoubleVar()
        self.Kd = DoubleVar()
        
        self.KpScale = Scale(self, var = self.Kp)
        self.KpScale.grid(row = 1, column = 3, rowspan =4)
        
        self.KiScale = Scale(self, var = self.Ki)
        self.KiScale.grid(row=1, column=4, rowspan=4)
        
        self.KdScale = Scale(self, var = self.Kd)
        self.KdScale.grid(row=1, column=5, rowspan=4)
        
    def getKi(self):
        return self.Ki.get()
    def getKp(self):
        return self.Kp.get()
    def getKd(self):
        return self.Kd.get()
    def setKi(self, Ki):
        self.Ki = Ki
    def setKd(self, Kd):
        self.Kd = Kd
    def setKp(self, Kp):
        self.Kp = Kp    
    def setName(self, name):
        self.name = name
        self.nameLabel.config(text = name)
    def link_uframe(self, uframe):
        self.uframe = uframe
        
class PlotScalesFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        
        self.scaleframes = []
    def addScaleFrame(self, uframe=None):
        dummy = scaleFrame(self)
        dummy.pack()
        self.scaleframes.append(dummy)
        return
        
class PlotFrame(LabelFrame):
    def __init__(self, parent,inpt,feedback, *args, **kwargs):
        LabelFrame.__init__(self,parent,*args,**kwargs)
        #self.test = scaleFrame(self)
        #self.test.pack()
        self.parent = parent
        
        self.inpt = inpt
        self.x = []
        self.u = []
        self.sp = []
        
        self.xlines = []
        self.ulines = []
        self.splines = []
        
        self.animation_lines = []
        
        self.names = []
        self.unames = []
        self.feedbackFrame = feedback
        
        self.colors = ['b','g','r','brown','purple', 'orange']
        self.f = Figure()
        self.f.add_subplot(111).grid()
        
        self.plottoolbarFrame = Frame(self)
        self.plottoolbarFrame.pack(side = LEFT, fill = BOTH, expand = True)
        
        self.canvas = FigureCanvasTkAgg(self.f,self.plottoolbarFrame)
        self.canvas.get_tk_widget().pack(fill= BOTH, expand = True)
        
        
        self.toolbar = NavigationToolbar2TkAgg(self.canvas,self.plottoolbarFrame)
        self.toolbar.update()
        self.canvas._tkcanvas.pack( fill= BOTH, expand = True)
        
        self.plotNotebook = ttk.Notebook(self)
        self.plotNotebook.pack(side=LEFT, fill=BOTH)
        
        self.plotOptionFrame = Frame(self.plotNotebook)
        self.plotOptionFrame.pack(fill =BOTH)
        
        self.plotsKFrame = Frame(self.plotNotebook)
        self.plotsKFrame.pack(fill=BOTH)

        
        self.animationFrame = LabelFrame(self.plotNotebook, text = "test")
        self.animationFrame.pack(fill = BOTH, expand = True)
        
        self.plotNotebook.add(self.plotOptionFrame, text = "Plot Options")
        self.plotNotebook.add(self.animationFrame, text = "Animation")
        self.plotNotebook.add(self.plotsKFrame, text = "K Plots")
        
        self.t = Frame(self.plotOptionFrame)
        self.t.pack(side=BOTTOM)
        #TIME STUFF
        self.timeLabel = Label(self.t,text="Time:")
        self.timeLabel.pack(side=LEFT)
        
        self.timeEntry = Entry(self.t, width = 4)
        self.timeEntry.insert(0, "10")
        t = np.linspace(0,float(self.timeEntry.get()),TIME_PTS)
        Timer.reset(t)
        self.timeEntry.pack(side=LEFT)
        self.timeEntry.bind("<KeyRelease>", self.validateTime)
        
        
        self.RunPlotButton = Button(self.t,text="Run",command = self.run, width=10)
        self.RunPlotButton.pack(side=LEFT)
        #END

        self.xLabel = Label(self.plotOptionFrame, text = "Outputs", width = 10)
        self.xLabel.pack(side=TOP)
        
        self.xFrame = Frame(self.plotOptionFrame)
        self.xFrame.pack()
        
        self.uLabel = Label(self.plotOptionFrame, text = "Inputs")
        self.uLabel.pack()
        
        self.uFrame = Frame(self.plotOptionFrame)
        self.uFrame.pack()
        
        self.spLabel = Label(self.plotOptionFrame, text = "Set Points")
        self.spLabel.pack()
        
        self.spFrame = Frame(self.plotOptionFrame)
        self.spFrame.pack()
        
        self.RunAnim = Button(self.animationFrame, text="Run Animation", command = self.runAnimation)
        self.RunAnim.grid(row=7, column = 5)
        
        self.animationKEntry = Entry(self.animationFrame)
        self.animationKEntry.grid(row=1, column=5)
        
        self.animationKLabel = Label(self.animationFrame, text = "K:")
        self.animationKLabel.grid(row = 1, column = 4)
        
        self.animationKButton = Button(self.animationFrame, text = "Choose K", command = self.chooseK)
        self.animationKButton.grid(row=1,column = 6)
        
        self.animationCalcButton = Button(self.animationFrame, text = "Update K", command = self.updateK)
        self.animationCalcButton.grid(row=7, column=6)
        
        
        self.maxy = float("-inf")
        self.miny = float("inf")
        
        self.stop = BooleanVar()
        self.stop.set(False)
        
        self.Kset = [None,None,None] #Change
        
    def chooseK(self, event = None):
        self.inpt.ControllerFrame.bindEntries()
        
    def adjustSP(self):
        spchoice = self.parent.ui.ControllerFrame.getSPchoice_matrix()
        uframe = self.parent.ui.ControllerFrame.u_matrix
        
        while len(spchoice) > len(self.sp):
            self.sp.append(None)
            
        while len(spchoice) < len(self.sp):
            self.sp[-1].deleteSelf()
            
        for i in range(len(self.sp)):
            if spchoice[i]:
                if self.sp[i] == None:
                    self.sp[i] = x(self.spFrame, self.sp, 'sp')
                    self.sp[i].pack()
                self.sp[i].setName(uframe[i].SPname + "\nmark")
            else:
                if self.sp[i] != None:
                    self.sp[i].pack_forget()
                    self.sp[i].destroy()
                    self.sp[i] = None
                    
    def updateK(self):
        [fro, to, pts] = eval(self.animationKEntry.get())
        
        self.K = np.linspace( fro,to,pts )
        t = np.linspace(0,float(self.timeEntry.get()),TIME_PTS)
        
        
        self.x_main = np.zeros( (len(self.K), TIME_PTS, len(self.inpt.PlantFrame.getA()))  )
        self.u_main = np.zeros( (len(self.K), TIME_PTS, self.inpt.PlantFrame.getB().shape[1])  )


        for i in range(len(self.K)):
            Timer.reset(t)
            (x,u) = self.inpt.getX(t, self.Kset + [self.K[i]])
            
            self.u_main[i,:,:] = u
            self.x_main[i,:,:] = x
            
            
            
        
    def runAnimation(self):
        lines = self.f.axes[0].lines
        t = np.linspace(0,float(self.timeEntry.get()),TIME_PTS)
        K = self.K
        x_main = self.x_main
        u_main = self.u_main

        
        max_list = []
        min_list = []
        
        for i in range(len(K)):
            w = 0
            for j in range(   x_main.shape[2]   ):
                if self.x[j].get():
                    max_list.append(np.max(x_main[i][:,j]))
                    min_list.append(np.min(x_main[i][:,j]))
                    w += 1
                    
            for j in range( u_main.shape[2] ):
                if self.u[j].get():
                    max_list.append(np.max(u_main[i][:,j]))
                    min_list.append(np.min(u_main[i][:,j]))
                    w += 1
                    
        maxy = np.max(max_list)
        miny = np.min(min_list)
        
        self.f.axes[0].set_ylim(math.ceil(miny),math.ceil(maxy))
        self.f.axes[0].set_xlim(0,Timer.t[-1])

        def init():
            for line in lines:
                line.set_data([], [])
            return lines
        
        def animate(i):
            self.f.axes[0].set_title("K = " + '%s' % float('%.3g' %  K[ i % len(K)]))
            w = 0
            for j in range(   x_main.shape[2]   ):
                if self.x[j].get():
                    lines[w].set_data(t,x_main[i][:,j])
                    w += 1
                    
            for j in range( u_main.shape[2] ):
                if self.u[j].get():
                    lines[w].set_data(t,u_main[i][:,j])
                    w += 1

                        
            return lines

        animation.FuncAnimation(self.f, animate, init_func=init,
                                frames=len(K), interval=5000/len(K), repeat = False, blit=False)
        
        
        self.canvas.show()

    def stop(self, event = None):
        self.stop.set(True)
        
    def validateTime(self,event):
        try:
            t = np.linspace(0,float(self.timeEntry.get()),TIME_PTS)
            Timer.reset(t)
        except:
            self.feedbackFrame.addMsg("Invalid Time")
        
    def run(self):
        
        '''Get Timer'''
        try:
            t = np.linspace(0,float(self.timeEntry.get()),TIME_PTS)
            Timer.reset(t)
            self.feedbackFrame.clearMessages()
            
            (x,u) = self.inpt.getX(Timer.t)
            
            
        except Exception as e:
            print(e)
            self.feedbackFrame.clearMessages()
            self.feedbackFrame.addMsg("Invalid Input.")
        else:
            self.xlines = []
            self.ulines = []
            self.splines = []
            
            self.setNamesX(self.inpt.PlantFrame.getxnames())
            self.adjustX(self.inpt.PlantFrame.getxsize())
            
            self.setNamesU(self.inpt.PlantFrame.getunames())
            self.adjustU(self.inpt.PlantFrame.getusize())
            
            self.adjustSP()
            
            u_matrix = self.inpt.ControllerFrame.u_matrix
            
            self.analysis(x, u, self.names, self.unames, self.u, self.x)
            
            self.f.axes[0].cla()
            self.f.axes[0].grid()
            self.f.axes[0].set_xlabel("Time")
            

            
            color_index = 0
            
            for i in range(len(self.x)):
                self.xlines.append(  Line2D(Timer.t,x[:,i], label = self.names[i], linewidth = 2, c = self.colors[color_index % len(self.colors)])  )
                color_index += 1
                if self.x[i].get():
                    self.f.axes[0].add_line( self.xlines[-1] )
            
            for i in range(len(self.u)):
                self.ulines.append( Line2D(Timer.t,u[:,i], label = self.unames[i], linewidth = 2, c = self.colors[color_index % len(self.colors)]) )
                color_index += 1
                if self.u[i].get():
                    self.f.axes[0].add_line( self.ulines[-1])
                    
            for i in range(len(self.sp)):
                if self.sp[i] != None:
                    self.splines.append( Line2D(Timer.t, u_matrix[i].editWindow.get(), label = self.sp[i].getName(), linewidth = 2, c = self.colors[color_index % len(self.colors)], ls = "--") )
                    color_index += 1
                    if self.sp[i].get():
                        self.f.axes[0].add_line(self.splines[-1])
                    
            
            self.f.axes[0].margins(y=0.1)
            self.f.axes[0].set_xlim(0,Timer.t[-1])
            
            [ybot, ytop] = self.f.axes[0].get_ylim()
            
            self.f.axes[0].yaxis.set_major_locator(MaxNLocator(20))
            
            self.f.axes[0].legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
            
            self.canvas.show()

    def addSP(self):
        temp = x(self.spFrame, self.sp)
        temp.pack()
        self.sp.append(temp)
        
    def addx(self):
        temp = x(self.xFrame,self.x, 'x')
        temp.pack()
        self.x.append(temp)
        
    def addu(self):
        temp = x(self.uFrame,self.u, 'u')
        temp.pack(side=TOP)
        self.u.append(temp)
        
    def adjustX(self,x_size):
        while len(self.x) < x_size:
            self.addx()

        while len(self.x) > x_size:
            self.x[-1].deleteSelf()
                
        for i in range(len(self.x)):
            self.x[i].setName(self.names[i])
            
    def adjustU(self,u_size):
        while len(self.u) < u_size:
            self.addu()
            
        while len(self.u) > u_size:
            self.u[-1].deleteSelf()
            
        for i in range(u_size):
            try:
                self.u[i].setName(self.unames[i])
            except:
                pass

   
        
    def setNamesU(self,unames):
        self.unames = unames
        
    def setNamesX(self,names):
        self.names = names
        
    def clearU(self):
        for u in self.u:
            u.deleteSelf()
        
    def clearX(self):
        while self.x != []:
            self.x[-1].deleteSelf()
            
    def analysis(self, x,u,xnames,unames, uChoices, xChoices):
        #MAX SIZE
        self.feedbackFrame.addMsg("Output")
        for i in range(x.shape[1]):
            if xChoices[i].get():
                maximum = np.max(x[:,i])  
                minimum = np.min(x[:,i])
                self.feedbackFrame.addMsg(xnames[i] + " maximum is " +  '%s' % float('%.3g' % maximum)  + " minimum is " + '%s' % float( '%.3g' % minimum ))           #"K = " + '%s' % float('%.3g' %  K[ i % len(K)])
            
        self.feedbackFrame.addMsg("Input")
        for i in range(u.shape[1]):
            if uChoices[i].get():
                maximum = np.max(u[:,i])
                minimum = np.min(u[:,i])
                self.feedbackFrame.addMsg(unames[i] + " maximum is " +  '%s' % float('%.3g' % maximum)  + " minimum is " + '%s' % float( '%.3g' % minimum ))
        
class x(Frame):
    def __init__(self,parent,x,set,*args,**kwargs):
        Frame.__init__(self,parent,*args,**kwargs)
        
        self.parent = parent
        
        self.x = x
        self.name = ""
        self.label = Label(self)
        self.set = set
            
        self.label.grid(row=0,column=0)
        
        self.var = BooleanVar()
        self.var.trace('w', self.onClick)
        
        
        self.yesRadioButton = Radiobutton(self,text="Y",variable=self.var, value = True)
        self.yesRadioButton.grid(row=0,column=1)
        self.yesRadioButton.select()
        self.prev = True
        
        self.noRadioButton = Radiobutton(self,text="N",variable=self.var,value=False)
        self.noRadioButton.grid(row=0,column=2)
        
        
    def get(self):
        return self.var.get()
        
    def deleteSelf(self):
        self.pack_forget()
        self.destroy()
        i = self.x.index(self)
        del self.x[i]
        
    def setName(self,name):
        self.name = name
        self.label.config(text= name)
        
    def getName(self):
        return self.name
    
    def onClick(self, *args):
        try:
            if self.var.get() != self.prev:
                i = self.x.index(self)
                
                self.f = self.parent.master.master.master.f
                self.xlines = self.parent.master.master.master.xlines
                self.ulines = self.parent.master.master.master.ulines
                self.splines = self.parent.master.master.master.splines
                self.canvas = self.parent.master.master.master.canvas
                
                if self.var.get():# Y click
                    if self.set == 'x':
                        self.f.axes[0].add_line(self.xlines[i])
                    elif self.set == 'u':
                        self.f.axes[0].add_line(self.ulines[i])
                    elif self.set == 'sp':
                        self.f.axes[0].add_line(self.splines[i])
                    #self.f.axes[0].add_line(  )
                else:
                    if self.set == 'x':
                        self.f.axes[0].lines.remove(self.xlines[i])
                    elif self.set == 'u':
                        self.f.axes[0].lines.remove(self.ulines[i])
                    elif self.set == 'sp':
                        self.f.axes[0].lines.remove(self.splines[i])
                        
                self.f.axes[0].margins(y=0.1)
                self.f.axes[0].set_xlim(0,Timer.t[-1])
                
                if self.f.axes[0].get_lines() == []:
                    self.f.axes[0].legend_.remove()
                else:
                    self.f.axes[0].legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
                    
                self.canvas.show()
                self.prev = self.var.get()
        except Exception as e:
            print(e)
            pass
        
        
        
        
        