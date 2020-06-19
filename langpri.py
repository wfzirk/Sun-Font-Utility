
import os
import sys
import csv
#import traceback
from util import convert2csv, unicode2hex
from array2xlsx import array2xlsx
from bfConfig import readCfg
from bfLogger import logger, setLogFile, closeLogFile


cfg = readCfg()  
pwSym = cfg["enColumns"]["index_font"]
pwUec = cfg["enColumns"]["index_unicode"]
pwName = cfg["enColumns"]["index_name"] 
# "","brothers","e007","hermanos",,
langSymCol = cfg["langColumns"]["index_font"]
langUniCol = cfg["langColumns"]["index_unicode"]
enNameCol =  cfg["langColumns"]["index_name"] 
langNameCol = cfg["langColumns"]["index_langName"] 

def readLang(file, priList):
    # due to everyone using their own column order an attempt is
    # made to standardize file into sym, enname, langname, unicode
    # assume sym col is always 0
    lsymcol=0
    lencol=0
    lunicol=0
    langcol=0
    # spanish       ,sisters,e00f,hermanas,,
    # portuguese    ,abomination,abominação,e0a4


    try:
        logger.info("readlang %s",file)
        f = open(file, 'r', encoding="utf-8")
        reader = csv.reader(f, delimiter=',', quotechar='"')
        #sort by name
        uic_sort = sorted(reader, key=lambda x: x[1].lower())

        row = uic_sort[5]      # pick arbitrary 5th row  make sure not header
        #print(len(uic_sort), len(row),row)
        if len(row) > 3:
            uic = row[lsymcol].strip()   # the first column should contain symbol
            ux = unicode2hex(uic)
            for i in range(len(row)):
                u = '0x'+row[i]
                if ux == u.lower():     # unicode matches symbol unicode
                    #print('uec match',i,u, ux)
                    lunicol = i
                if row[i] in priList:   # english name column matches
                    #print('ename match', i, row[i])
                    lencol = i
            if lunicol == 0 or lencol == 0:
                logger.error(' could not determine unicode col %d en col %d len col %d',lunicol, lencol)
                return(1)
                
            for i in range(len(row)):       # get column for language
                if i == lsymcol or i==lunicol or i==lencol:
                    continue
                else:
                    langcol = i
                    break
    except Exception as e:
        logger.exception('readLang file  error: %s',e)
        #traceback.print_exc()
        return(1)          
    #logger.info('langList','cols = sym',lsymcol,'name', lencol,'lang', langcol,'unicode', lunicol) 
    logger.info('langList  symcol %d namecol %d langcol %d unicode %d',lsymcol, lencol, langcol, lunicol) 
    logger.info('langCols %d %d %d %d', langSymCol, enNameCol, langNameCol, langUniCol)
    if lsymcol == langSymCol and lencol == enNameCol and langcol == langNameCol and lunicol == langUniCol:
        logger.info("columns Match")
    else:
        logger.warning("columns don't match, reordering columns")
  
    name_sort = sorted(uic_sort, key=lambda x: x[lencol].lower()) 
    
    langList = {}
    for n in name_sort:
        #logger.info('langtodict %s %s',n, n[lencol])
        logger.debug('langtodict %s %s', n[lencol], n[lunicol])
        sym = n[lsymcol].strip()
        eName = n[lencol].strip()
        lName = n[langcol].strip()
        uec = n[lunicol].strip().lower()
        langList[n[lencol]] = [sym,eName,lName,uec]  #english word as key
        
    return langList  # lang file reordered columns and sorted by name

#
def fixLangList(langList):
    logger.info('fixlanglist duplicate names')
    #cnt = 0;
    ln = {}   # create dict with langName as key
    try:
        for i in langList:
            lName = langList[i][langNameCol]
            luec = langList[i][langUniCol]
            #print('fix %s', i, langList[i][langNameCol])
            logger.debug('fix '+i+' '+langList[i][langNameCol]+':'+luec)
            if lName in ln:
                #logger.warning('Duplicate names %s %s %s using first name',lName,langList[i][3],ln[lName][3])
                #print('logger warning Duplicate names '+lName, end='')
                logger.warning('Duplicate names '+lName+':'+luec+'->'+ln[lName][3])  #+' '+ %s %s %s using first name',lName,langList[i][3],ln[lName][3])
                continue
            ln[lName] = langList[i]
        ll = {}   
    except Exception as e:
        print('logger exception',e)
        logger.exception(e)
        return ''
    for i in ln:
        ename = ln[i][1]
        ll[ename] = ln[i]
        
    return(ll)    
    
        

