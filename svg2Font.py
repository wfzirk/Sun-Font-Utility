
# http://fontforge.github.io/scripting.html#Example
# https://fontforge.github.io/python.html
# https://stackoverflow.com/questions/14813583/set-baseline-with-fontforge-scriping
# https://www.reddit.com/r/neography/comments/83ovk7/creating_fonts_with_inkscape_and_fontforge_part10/
# http://designwithfontforge.com/en-US/Importing_Glyphs_from_Other_Programs.html
#https://pelson.github.io/2017/xkcd_font_raster_to_vector_and_basic_font_creation/

import fontforge as ff
import psMat
import os
import sys
#import subprocess
import csv
import os.path
#from os import walk
#import time
from bfLogger import logger, setLogFile, closeLogFile
from bfConfig import readCfg 
 

ffMetrics = {}  # font metrics taken from font

'''    
   Font         ascent  _____
   Metrics      xheight _____   scale = 200/xheight
   scaling      base    _____   height =200  scale = xheight / 200
                descent _____   d = font_descender / scale
                
   wordMax and wordMin are whole word metrics calculated from font for each word
   ff_asc, ff_dsc, ff_height taken from the defult font metrics for all of font
'''

def getWord(word):
    maxt = 0
    minb = 0
    ww = []
    for w in word:
        g = ffMetrics["ttfFont"][ord(w)]
        name = g.glyphname
        left, bot, right, top = g.boundingBox()
        name = g.glyphname
        ww = [bot, top]
        b = ww[0]
        t = ww[1]
        if b < minb:
            minb = b
        if t > maxt:
            maxt = t

    #log_info('getWord %20s \t%s \t%s'%(word, minb, maxt))
    #sys.stdout.flush() 
    return minb, maxt


def scale(glyph):   #, wordMin, wordMax):
    global desc_scale
    wordMin, wordMax = getWord(glyph.glyphname)
    printBound(glyph,'Image Size')
    iL, iB, iR, iT = glyph.boundingBox()

    # scale to word
    iH = iT - iB
    wH = wordMax - wordMin
    wScale = wH/iH
 
    scale_matrix = psMat.scale(wScale)
    glyph.transform(scale_matrix)
    
    s = 200/ffMetrics['xheight']
    #log_info('scale to FF',round(s,2))
    logger.debug('scale to FF %5.2f',s)
    scale_matrix = psMat.scale(s)
    glyph.transform(scale_matrix)
    
    # move image vertically 
    sL, sB, sR, sT = glyph.boundingBox()
    y = 300 - sB + (wordMin * s)
    base_matrix = psMat.translate(0, y)
    glyph.transform(base_matrix)
    #log_info('move y: %s bot: %s desc:%s'%(round(y,2), round(sB,2), round((wordMin*s),2)))
    logger.debug('move y: %5.2f bot: %5.2f desc:%5.2f', y, sB, (wordMin*s))
    printBound(glyph,'Moved ')
 
def printBound(glyph, comment = ""):
    left, bot, right, top = glyph.boundingBox()
    #log_info(comment,'bound height:', round((top-bot),2), 'bot:',round(bot,2), 'top:',round(top,2), 'width:',round((right-left),2),'lb:',round(glyph.left_side_bearing,2), 'rb:',round(glyph.right_side_bearing,2))
    logger.debug('%s bound height: %5.2f bot: %5.2f top:%5.2f width:%5.2f lb:%5.2f rb:%5.2f', comment, (top-bot), bot, top, (right-left), glyph.left_side_bearing, glyph.right_side_bearing)
   
def setBearing(glyph):
    left, bot, right, top = glyph.boundingBox()
    
    glyph.width = int(right) - int(left) + 150
    glyph.left_side_bearing = 75
    glyph.right_side_bearing = 75
    #log_info('bearing', round(glyph.left_side_bearing,2), round(glyph.right_side_bearing,2), round(right-left, 2))
    logger.debug('bearing left:%5.2f right:%5.2f width:%5.2f', glyph.left_side_bearing, glyph.right_side_bearing, (right-left))
    
def addFont(font, unicode, alias, imagename):  #, mn, mx) :
    
    if unicode == 'e37e':
        file = "e37e_period.svg"
        glyph = font.createChar(int(unicode, 16))
        glyph.importOutlines(file)  
        return
    elif unicode == 'e390':
        file = "e390_possesive.svg"
        glyph = font.createChar(int(unicode, 16))
        glyph.importOutlines(file) 
        return
    elif unicode == 'ed11':
        file = "ed11_pn.svg"
        glyph = font.createChar(int(unicode, 16))
        glyph.importOutlines(file) 
        return
    else:
    
        try:
            file = "svg\\"+alias+"_"+unicode+".svg"
            exists = os.path.isfile(file)
            if exists:
                #logger.info("------------------------------------")
                logger.debug('addFont file %s %s %s', file, unicode, imagename)
                
                if unicode == -1:
                    glyph = font.createChar(-1, imagename)
                else:
                    glyph = font.createChar(int(unicode, 16))
                glyph.importOutlines(file)  
                glyph.glyphname = imagename
                scale(glyph)    #, mn, mx)
                setBearing(glyph)           
            else:
                logger.warning("file %s does not exist", file)
                return(2)
        except Exception as e:
            logger.exception('exception %s',e)
            #traceback.print_exc()
            return(1)
       
