#!/usr/bin/env fontforge -lang=py
# http://www.typophile.com/node/81351
# http://fontforge.github.io/scripting.html#Example
# https://fontforge.github.io/python.html
# https://stackoverflow.com/questions/14813583/set-baseline-with-fontforge-scriping
# https://www.reddit.com/r/neography/comments/83ovk7/creating_fonts_with_inkscape_and_fontforge_part10/

import fontforge
import sys
import os
import csv
import subprocess
import time
import glob
#import traceback
from bfLogger import logger, setLogFile, closeLogFile
from bfConfig import readCfg, bfVersion
 
cnt = 0
#imagemagic command  = 'convert -font Arial -pointsize 72 caption:%inp4% oxl.pnm'
def makeSVG(fontName, uniName, name, alias, debug):
    global cnt
   #log_info('  makesvg', fontName, ',',uniName, ',',name,',', alias)
    if uniName == 'e37e':
        svgFile = "e37e_period.svg"
        logger.info("using existing file %s",svgFile)
        #svgCopy(svgFile)
        return 0
    elif uniName == 'e390':
        svgFile = "e390_possesive.svg"
        logger.info("using existing file %s",svgFile)
        #svgCopy(svgFile)
        return 0
    elif uniName == 'ed11':
        svgFile = "ed11_pn.svg"
        logger.info("using existing file %s",svgFile)
        #svgCopy(svgFile)
        return 0
    else:
        if uniName == 'e316':
            name = '?'
            logger.info('generating ? as questionmark')
            
        svgFile = "Svg\\"+alias+"_"+uniName+".svg"
        pnmFile = "tmp.pnm"
        #pattern = "Svg\\*_"+uniName+"+*.svg"
        if glob.glob(svgFile):
            logger.warning('file pattern %s alreadyexists',uniName)
            return 0
        exists = os.path.isfile(svgFile)

        if not exists or debug:
            #cmd = "magick convert" + " -font "+fontName+" -pointsize 72 label:"+'"'+name+'"'+" tmp.pnm"
            cmd = "magick convert" + " -font "+fontName+" -pointsize 72 label:"+'"'+name+'"'+" "+pnmFile
            logger.info('magick convert %s',cmd)
            try:
                status = subprocess.call(cmd, shell=True)                #cmd = "potrace" +" --height 1.0 -s tmp.pnm -o "+'"'+svgFile+'"'
                cmd = "potrace" +" --height 1.0 -s "+pnmFile+" -o "+'"'+svgFile+'"'
                logger.info('   potrace %s %s ',status, cmd)
                if status == 0:
                    status = subprocess.call(cmd, shell=True)
                    #log_info('    ',status, cmd)
                if status != 0:    
                    logger.error('Error processing  %s %s',status, cmd)
                    return(status)
            except Exception as  e:
                logger.exception("fatal error makeSVG file  %s %s", svgFile,e)
                #traceback.print_exc()
                return(2)
        else:
            logger.warning('%d ***duplicate file %s',cnt,svgFile)  #, file=sys.stderr)
            #time.sleep(0.1)
            #log_warn('    ***Must delete existing files first')  #file=sys.stderr)
            #sys.stdout.flush()
            #return()
    cnt += 1
    return(0)

def read_list(fontname, csvFile, namelist=""):
    #cfg = json.load(open('config.json'))
    cfg = readCfg()
    alias = cfg["alias"]
    debug = (cfg["debug"] == "True")    
    print('debug',debug)
    if alias == 'EN':
        ixu = cfg["enColumns"]["index_unicode"]
        ixn = cfg["enColumns"]["index_name"]
    else:
        ixu = cfg["langColumns"]["index_unicode"]
        ixn = cfg["langColumns"]["index_langName"]
    status = 0
    try:
        logger.info('readlist %s %s %s',fontname, csvFile, namelist)
        with open(csvFile, encoding='utf8') as csvDataFile:
            csvReader = csv.reader(csvDataFile, delimiter=',', quotechar ='"')
            for row in csvReader:
                #logger.info('%s,%d %d',alias,ixn, ixu)
                logger.info(row)
                #logger.info('%s %s',row[ixn],row[ixu])
                ncol = len(row)
                name = row[ixn].strip()
                unicode = row[ixu].strip().lower()
                if len(name) == 0:
                    continue
                if namelist:
                    if unicode not in namelist:
                        #log_info(ixu,namelist, row[ixu],'not in namelist')
                        continue
                #log_info(name, unicode, ncol)
                if (len(row) < 3) or (len(row[ixu])) != 4: 
                    logging.info('wrong length '+len(row)+' '+len(row[ixu]))
                    continue

                if len(unicode) < 4:
                    status = makeSVG(fontname, name, name, alias, debug)
                else:
                    status = makeSVG(fontname, unicode, name, alias, debug)
                #time.sleep(0)   # allow interrupts
                if status != 0:
                    return status
                #time.sleep(0.005)
    except Exception as e:
        logger.exception("fatal error read_list %s",e)   # file=sys.stderr)
        #traceback.print_exc()
        return(3)
        
    return status
                

def main(*ffargs):   
    lgh = setLogFile('Log/'+__file__[:-3]+'.log') 
    logger.info('version %s', bfVersion)
    args = []
    rc = 0
    for a in ffargs[0]:
        logger.info('%s',a)
        args.append(a)
        

    if len(args) > 2: 
        csvFile = args[1]
        #alias = sys.argv[2].upper().strip()
        ttfFont = args[2].lower()
        #cg = getConfig('langinfo', language)
        namelist = ""
        if len(args) > 3:
            index = 0
            for arg in args:
                #log_info(index, arg)
                if index > 2:
                    namelist = namelist+'+'+arg.strip()
                index += 1
                
            if len(namelist) < 4:
                namelist = ""
                
        print('csvfile',csvFile)
        status = read_list(ttfFont, csvFile, namelist.lower())
        logger.info('read_list status %s',status)
        rc = status
    else:
        logger.warning("\nSYNTAX Error")
        logger.warning("\nsyntax: fontforge -script bfv2svg.py csvfile ttffile [unicode list]\n")
        logger.warning("   - script Python script file,  csvfile language fontfile\n")
        logger.warning("   optional space separated unicode list i.e. e000 eda5\n")
        logger.warning("\nCreates svg files in the /svg directory using\n")
        logger.warning("the names in the csv file\n")
        logger.warning("The csv file format \n")
        logger.warning("      glyph, unicode(hex), name\n")
        logger.warning("Optionally limits build to list of unicodes\n")
        rc = 1

    if rc == 0:
        logger.info('Done SVG files are in Svg directory')
    else:
        logger.error('Failed %d',rc)
    
    closeLogFile(lgh)
    #sys.exit(rc)
    return(rc)

if __name__ == "__main__":
   
    logger.debug('name main %s',sys.argv)
    rc = main(sys.argv) 
    sys.exit(rc)