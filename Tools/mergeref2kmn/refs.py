# create reference list
#  

import sys
import csv
# to do sort list 
# todo sorted(list, key=lambda x: x[1])
script = sys.argv[0]
logname = script.split('.')[0]
sys.stdout = open(logname+".log", "w",encoding="utf-8")

refList=[]

def writeCsv(arry):
    with open('refs.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(arry)

if len(sys.argv) > 1:
    with open(sys.argv[1]) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for line in readCSV:
            # 	Abihu	Abihu	e2de	Exod 28:1
            #,Abidah,Abidah,e2f3,Gen 25:4,
            name = line[1].strip()
            uec = line[3].strip()
            ref = line[4].strip()
            if ref:
                refList.append([name,uec,ref])
            else:
                continue
    
    writeCsv(refList)
    print ('\n*** done ****')
else:
    print("\nsyntax: fontforge -script refs.py 'dict with refs'")
    print("   i.e. fontforge -script refs.py trdict.csv")
    print("   note: expects name in column 1 and reference in column 4")
    print("   creates 'refs.csv' - list of references to place in kmn file")
