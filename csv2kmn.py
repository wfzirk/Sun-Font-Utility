'''
create SUN kmn file from SUN csv dictionary.
    
store(&VERSION) '9.0' U+0079
store(&TARGETS) 'any windows macosx linux web iphone ipad androidphone androidtablet mobile desktop tablet'
store(&KEYBOARDVERSION) '090026'
store(&LAYOUTFILE) 'Sun2-layout.js'
store(&NAME) 'sun7_6'
begin Unicode > use(main)

group(main) using keys

'Aaron' + ' ' > U+Eb0d
'Abel' + ' ' > U+EA96
'Abiathar' + ' ' > U+E35F
'abide' + ' ' > U+E17B
....    

'''
import fontforge
import os
import sys
import csv
from bfConfig import readCfg, bfVersion
from bfLogger import logger, setLogFile, closeLogFile

def get_header(name):
    logger.info('get_header %s', name)
    hdr = "store(&VERSION) '9.0' U+0079\n"
    hdr = hdr + "store(&TARGETS) 'any windows macosx linux web iphone ipad androidphone androidtablet mobile desktop tablet'\n"
    hdr = hdr + "store(&KEYBOARDVERSION) '090023'\n"
    hdr = hdr + "store(&LAYOUTFILE) 'Sun2-layout.js'\n"
    hdr = hdr + "store(&NAME) '"+name+"'\n"
    hdr = hdr + "begin Unicode > use(main)\n"
    hdr = hdr + "\ngroup(main) using keys"
    hdr = hdr + "\n\n"
    logger.info(hdr)
    return hdr
    
def build_row(name, unicode):  
    #   'Aaron' + ' ' > U+Eb0d
    row = "'"+name+"' + ' ' > U+"+unicode.lower()
    return row
    
def read_csv(f):
    cfg = readCfg()["langColumns"]
    ixu = cfg["index_unicode"]
    ixn = cfg["index_langName"]
    ixe = cfg["index_name"]
    logger.info('read_csv %s %s',f, cfg["index_langName"])
    csvData = []
    try:
        with open(f, encoding='utf8', newline='') as csvfile:
            data = list(csv.reader(csvfile))
            logger.debug('data %d %d',len(data), len(data[1]))
            logger.debug(cfg)
            cnt = 0
            for i in data:
                #logger.debug('%s %d %s %s',i, len(i), i[ixu],i[ixn], i[ixe])
                logger.debug('%d %s %s %s', cnt, i[ixu],i[ixn], i[ixe])
                unicode = i[ixu].lower()
                #log_info('unicode', unicode)
                name = i[ixn]
                if len(name) == 0:
                    #logger.error('length = 0')
                    continue
                #log_info('name',name, len(name))
                csvData.append(build_row(name, unicode)) 
                cnt += 1
                
    except Exception as  e:
            logger.exception("fatal error read_csv %s",e)
            #traceback.print_exc()
            return(1)  
            
    name_sort = sorted(csvData, key=lambda x: x[ixn].lower())
    return name_sort


# parse kmn file and generate csv file for documentation
def write_kmn(hdr, data, outfile):
    logger.info('write_kmn %s', outfile)
    try:
        fw = open(outfile, 'w')
        fw.write(hdr)
        for i  in data:
            logger.debug('kmn %s',i)
            wstr = i+'\n'
            fw.write(wstr)
    
    except Exception as  e:
        logger.exception("fatal error write_kmn %s",e)
        #traceback.print_exc()
        fw.close()
        return(1)
    
    fw.close()
    return(0)

    
def main(*ffargs):
    lgh = setLogFile('Log/'+__file__[:-3]+'.log') 
    logger.info('version %s', bfVersion)
    rc = 0 
    
    args = []
    for a in ffargs[0]:
        logger.debug(a)
        args.append(a)

    if len(args) > 4: 
        csvData = read_csv(args[1])
        logger.debug('csvdata len %d',len(csvData))
        if csvData:
            version = args[2]
            alias = args[3]
            outFile = args[4]
            name = outFile.split('.')[0]
            hdr = get_header(name)
            rc = write_kmn(hdr, csvData, outFile)
        else:
            logger.error('csvdata not valid')
            rc = 1
    else:
        logger.error("Create SUN kmn file from SUN csv dictionary.")
        logger.error(" i.e   fontforge -script csv2kmn.py infile.csv version alias outfile.kmn")
        rc = 1
        
    if rc == 0:
        logger.info('Done saved kmn file in %s \n', outFile)
    else:
        logger.error('finished with Errors status %d \n',status)
    
    closeLogFile(lgh)
    #sys.exit(rc)
    return(rc)
    
if __name__ == "__main__":
   
    logger.info(': '.join(sys.argv))
    rc = main(sys.argv) 
    sys.exit(rc)