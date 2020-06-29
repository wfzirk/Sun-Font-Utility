#
# https://stackoverflow.com/questions/57909525/how-do-i-close-a-file-opened-using-os-startfile-python-3-6


import os
import sys
import subprocess
#import psutil
import time
from bfLogger import logger
import threading
'''
class loadFontThrd(threading.Thread):

    def __init__(self, cmd,
                 group=None, name=None, daemon=True):
        super().__init__(group=group, name=name, daemon=daemon)

        self.cmd = cmd
        self._stop = threading.Event()
        
    def run(self):
        logger.info('process started')
        self.process = subprocess.Popen(self.cmd, shell=False)
        print('running', self.process.runcode)


    def stop(self):
        #logger.debug('stop called')
        # request the thread to exit gracefully during its next loop iteration
        self._stop.set()
'''
'''
# https://stackoverflow.com/questions/57909525/how-do-i-close-a-file-opened-using-os-startfile-python-3-6
class xloadFontThrd(threading.Thread):

    def __init__(self, font,
                 group=None, name=None, daemon=True):
        super().__init__(group=group, name=name, daemon=daemon)


        self.cmd = ["fontloader.exe", font]
        #self._stop = threading.Event()
        
    def run(self):
        logger.info('process started')
        self.shell_process = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True) 
        logger.info('process pid %s',self.shell_process.pid)
        #parent = psutil.Process(self.shell_process.pid)
        #while(parent.children() == []):
        #    continue
        #children = parent.children()
        #logger.info('children %s',children)
        #child_pid = children[0].pid
        #logger.info('child pid %s',child_pid)

    def stop(self):
        #logger.debug('stop called')
        # request the thread to exit gracefully during its next loop iteration
        #self._stop.set() 
        logger.info('stop called')
        self.shell_process.stdin.write(b'x')
        logger.info('write stdin')
        self.shell_process.stdin.flush()
        #subprocess.check_output("Taskkill /PID %d /F" % self.shell_process.pid)
'''
 
# https://stackoverflow.com/questions/57909525/how-do-i-close-a-file-opened-using-os-startfile-python-3-6
class loadFontThrd(threading.Thread):

    def __init__(self, font,
                 group=None, name=None, daemon=True):
        super().__init__(group=group, name=name, daemon=daemon)

        self.font = font
        self.cmd = ["fontloader.exe", self.font]
        self._stop = threading.Event()
        self._start = threading.Event()
        
    def run(self):
        logger.info('process started %s',self.cmd)
        self.shell_process = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True) 
        #self.shell_process = subprocess.Popen(self.cmd,  shell=True)
        logger.info('process pid %s',self.shell_process.pid)

    def stop(self):
        logger.info('stop called')
        self.shell_process.stdin.write(b'x')
        logger.info('write stdin')
        #self.shell_process.stdin.flush()
        #subprocess.check_output("Taskkill /PID %d /F" % self.shell_process.pid)

 
if __name__ == "__main__":
    
    #lf = loadFontThrd(["fontloader.exe", "sun7_7_519.ttf"]) 
    lf = loadFontThrd("sun7_7_519.ttf") 
    lf.run()
    logger.info('xalive? %s',lf.is_alive())
    time.sleep(5)
    logger.info('alive? %s',lf.is_alive())
    lf.stop()
    logger.info('1alive? %s',lf.is_alive())
    #lf.join()
    #logger.info('2alive? %s',lf.is_alive())
    time.sleep(1)
    del lf
    #sys.exit(0)
    #shellprocess(["fontloader.exe", "sun7_7_519.ttf"]) 
    time.sleep(20)
    logger.info('done')
    sys.exit(0)
    