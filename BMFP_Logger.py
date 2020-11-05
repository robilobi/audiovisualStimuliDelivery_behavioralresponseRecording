'''
Logger for TMS Experiment
Based on MFST code
Joseph Thibodeau 2014
'''
import threading
import datetime

class Logger():
    def __init__(self, logfilename):
        self.file = open(logfilename, 'w')
        self.lock = threading.Lock()
    
    def write(self, log_str):
        time_now = datetime.datetime.now()
        millisecond = time_now.microsecond/1000
        time_str=str(time_now.hour)+"\t"+str(time_now.minute)+"\t"+str(time_now.second)+"\t"+str(millisecond)
        self.lock.acquire()
        self.file.write(time_str + "\t" + log_str+"\n")
        self.lock.release()
    
    def closefile(self):
        self.lock.acquire()
        self.file.close()
        self.lock.release()