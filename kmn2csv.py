# https://stackoverflow.com/questions/867866/convert-unicode-codepoint-to-utf8-hex-in-python

import fontforge
import os
import sys
import csv

from util import getUnicode
from bfConfig import readCfg 
from bfLogger import logger, setLogFile, closeLogFile
from array2xlsx import array2xlsx

'''
def getUnicode(str):
    #log_info('getunicode', str)
    a = chr(int(str,16)).encode('utf-8')
    #log_info('getunicode hex:'+str+' unicode:'+ a.hex())  # "+' '+a.decode('utf-8'))
    return a.decode('utf-8')
'''
   
# parse kmn file and generate csv file for documentation

def read_kmn(kmnfile):
    #cfg = json.load(open('config.json'))["enColumns"]
    cfg = readCfg()
    enc = cfg["enColumns"]
    DEBUG = cfg["debug"] == "true"
    cnt = 0
    kmnAry = []
    fr = open(kmnfile, 'r')
    #fw = open(outfile, 'w' ,encoding='utf8')
    csvReader = csv.reader(fr, delimiter='+')
    #csvWriter = csv.writer(fw, delimiter=',', lineterminator='\n')
    for row in csvReader:
        l = len(row)
        if l == 3:
            if '>'  in row[1]:
                csvRow = [None, None, None]
                #log_info(row)
                unicode = row[2].strip().strip('\"').strip("\'").lower()
                uic = getUnicode(unicode)
                name = row[0].strip().strip('\"').strip("\'")
                csvRow[enc["index_font"]] = uic
                csvRow[enc["index_name"]] = name
                csvRow[enc["index_unicode"]] = unicode
                logger.info('%s %s %s',uic.encode().hex(),unicode, name)
                kmnAry.append(csvRow)
                #csvWriter.writerow(csvRow)
                
        if DEBUG:
            cnt = cnt+1
            if cnt>20:
                break


    fr.close()

    name_sort = sorted(kmnAry, key=lambda x: x[enc["index_name"]].lower())
    
    # note: need to sort this by name

    return name_sort
'''
# parse kmn file and generate csv file for documentation
def write_kmn(arry, outfile):
    #cfg = json.load(open('config.json'))["enColumns"]
    #cfg = readCfg()["enColumns"]
    #kmnAry = []
    #fr = open(namelist, 'r')
    fw = open(outfile, 'w' ,encoding='utf8')
    #csvReader = csv.reader(fr, delimiter='+')
    csvWriter = csv.writer(fw, delimiter=',', lineterminator='\n')
    for row in arry:
        csvWriter.writerow(csvRow)

    fw.close()

    return 0
'''


def main(*ffargs):
    base=os.path.basename(ffargs[0][0])
    lgh = setLogFile('Log/'+base[:-3]+'.log') 
    logger.info('start %s',base)
    rc = 0

    args = []
    for a in ffargs[0]:
        logger.debug('%s',a)
        args.append(a)

    if len(args) == 3: 
        namelist = args[1]
        outFile = args[2]
        try:
            kmnAry = read_kmn(namelist)
            if kmnAry:
                cfg = readCfg()
                array2xlsx(kmnAry, outFile[:-4]+'.ods', csv=True)
            else:
                rc = 1
        except Exception as e:
            logger.exception("fatal error %s",e)
            rc = 3
    else:
        logger.error("\nsyntax: fontforge -script kmn2csv.py %kmn%.kmn kmn%kmn%.csv")
        logger.error("  i.e. - script Python script file,  SUN7_251.kmn kmnSUN7_251.csv")
        rc = 1
    
    if rc == 0:
        logger.info('done file is in %s',outFile[:-4]+'.ods')
    else:
        logger.error("failed status = %s",rc)
    
    closeLogFile(lgh)
    #sys.exit(rc)
    return(rc)

if __name__ == "__main__":
   
    logger.info('name main %s',sys.argv)
    rc = main(sys.argv)    
    sys.exit(rc)