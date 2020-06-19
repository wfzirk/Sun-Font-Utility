# https://stackoverflow.com/questions/867866/convert-unicode-codepoint-to-utf8-hex-in-python

import fontforge
import os
import sys
import csv
#import traceback
from util import getUnicode
from bfLogger import logger, setLogFile, closeLogFile
from bfConfig import readCfg  
 
def read_csv(namelist, outfile):
    try:
        #cfg = json.load(open('config.json'))
        cfg = readCfg()
        if cfg["alias"] == "EN":
            ixu = cfg["enColumns"]["index_unicode"]
        else:
            ixu = cfg["langColumns"]["index_unicode"]
        logger.info('read_csv namelist:%s outfile:%s',namelist,outfile)
        fr = open(namelist, 'r', encoding='utf8')
        fw = open(outfile, 'w' , encoding='utf8')
        csvReader = csv.reader(fr, delimiter=',')
        for row in csvReader:
            logger.debug(row);
            uic = row[ixu].strip()
            if uic != "":
                unicode = getUnicode(uic)
                fw.write(unicode)
        fr.close
        fw.close()
        return 0
    except Exception as e:
        logger.exception('exception %s',e)
        #traceback.print_exc()
        return(1)
 
def main(*ffargs):  
    base=os.path.basename(ffargs[0][0])
    lgh = setLogFile('Log/'+base[:-3]+'.log') 
    logger.info('start %s',base)
    args = []
    for a in ffargs[0]:
        logger.debug(a)
        args.append(a)


 
    if len(args) == 3: 
        infile = args[1]
        outfile = args[2][:-4]+'.txt'
        
    else:
        logger.warning("\nsyntax: fontforge -script back2doc.py output.txt")
        logger.warning("\nCreates a backfont text file for verification of word alignment")
        return 1

    rc = read_csv(infile, outfile)
    if rc == 0:
        #convett2odt(outfile)
        logger.info("Done!  The backdoc file is in %s", outfile)
    else:
        logger.error('Failed %d',rc)
    
    closeLogFile(lgh)
    #sys.exit(rc)
    return(rc)

if __name__ == "__main__":
   
    logger.info(': '.join(sys.argv))
    rc = main(sys.argv) 
    sys.exit(rc)