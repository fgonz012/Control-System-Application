from tkinter import *

class FeedbackFrame(LabelFrame):

    
    def __init__(self, parent, *args, **kwargs):
        LabelFrame.__init__(self, parent, *args, **kwargs)
        
        self.error_messages = []
        
        self.canvas = Canvas(self, bg="white")
        self.canvas.pack(fill=BOTH, expand = True)
        
        self.canvas.pack_propagate(False)
        
    def addMsg(self, text):
        
    
        temp_frame = Label(self.canvas, text = text, bg='white')
        temp_frame.pack(side = TOP, anchor = W)
        
        self.error_messages.append(temp_frame)
        
    def clearMessages(self):
        
        for err_msg in self.error_messages:
            err_msg.pack_forget()
            err_msg.destroy()
            del err_msg
        
        
        