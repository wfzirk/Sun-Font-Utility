#!/usr/bin/env fontforge -lang=py
# http://www.typophile.com/node/81351
# http://fontforge.github.io/scripting.html#Example
# https://fontforge.github.io/python.html
# https://stackoverflow.com/questions/14813583/set-baseline-with-fontforge-scriping
# https://www.reddit.com/r/neography/comments/83ovk7/creating_fonts_with_inkscape_and_fontforge_part10/
# http://designwithfontforge.com/en-US/Importing_Glyphs_from_Other_Programs.html
#https://pelson.github.io/2017/xkcd_font_raster_to_vector_and_basic_font_creation/

import fontforge
import sys
import csv

import os.path
#from os import walk


script = sys.argv[0]
logname = script.split('.')[0]
sys.stdout = open(logname+".log", "w",encoding="utf-8")


xsymbol = 0
xname = 1
xsynonym = 2
xunicode = 3
xxref = 4

def getXrefList(file, outfile):
    print('getXrefList',file)
    fr = open(file, encoding='utf8')
    reader = csv.reader(fr, delimiter=',', quotechar ='"')
    fw = open(outfile, 'w')
    #writer = csv.writer(fw, delimiter=',', quotechar ='"')
    try:
        count = 0
        for row in reader:
            print(len(row))
            if len(row) > 1:
                key = row[3]
                value = row[4].replace("+u'\uF09E'","")
                print(value, u'\uF09E' in value)
                #xrefList[key] = value
                count = count + 1
                wr = '"'+key+'","'+value+'"'
                print(wr)
                #print(wr)
                fw.write(wr+'\n')
            
    except:
        
        print('error the fields must be separated by "|"') 
        print('All fields must be quoted  with " ') 
        sys.exit(1)
        
    fr.close()    
    fw.close()
    #print(xrefList)
    #for i in xrefList:
        #print(i, '\t\t',xrefList[i])

x = 0      
for arg in sys.argv:
    print( x,arg)
    x=x+1
print(len(sys.argv))
if len(sys.argv) > 1: 
    xrefFile = sys.argv[1]
    getXrefList(xrefFile, "xref.csv")

else:
    print("\nsyntax: fontforge -script xref.py")
    print("  creates xref.csv from  existing xref dictionary")
    sys.exit()

print('Done')

    