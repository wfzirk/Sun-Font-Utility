
#https://stackoverflow.com/questions/30349542/command-libreoffice-headless-convert-to-pdf-test-docx-outdir-pdf-is-not	


import os
import sys
import subprocess
import inspect
import zipfile
import time
from datetime import timedelta
import logging
#import inspect

#frame_records = inspect.stack()[1]
#calling_module = inspect.getmodulename(frame_records[1])
#print('calling',calling_module)

class LoggerAdapter(logging.LoggerAdapter):
    def __init__(self, logger, prefix):
        super(LoggerAdapter, self).__init__(logger, {})
        self.prefix = prefix

    def process(self, msg, kwargs):
        return '[%s] %s' % (self.prefix, msg), kwargs

def setup_logger(name, log_file, level=logging.INFO):
    logger = logging.getLogger(name)
    # Add any custom handlers, formatters for this logger
    #myHandler = logging.StreamHandler()
    myFormatter = logging.Formatter('%(asctime)s ,%(message)s')
    #myHandler.setFormatter(myFormatter)
    handler = logging.FileHandler(log_file, mode='w')
    handler.setFormatter(myFormatter)
    logger.addHandler(handler)
    #logger.addHandler(myHandler)
    logger.setLevel(level)
    ln = log_file.split('.')[0]
    ln = ln.replace("Log\\","")
    
    return LoggerAdapter(logger, ln)
    
'''

def setup_logger(name, log_file, level=logging.INFO):
    # https://stackoverflow.com/questions/28330317/print-timestamp-for-logging-in-python
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler(log_file, mode='w')
    handler.setFormatter(formatter)
    #screen_handler = logging.StreamHandler(stream=sys.stdout)
    #screen_handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    #logger.addHandler(screen_handler)
    return logger

script = sys.argv[0]
logname = script.split('.')[0]
#logname = calling_module
logger =  setup_logger("info", 'Log\\'+logname+'.log', logging.INFO)
errlogger = setup_logger("err", 'Log\\'+logname+'.err', logging.ERROR)

def new_logger(name):
    global logger, errlogger
    #print('new_logger',name)
    logger = setup_logger("info", 'Log\\'+name+'.log', logging.INFO)
    errlogger = setup_logger("err", 'Log\\'+name+'.err', logging.ERROR)

def closeLoggers(name):
    log = logging.getLogger('info')
    x = list(log.handlers)
    for i in x:
        log.removeHandler(i)
        i.flush()
        i.close()
        
    log = logging.getLogger('err')
    x = list(log.handlers)
    for i in x:
        log.removeHandler(i)
        i.flush()
        i.close()    


lcnt = 0  
def log_info(*args, end=''):
    global lcnt
    line = ' '.join([str(a) for a in args])
    logger.info(str(lcnt)+','+line)
    if '\n' in line:
        print(lcnt,line, end='')
    else:
        print(lcnt, line)
    lcnt = lcnt+1
    
def log_warn(*args, end=''):
    global lcnt
    line = ' '.join([str(a) for a in args])
    errlogger.error(str(lcnt)+','+line)
    #print(lcnt,line, file=sys.stderr)
    if '\n' in line:
        print(lcnt,',',line, end='', file=sys.stderr)
    else:
        print(lcnt, ',',line, file=sys.stderr)
    lcnt+=1
    
def log_err(*args, end=''):
    global lcnt
    line = ' '.join([str(a) for a in args])
    errlogger.error(str(lcnt)+','+line)
    #print(lcnt,line, file=sys.stderr)
    if '\n' in line:
        print(lcnt, ',',line, end='', file=sys.stderr)
    else:
        print(lcnt, ',',line, file=sys.stderr)
    lcnt+=1
'''   
start_time = ""
def runTime(t = 'start'):
    global start_time
    if t == 'start':
        start_time = time.time()
        ft = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(start_time))
        print('ft',ft)
        return ft
    
    if t == 'stop':
        stop_time = time.time()
        elapsed_time = stop_time - start_time
        td =  timedelta(milliseconds=round(elapsed_time))
        
        msg = (td.seconds,td.microseconds)
        print(msg)
        #msg = "Execution took: %s secs (Wall clock time)" % timedelta(milliseconds=round(elapsed_time))

        return 'Execution time '+str(msg)
    


def lineno():
    """Returns the current line number in our program."""
    #t = time.strftime("%Y-%m-%d %H:%M:%S.%f")
    #return t
    return inspect.currentframe().f_back.f_lineno
    

def getUnicode(str):
    try:
        a = chr(int(str,16)).encode('utf-8')
        return a.decode('utf-8')
    except Exception as  e:
        log_err("fatal error getUnicode",e)
        sys.exit(1)
        
def unicode2hex(uic): 
    #print(hex(ord(uic)))
    return(hex(ord(uic)))
   
