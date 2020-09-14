# create synonym list and merge with xref file
# 

import fontforge
import os
import sys
import csv
import logging


script = sys.argv[0]
logname = script.split('.')[0]
sys.stdout = open(logname+".log", "w",encoding="utf-8")
 
#priData = []
#xrefData = []
#synData = {}    # dictionary file of synonymns {key=unicode, value= synonyms}
xuniCol = 2     # unicode column in xref
xnameCol = 1    # name column in xref 
xrefCol = 3     # xref column in xref
xglyphCol = 0     # fontforge glyph
puniCol = 2     # unicode column in primary
pnameCol = 1    # name column in primary

def getUnicode(str):
    a = chr(int(str,16)).encode('utf-8')
    #print('getunicode hex:',str,' unicode:', a.hex(), a.decode('utf-8'))
    return a.decode('utf-8')

# merge xref and synonyms  p=primary, x = xref, s = synonymn    
def mergeXrefSyn(p,x, s):
    print('mergexrefsyn',type(p),type(x), type(s))
    data = []
    #xd = arry2Obj(x)
    #print('xd ==============')
    #print(xd)
    #print('xdmiss ==============')
    #print(xdmiss)
    for uec in p:
        word = p[uec]
        print(uec,word)
        item = []
       
        print('mergexrefsyn',uec, 'in', uec in s, uec in x)
        #if uec in s:
        if s.get(uec) != None:
            synlist = s[uec]
            item.append(uec)
            item.append(word)
            item.append(synlist)
        else:
            item.append(uec)
            item.append(word)
            #if not uec in s: 
            if not s.get(uec): 
                item.append("")
            else:
                #item.append(s[uec])
                #item[1] = '*'+item[1]
                # Because of typos resulting in miscompares in name and uec
                # an attempt is made to flag it and fix the problem
                #str = s.get(uec)
                print('error ',uec, word, ' not in synonymn', s.get(uec))
            
        #if uec in x:
        if x.get(uec) != None:
            item.append(x[uec])
        else:
            #item.append(u'\uF09E')
            #str = xdmiss.get(uec)
            # Because of typos resulting in miscompares in name and uec
            # an attempt is made to flag it and fix the problem
            '''if str == None:
                item.append("")
            else:          
                item.append(xdmiss.get(uec))
                item[1] = '*'+item[1]
            '''    
            #i[4] = i[4]+" "+u'\uF09E'
            print('error1 ',uec, word ,' not in xref', item)

        data.append(item) 

    return(data)

def writesynxref(outfile, ddata):
    print('wrtexref')
    with open(outfile, 'w', encoding='utf8') as f:
        for row in ddata:
            print(len(row), row)
            name = row[1].strip()
            uec = row[0].strip().lower()
            syn = row[2].strip()
            if len(row) < 4:
                xref = ""
            else:
                xref = row[3].strip()
            #print(uec, xref, type(xref))

            if "," in xref:
                xref = '"'+xref+'"'
            unicode = getUnicode(uec)
            print('uic',unicode,name,syn,uec,xref)
            f.write(unicode+','+name+','+syn+','+uec+','+xref+'\n')    

# e03e, persecution persecute tribulation
def read_syn(f):
    syn = {}
    with open(f, encoding='utf8', newline='') as csvfile:
        data = list(csv.reader(csvfile))
        #print(data)
        for i in data:
            if len(i)== 2:
                #print(i)
                unicode = i[0].strip().lower()
                syn[unicode] = i[1]
    #print('syn',type(syn))
    return syn
            
# "ea5b","man: king,master,ruler,lord: love,compassion" 
def read_xref(f):
    xd = {}
    with open(f, encoding='utf8', newline='') as csvfile:
        data = list(csv.reader(csvfile))
        for i in data:
            unicode = i[0].strip().lower()
            xref = i[1]
            xd[unicode] = xref
    
    return xd

# ,eb78,Dionysius
def read_pri(f):
    pd = {}
    with open(f, encoding='utf8', newline='') as csvfile:
        data = list(csv.reader(csvfile))
        for i in data:
            symbol = i[xglyphCol]
            unicode = i[puniCol].strip().lower()
            name = i[pnameCol]
            pd[unicode] = name
    #print('x', type(xd))        
    #print(xd)
    return pd

 
ix = 0
print(len(sys.argv))
for arg in sys.argv:
    print(ix,arg)
    ix=ix+1
 
#  pw7251.csv xref7251.csv syn.csv  synxref7251.csv
if len(sys.argv) > 3: 
    priData = {}
    xrefData = {}
    synData = {}
    priData = read_pri(sys.argv[1])
    print('pridata-------------------------------------')
    print(priData)
    xrefData = read_xref(sys.argv[2])
    print('xrefdata-------------------------------------')
    print(xrefData)
    synData = read_syn(sys.argv[3])
    print('synData -------------------------------------')
    print(synData)
    mergeData = mergeXrefSyn(priData, xrefData, synData)
    print('mergeData-------------------------------------')
    print(mergeData)
    writesynxref(sys.argv[4], mergeData)
    #writesyn('synonyms.csv', mergeData)
else:
    print("\nsyntax: fontforge -script synxref.py primary.csv xref.csv output.csv")
    print("Creates a synonym file and a merged xref and synonym file")
    print("Also creates 'syn.csv' as a separate file")

print ('\n*** done ****')


