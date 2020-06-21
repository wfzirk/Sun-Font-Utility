# routine to change glyph names in font
#  
'''
takes data from fontforge file to generate a list of unicodes and names
i.e.  Athens,eb08

invoke with:
fontforge -script glyphunicode.py  "Sunxxfont.sfd"	"csvfile name"

'''

import fontforge
import os
import sys
import csv
import logging
from tkinter import *
import time

from bfConfig import readCfg, bfVersion
from array2xlsx import array2xlsx
from bfLogger import logger, setLogFile, closeLogFile

    
def getUnicode(str):
    try:
        a = chr(int(str,16)).encode('utf-8')
        return a.decode('utf-8')
    except Exception as  e:
        logger.error("fatal error getUnicode %s",e)
        return 1

def listGlyphs(font):
    cfg = readCfg()
    DEBUG = cfg["debug"] == "true"
    IMAGEPOS = cfg["enColumns"]["index_font"]
    #LANGNAMEPOS = cfg["langColumns"]["index_langName"]
    UECPOS = cfg["enColumns"]["index_unicode"]
    ENNAMEPOS = cfg["langColumns"]["index_name"]
    
    cnt = 0
    glyphs = []
    for glyph in font:
        gl = [None, None, None]
        try:
            if font[glyph].unicode != -1:
                unicode = hex(font[glyph].unicode)[2:]
                if len(unicode) < 4:
                    continue;
                uic = getUnicode(unicode)
                name = font[glyph].glyphname.split('.')[0]
                #print(uic.encode().hex()+' '+unicode+' '+ name)
                #log_info(uic.encode().hex(),unicode, name)
                logger.info('lg:%s %s %s',uic.encode().hex(),unicode, name)
                gl[IMAGEPOS] = uic
                gl[ENNAMEPOS] = name
                gl[UECPOS] = unicode
                glyphs.append(gl)
                 
        except Exception as e:
            logger.exception("fatal error listGlyph %s",e)
            #traceback.print_exc()
            return 1,""
            
        if DEBUG:
            cnt = cnt+1
            if cnt>10:
                break
        #time.sleep(0.001)
                
    #sort by name        
    name_sort = sorted(glyphs, key=lambda x: x[ENNAMEPOS].lower())
    return 0, name_sort

def writeGlyphs(glyphs, outfile):
    logger.info('wrg %s',outfile)
    fw = open(outfile, 'w' ,encoding='utf8', newline='')
    csvWriter = csv.writer(fw)
    count = 0
    for g in glyphs:
        try:
            csvWriter.writerow(g)
        except Exception as e:
            logger.exception("fatal error writeGlyphs %s",e)
            #traceback.print_exc()
            return 2
        #time.sleep(0.001)
    fw.close()   
    return 0

def main(*ffargs):
    lgh = setLogFile('Log/'+__file__[:-3]+'.log') 
    logger.info('version %s', bfVersion)
    args = [] 
    for a in ffargs[0]:
        logger.debug('input ffargs %s',a)
        args.append(a)

    rc = 0
    if len(args) > 2: 
        fontName  = args[1]
        outfile = args[2]
        try:
            font = fontforge.open (fontName)
            rc,glyphs = listGlyphs(font)
            if rc == 0:
                rc = writeGlyphs(glyphs, outfile)
            if rc == 0:
                array2xlsx(glyphs, outfile[:-4]+'.ods')

        except Exception as e:
            #log_err("fatal error ",e)
            #traceback.print_exc()
            #logging.exception("Deliberate divide by zero traceback")
            logger.exception(e)
            rc = 1
    else:
        logger.warning("\n  SYNTAX: fontforge -script sfd2csv.py fontforgefile.sfd csvfile.csv")
        logger.warning("  Takes data from fontforge file to generate a csv file of symbols,")
        logger.warning("  unicodes and names")
        logger.warning("  i.e. symbol,eb08,Athens")
        rc = 1
        
    if rc != 0:
        logger.error("failed status = %s",rc)
    else:
        logger.info("Done!  The csv file is in %s", outfile)
    
    closeLogFile(lgh)
    #sys.exit(rc)
    return rc
    
if __name__ == "__main__":

    logger.info(': '.join(sys.argv))
    rc = main(sys.argv) 
    sys.exit(rc)