def convert2text(filename, outdir=""):
    # https://stackoverflow.com/questions/24704536/how-do-i-convert-doc-files-to-txt-using-libreoffice-from-the-command-line
    # https://wiki.openoffice.org/wiki/Documentation/DevGuide/Spreadsheets/Filter_Options#Filter_Options_for_the_CSV_Filter
    cmd = ["C:\Program Files\LibreOffice\program\soffice",
        "--convert-to",
        "txt:Text",
        filename]

    if outdir:
        cmd.append("--outdir")
        cmd.append(outdir)
    log_info('convert2text',cmd)
    try:
        result = subprocess.call(cmd)
        log_info('convert2text status', result)
    except Exception as e:
        log_info("fatal error convert2text ", result, filename,e)
        traceback.print_exc()
        return(1)
    txtFile = filename.split('.')[0]+'.txt'
    return txtFile
   
   
def convert2csv(filename, outdir=""):
    # https://wiki.openoffice.org/wiki/Documentation/DevGuide/Spreadsheets/Filter_Options#Filter_Options_for_the_CSV_Filter
    #cmd = "C:\Program Files\LibreOffice\program\soffice"+  " --convert-to csv"+ " --infilter=CSV:44,34,76,1,,,true "+ filename
    cmd = ["C:\Program Files\LibreOffice\program\soffice", "--convert-to", "csv", "--infilter=CSV:44,34,76,1,,,true ", filename]
    #log_info("convert2csv",cmd)
    if outdir:
        cmd.append("--outdir")
        cmd.append(outdir)
    log_info('convert2csv',cmd)
    try:
        result = subprocess.call(cmd)
        log_info('convert2csv status', result)
    except Exception as e:
        log_info("fatal error convert2csv ", result, filename,e)
        traceback.print_exc()
        return(1)
    csvFile = filename.split('.')[0]+'.csv'
    return csvFile
        

def convert2ods(filename, outdir=""):	
    
    cmd = ["C:\Program Files\LibreOffice\program\soffice", "--headless", "--convert-to", "ods", "--infilter=CSV:44,34,76,1,,,true", filename]
    if outdir:
 
        cmd.append("--outdir")
        cmd.append(outdir)
    log_info('convert2ods',cmd)
    try:
        result = subprocess.call(cmd)
        log_info('convert2ods status', result)
    except Exception as e:
        log_err("fatal error convert2ods =",result,filename,e)
        traceback.print_exc()
        return(1)
    odsFile = filename.split('.')[0]+'.ods'
    return odsFile

# https://stackoverflow.com/questions/30349542/command-libreoffice-headless-convert-to-pdf-test-docx-outdir-pdf-is-not	
#   /path/to/soffice                                                     \
#    --headless                                                         \
#   "-env:UserInstallation=file:///tmp/LibreOffice_Conversion_${USER}" \
#    --convert-to pdf:writer_pdf_Export                                 \
#    --outdir ${HOME}/lo_pdfs                                           \
#   /path/to/test.docx

def convert2pdf(filename, outdir=""):	
    #cmd = "C:\Program Files\LibreOffice\program\soffice"+ " --headless"+  " --convert-to pdf "+filename
    cmd = ["C:\Program Files\LibreOffice\program\soffice",
            "--headless",
            "--convert-to", 
            "pdf", 
            filename]
    
    #cmd = "C:\Program Files\LibreOffice\program\soffice" + " --headless" + " --convert-to pdf:calc_pdf_Export " + filename + " --outdir dist"
    if outdir:
        cmd.append("--outdir")
        cmd.append(outdir)
    log_info('convert2pdf',cmd)
    try:
        result = subprocess.call(cmd)
        log_info('convert2pdf status', result)
    except Exception as e:
        log_err("fatal error convert2pdf =", result, filename,e)
        traceback.print_exc()
        return(1)
    pdfFile = filename.split('.')[0]+'.pdf'
    return pdfFile

def convert2odt(filename, outdir=""):	
    #cmd = "C:\Program Files\LibreOffice\program\soffice"+ " --headless"+  " --convert-to pdf "+filename
    cmd = ["C:\Program Files\LibreOffice\program\soffice",
            "--headless",
            "--convert-to", 
            "odt", 
            filename]
    
    #cmd = "C:\Program Files\LibreOffice\program\soffice" + " --headless" + " --convert-to pdf:calc_pdf_Export " + filename + " --outdir dist"
    if outdir:
        cmd.append("--outdir")
        cmd.append(outdir)
    print('convert2odt',cmd)
    try:
        result = subprocess.call(cmd)
        print('convert2odt status', result)
    except Exception as e:
        print("fatal error convert2odt =", result, filename,e, file=sys.stderr)
        traceback.print_exc()
        return(1)
    odtFile = filename.split('.')[0]+'.odt'
    return odtFile
    
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def zipdir(path, name):
    zf = zipfile.ZipFile(name, "w")
    for dirname, subdirs, files in os.walk(path):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()

def printhi(x):    
    print('hi',x)
    print(sys.version_info[0])
    print(sys.version_info)
    
#zipdir("dist", "dist\724.zip")