def createFont(backfont):    #, ver, section):
    #fontname = 'SUNBF'+ver+'_'+section
    #f = backfont.split('.')

    fontname = os.path.basename(backfont)
    print('fontname', fontname)

    #fontname = f[0]
    ascent = 1000
    descent = 800
    em = 1000
    encoding = "Custom"
    weight = "Regular"
    #font = fontforge.font()
    ffont = ff.font()
    ffont.fontname = fontname
    ffont.familyname = fontname
    ffont.fullname = fontname
    ffont.ascent = ascent
    ffont.descent = descent
    ffont.em = em
    ffont.encoding = encoding
    ffont.weight = weight
    ffont.save(backfont+'.sfd')

    return ffont

def read_list(font, csvFile, alias, namelist=""):
    logger.info('readlist %s %s',csvFile, namelist)
    if 'debug' in namelist:
        namelist = namelist.replace("+debug","")
  
    cfg = readCfg()
    alias = cfg["alias"]
    if alias == "EN":
        ixu = cfg["enColumns"]["index_unicode"]
        ixn = cfg["enColumns"]["index_name"]
    else:
        ixu = cfg["langColumns"]["index_unicode"]
        ixn = cfg["langColumns"]["index_langName"]
    try:
        with open(csvFile, encoding='utf8') as csvDataFile:
            csvReader = csv.reader(csvDataFile, delimiter=',', quotechar ='"') 
            for row in csvReader:
                #log_info(len(row), row)
                #time.sleep(0)       # allow time for caller to read output
                if (len(row) < 3) or (len(row[ixu])) != 4: 
                    continue
                ncol = len(row)
                unicode = row[ixu].lower()
                name = row[ixn]
                #print('readlist namelist', namelist, unicode, unicode not in namelist)
                
                if namelist:
                    #print('if namelist', namelist, unicode, unicode not in namelist)
                    if unicode not in namelist:
                        continue
                #log_info(row[ixn], row[ixu], row[ixEN], ncol) 
                unicode = row[ixu].lower()
                name = row[ixn].strip() 
                addFont(font, unicode, alias, name)   #, float(mn), float(mx))

    except Exception as  e:
        logger.exception("fatal error read_list %s",e)
        #traceback.print_exc()
        return(1)
        
    return 0
    
def getMetrics(ttfFile, ttfFont):
    global ffMetrics
    v = {}
    v['ttfFile'] = ttfFile
    v['ttfFont'] = ttfFont
    v['xheight'] = float(ttfFont.xHeight)
    v['ascender'] = float(ttfFont.os2_typoascent)
    v['descender'] = float(ttfFont.os2_typodescent)
    ffMetrics = v
    #log_info('ffmetrics ascent= %s descent= %s xHeight= %s'%(v['ascender'], v['descender'], v['xheight']))
    logger.info('ffmetrics ascent= %s descent= %s xHeight= %s'%(v['ascender'], v['descender'], v['xheight']))


def main(*ffargs):
    base=os.path.basename(ffargs[0][0])
    lgh = setLogFile('Log/'+base[:-3]+'.log') 
    logger.info('start %s',base)
    args = []
    for a in ffargs[0]:
        logger.debug(a)
        args.append(a)
        
    rc = 0
    if len(args) > 4: 
        try:
            csvFile = args[1]
            ttfFile = args[2]
            alias = args[3].upper()
            #backFont = args[4].split('.')[0]
            backFont = args[4][:-3]+'_'+alias
            print('arg4',backFont)
            #ttfFont = fontforge.open(ttfFile) 
            ttfFont = ff.open(ttfFile)
            getMetrics(ttfFile, ttfFont)
            font = createFont(backFont)     #, ver, section)
            namelist = ""

            if len(args) > 5:
                index = 0
                for arg in args:
                    #log_info(index, arg)
                    if index > 4:
                        namelist = namelist+'+'+arg.strip().lower()
                        #log_info('namelist =',namelist, len(namelist))
                
                    index += 1
                if len(namelist) < 4:
                    namelist = ""
            logger.info('namelist = %s, %d',namelist, len(namelist))
            rc = read_list(font, csvFile, alias, namelist)
            if rc == 0:
                logger.info('Saving %s.sfd %d',backFont, rc)
                status = font.save(backFont+".sfd")
                logger.info('status = %s',status)

                logger.info('Generating %s.ttf',backFont)
                if not namelist:
                    status = font.generate(backFont+".ttf")
                    logger.info('status = %s',status)
                
                logger.info('Generating %s.woff',backFont)
                if not namelist:
                    status = font.generate(backFont+".woff")
                    logger.info('status = %s', status)

        except Exception as e:
            logger.exception('exception %s',e)
            #traceback.print_exc()
            rc = 1
       
    else:
        logger.error("\nsyntax: fontforge -script svg2Font.py backFont.sfd csvfile fontfile alias [unicode list]")
        logger.error("   Creates a back font from the svg files in /svg directory")
        logger.error("   using the names in the pw file for font characteristics")
        logger.error("   Optionally limits build to list of unicodes")
        logger.error("   -script Python script file,  Fontforge file  csvfile( The dictionary file)")
        logger.error("   language 2 character i.e. EN")
        logger.error("   optional space separated unicode list i.e. e000 eda5")
        logger.error("   The csv file is expected to have:")
        logger.error("      symbol in column 0, unicode in column 1 english word in column 2 and")
        logger.error("      language words in column 3. \n   Optionally limits build to list of unicodes")
        rc = 1
        
    if rc == 0:
        logger.info('\nDone saved font files in %s .ttf |.woff |.sfd', backFont)
    else:
        logger.error('Failed %d',rc)
    
    closeLogFile(lgh)
    return rc

if __name__ == "__main__":
   
    logger.info(': '.join(sys.argv))
    rc = main(sys.argv) 
    sys.exit(rc)