def mergeLists(enList, langList):
    mList = []
    try:
        for eName in enList:
            logger.debug('ename %s %s',eName, enList[eName][1])
        
            eUec = enList[eName][1].strip()
            eSym = enList[eName][0]
            if eName in langList:
                logger.debug('match %s %s',eName, langList[eName][langNameCol])
                #print('match %s %s',eName, langList[eName])
                #logger.info('match '+eName+' '+langList[eName][langNameCol])
                lName = langList[eName][langNameCol].strip()
                lUec = langList[eName][langUniCol].strip()
                if lUec != eUec:
                    logger.warning(">>>unicode mismatch<<<, use primary unicode., %s %s %s",eName, eUec, lUec)
                if ' ' in lName:
                    logger.warning("---Name Error---, name contains spaces replace with '_', %s", lName)
                    lName = lName.replace(' ','_')
                #mList.append([eSym, eName, lName, eUec])
            else:
                #logger.warning('***Name*** not used  %s for %s ignore row',eName,cfg["language"])
                logger.warning('***Name*** not used  %s:%s,  name blank for %s ',eName,lUec,cfg["language"])
              
                lName = ""
            mList.append([eSym, eName, lName, eUec])
        # sort by language column
        #name_sort = sorted(mList, key=lambda x: x[langNameCol])  #, reverse=True) 
        # sort by english column
        name_sort = sorted(mList, key=lambda x: x[enNameCol].lower())  #, reverse=True) 
    except Exception as e:
        logger.exception(e)
        return ''     
    return name_sort
        
def readENPri(pwfile):
    try:
        nameList = {}
        with open(pwfile, 'r', encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            for row in reader:
                uic = row[pwSym].strip()
                name = row[pwName].strip().strip('"').strip("'")
                uec = row[pwUec].strip().strip('"').strip('"').lower()
                #pwname = pwname+':'+name
                #pwuec = pwuec+':'+uec.lower()
                nameList[name] = [uic,uec]
            logger.info('primary name list created')
            #logger.info(nameList)
    except Exception as e:
        logger.exception('readEnPri error:%s',e)
        #traceback.print_exc()
        return(1)
        
    return nameList

def main(*ffargs):
    base=os.path.basename(ffargs[0][0])
    lgh = setLogFile('Log/'+base[:-3]+'.log') 
    logger.info('start %s',base)
    rc = 0
    
    args = []
    for a in ffargs[0]:
        logger.debug( a)
        args.append(a)
 
    if len(args) > 2: 
        pwFile  = args[1]
        langFile = args[2]
        pwLangFile = args[3]
        
        try:
            lExt = langFile[-3:].strip().lower()   
            logger.debug('ext %s','|'+lExt+'|')
            if lExt == '.csv':
                csvFile = langFile
            elif lExt == 'ods':
                csvFile = convert2csv(langFile)
            else:
                logger.exception('Wrong type of File only csv or ods files accepted')
                rc = 2
            if rc == 0:    
                logger.info('***')
                enList = readENPri(pwFile)   
                logger.info('****')            
                langList = readLang(csvFile, enList)
                if langList:
                    #dicFile = cfg["langFile"]
                    langList = fixLangList(langList)
                    if langList:
                        mList = mergeLists(enList, langList)
                        if mList:
                            array2xlsx(mList, pwLangFile)
                            fods = pwLangFile.split('.')[0]+'.ods'
                            fcsv = convert2csv(fods, 'dist')
                            if fcsv == 1:
                                rc = 1
                        else:
                            rc = 1
                    else:
                        rc = 1
                else:
                    rc = 1
            
        except Exception as e:
            logger.exception('Error %s',e)
            rc = 1

    else:
        logger.error("\n  SYNTAX: fontforge -quiet -script langpri.py pw%ver%_EN.csv %langFile%, outfile") 
        logger.error("Creates 'langpw.csv' as a list of all primary words in language")
        rc = 1
    
    if rc == 0:
        logger.info('done file in %s',pwLangFile)
    else:
        logger.error("Error could not complete commands status = %d",rc)
    
    closeLogFile(lgh)
    return(rc)
   
if __name__ == "__main__":
   
    logger.info(': '.join(sys.argv))
    rc = main(sys.argv)
    print('returncode =',rc)
    sys.exit(rc)