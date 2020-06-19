
#https://stackoverflow.com/questions/30349542/command-libreoffice-headless-convert-to-pdf-test-docx-outdir-pdf-is-not	


import os
import sys
import subprocess
import inspect
import zipfile
import time
from datetime import timedelta
from bfLogger import logger
#import inspect

#frame_records = inspect.stack()[1]
#calling_module = inspect.getmodulename(frame_records[1])
#print('calling',calling_module)

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
'''    
'''

def setup_logger(name):
    global logger
    # set up logging to file - see previous section for more details
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='Log/'+name+'.log',
                        filemode='w')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger(name)
    return logger

logger = logging.getLogger()

class logColor:
    ERROR = "\033[1;31;47m"
    WARNING = '\033[93m'
    

def log_traceback(ex, ex_traceback=None):
    if ex_traceback is None:
        ex_traceback = ex.__traceback__
    tb_lines = [ line.rstrip('\n') for line in
                 traceback.format_exception(ex.__class__, ex, ex_traceback)]
    #exception_logger.log(tb_lines)
    #tb_lines = ERROR+tb_lines
    #logger.error(tb_lines)
    log_err(tb_lines)

def log_info(*args):
    #global lcnt
    line = ' '.join([str(a) for a in args])
    #print('INFO',line)
    logger.info(line)
    
def log_err(*args):
    #global lcnt
    line = ' '.join([str(a) for a in args])
    #print('ERROR',line)
    line = logColor.ERROR+line
    logger.error(line)





logger = logging.getLogger(__name__)
print('util',logger)
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
'''
'''
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
        
    logger.info('convert2text %s',cmd)
    try:
        result = subprocess.call(cmd)
        logger.info('convert2text status %s', result)
    except Exception as e:
        logger.exception("fatal error convert2text %S %S %s", result, filename,e)
        #traceback.print_exc()
        return(1)
    txtFile = filename[:-4]+'.txt'
    return txtFile
   
   
def convert2csv(filename, outdir=""):
    # https://wiki.openoffice.org/wiki/Documentation/DevGuide/Spreadsheets/Filter_Options#Filter_Options_for_the_CSV_Filter
    #cmd = "C:\Program Files\LibreOffice\program\soffice"+  " --convert-to csv"+ " --infilter=CSV:44,34,76,1,,,true "+ filename
    cmd = ["C:\Program Files\LibreOffice\program\soffice", "--convert-to", "csv", "--infilter=CSV:44,34,76,1,,,true ", filename]
    #log_info("convert2csv",cmd)
    if outdir:
        cmd.append("--outdir")
        cmd.append(outdir)
        
    logger.info('convert2csv %s',filename)
    try:
        result = subprocess.call(cmd)
        logger.info('convert2csv status %s', result)
    except Exception as e:
        logger.exception("fatal error convert2csv %s %s %s", result, filename,e)
        #traceback.print_exc()
        return(1)
    csvFile = filename[:-4]+'.csv'
    return csvFile
        

def convert2ods(filename, outdir=""):	
    cmd = ["C:\Program Files\LibreOffice\program\soffice", "--headless", "--convert-to", "ods", "--infilter=CSV:44,34,76,1,,,true", filename]
    #cmd = "C:\Program Files\LibreOffice\program\soffice"+ " --headless"+ " --convert-to ods"+ " --infilter=CSV:44,34,76,1,,,true "+ filename   # + " --outdir dist"
    if outdir:
        #cmd = cmd+" --outdir "+outdir
        cmd.append("--outdir")
        cmd.append(outdir)
        
    logger.info('convert2ods %s',filename)
    try:
        result = subprocess.call(cmd)
        logger.info('convert2ods status %s', result)
    except Exception as e:
        logger.exception("fatal error convert2ods %s %s %s",result,filename,e)
        #traceback.print_exc()
        return(1)
    odsFile = filename[:-4]+'.ods'
    return odsFile

# https://stackoverflow.com/questions/30349542/command-libreoffice-headless-convert-to-pdf-test-docx-outdir-pdf-is-not	
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
        
    logger.info('convert2pdf %s',filename)
    try:
        result = subprocess.call(cmd)
        logger.info('convert2pdf status %s', result)
    except Exception as e:
        logger.exception("fatal error convert2pdf %s %s %s", result, filename,e)
        #traceback.print_exc()
        return(1)
    pdfFile = filename[:-4]+'.pdf'
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
        
    logger.info('convert2odt %s',filename)
    try:
        result = subprocess.call(cmd)
        logger.info('convert2odt status %s', result)
    except Exception as e:
        logger.exception("fatal error convert2odt %s %s %s", result, filename,e)
        #traceback.print_exc()
        return(1)
    odtFile = filename[:-4]+'.odt'
    return odtFile
    
'''   
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
'''