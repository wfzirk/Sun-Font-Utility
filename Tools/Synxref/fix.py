# create synonym list and merge with xref file
# 

import os
import sys
import csv
import logging


script = sys.argv[0]
logname = script.split('.')[0]
sys.stdout = open('Log\\'+logname+".log", "w",encoding="utf-8")


def read_pri(f, wr):
    pd = []
    with open(f, encoding='utf8', newline='') as csvfile:
        wr = open(wr, 'w', encoding='utf8')
        data = list(csv.reader(csvfile))
        for i in data:
            #symbol = i[0]
            #unicode = i[3].lower()
            #name = i[1]
            #xref = i[4]
            #syn = i[2]
            #ast = ""
            i[3] = i[3].lower()
            #print( "<<<" in xref, xref)
            if "<<<" in i[4]:
                print('in xref')
                i[4] = i[4].replace("<<<err word>>>", "")
                i[4] = i[4]+" "+u'\uF09E'
            #if "," in xref:
            #    xref = '"'+xref+'"'
           
            #print(len(i),i)
            outStr = ""
            for j in i:
                #print(len(j), j)
                outStr = outStr+'"'+ j +'",'
            outStr = outStr[:-1]   # remove last char of string
            outStr = outStr+'\n'
            #outStr = '"'+symbol+'", "'+ast+'", "'+name+'", "'+syn+'", "'+unicode+'", "'+xref+'"\n'  
            print(outStr)
            wr.write(outStr)
            #print(symbol+','+ast+','+name+','+syn+','+unicode+','+xref)
            #wr.write(symbol+','+ast+','+name+','+syn+','+unicode+','+xref+'\n')    

    return 

read_pri("synxref724-10.csv", "sxout.csv")

print ('\n*** done ****')


