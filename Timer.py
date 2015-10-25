'''
Created on Sep 13, 2015

@author: Zita
'''

class Timer(object):
    now = None
    prev = None
    i = 0
    t = []
        
    def update():
        Timer.i += 1
        try:
            Timer.now = Timer.t[Timer.i]
            try:
                Timer.prev = Timer.t[Timer.i-1]
            except:
                pass
            return True
        except:
            return False
        
    
    def getTime():
        return Timer.now
        
    def setTime(t):
        Timer.t = t
        
    def reset(t):
        Timer.now = None
        Timer.prev = None
        Timer.i = 0
        Timer.t = t