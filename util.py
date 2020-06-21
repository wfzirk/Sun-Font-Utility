
#https://stackoverflow.com/questions/30349542/command-libreoffice-headless-convert-to-pdf-test-docx-outdir-pdf-is-not	


import os
import sys
import subprocess
import inspect
import zipfile
import time
from datetime import timedelta
from bfLogger import logger

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
    
