'''
Created on May 31, 2015

@author: Zita
'''
import numpy as np
from scipy.integrate import odeint
from Timer import Timer

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

class Plant(object):
    def __init__(self, ic,A=0,B=0,C=0):
        self.A = A
        self.B = B
        self.C = C
        
        self.ic_initial = ic
        self.ic = ic
        self.x = ic
        
    def update(self,u):
        
        def diff_func(y,t):
            y_column = row_to_column(y)
            u_column = row_to_column(u)
            
            x = np.dot(self.A,y_column) + np.dot(self.B,u_column)
            return column_to_row(x)
    
        x = odeint(diff_func, self.ic, np.linspace(Timer.prev,Timer.now,Timer.t[-1]*25))
        
        self.x = x[-1]
        self.ic = self.x
    
    def get(self,u):
        self.update(u)
        return self.x
    
    def getInitial(self):
        return self.ic
        
    def solve(self,u):
        def diff_func(y,t):
            try:
                return np.dot(self.A,y) + np.dot(u,self.B)
            except:
                return np.dot(self.A,y) + u*self.B
        if Timer.now == 0:
            x = odeint(diff_func, self.ic_initial, np.linspace(Timer.prev,Timer.now,100))
        else:
            x = odeint(diff_func, self.ic, np.linspace(Timer.prev,Timer.now,100))
        
        self.x = x[-1]
        self.ic = self.x
        return self.x
    
    
    
    def get_size_of_x(self):
        return len(self.A)
    
    def get_size_of_u(self):
        return self.B.shape[1]
    
    def getA(self):
        return self.A
    def getB(self):
        return self.B    