'''
Created on Sep 6, 2015

@author: Zita
'''
import numpy as np
from Timer import Timer


class Controller(object):
    def __init__(self, Kp=0,Ki=0,Kd=0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        
        self.max = float('inf')
        self.min = float('-inf')
        
        self.acc_error = 0
        self.prev_error = 0
    
    def get(self,sp,x):
        if Timer.t[1] == Timer.now:
            self.acc_error = 0
            self.prev_error = sp-x
        
        dt = Timer.now - Timer.prev
        err = sp-x
        self.acc_error += err
        
        #print((err-self.prev_error)/dt)
        
        u = self.Kp*err + self.Ki * self.acc_error*dt + self.Kd * ( err - self.prev_error)/dt

        
        self.prev_error = err
        
        if u > self.max:
            return self.max
        
        if u < self.min:
            return self.min
        
        return u
        
    def setMax(self,max):
        self.max = max
    def setMin(self,min):
        self.min = min
    def setKi(self, Ki):
        self.Ki = Ki
    def setKp(self, Kp):
        self.Kp = Kp
    def setKd(self, Kd):
        self.Kd = Kd
        
        
class ControllerSet(object):
    def __init__(self):
        self.controllers = []
        self.n = 0 #number of controllers
        
        
    def addController(self,xn,controller):
        self.controllers.append( [xn, controller] )
        self.n += 1
        
    def get(self,sp,x):
        for controller in reversed(self.controllers):
            sp = controller[1].get(sp,x[controller[0]])
        return sp
    
    def setKi(self,cn, Ki):
        self.controllers[cn][1].setKi(Ki)
    def setKp(self,cn, Kp):
        self.controllers[cn][1].setKp(Kp)
    def setKd(self,cn,Kd):
        self.controllers[cn][1].setKd(Kd)
            
class ControllerBox(object):
    def __init__(self, u_size):
        self.u_size = u_size
        '''[Set point, Controller Set'''
        self.controllers = [[None,ControllerSet()]] * u_size
        
        
        self.u = np.array(      (len(Timer.t),u_size)      )
        
    def addController(self, un,xn, Ki=0, Kp = 0, Kd = 0):
        self.controllers[un][1].addController(xn, Controller(Ki = Ki, Kp = Kp, Kd = Kd))
        
    def addSetPoint(self,sp, un):
        self.controllers[un][0] = sp
        
    def addControllerSet(self,un, sp,controllerset):
        self.controllers[un] = [sp,controllerset]
        
    def get(self,x):
        u = np.zeros(self.u_size)
        
        for i in range(self.u_size):
            
            try:
                sp = self.controllers[i][0][Timer.i]
            except:
                sp = self.controllers[i][0]
                
            ctrler = self.controllers[i][1]
            u[i] = ctrler.get(sp,x)
            
        return u
    
    def setKi(self,un,cn,Ki):
        self.controllers[un][1].setKi(cn,Ki)
        
    def setKp(self, un, cn, Kp):
        self.controllers[un][1].setKp(cn,Kp)
    
    def setKd(self, un, cn, Kd):
        self.controllers[un][1].setKd(cn,Kd)
def row_to_column(A):
    try:
        a_column = np.zeros((len(A),1))
    except:
        return A
    
    for i in range(len(A)):
        a_column[i][0] = A[i]
        
    return a_column

def column_to_row(A):
    try:
        a_row = np.zeros(len(A))
    except:
        return A
    
    for i in range(len(A)):
        a_row[i] = A[i][0]
        
    return a_row
