# https://stackoverflow.com/questions/867866/convert-unicode-codepoint-to-utf8-hex-in-python

import fontforge
import os
import sys
import csv
import traceback

# parse kmn file and add reference as comment

def xupdate_kmn(kmnfile,outFile, refList):
    with open(kmnfile, 'r') as fr:
        with open(outFile, 'w') as fw:
            csvReader = csv.reader(fr, delimiter='+')
            # 'Aaron' + ' ' > U+Eb0d
            for row in csvReader:
                l = len(row)
                if l == 3:
                    if '>'  in row[1]:
                        csvRow = [None, None, None, None]
                        #log_info(row)
                        unicode = row[2].strip().strip('\"').strip("\'").lower()
                        name = row[0].strip().strip('\"').strip("\'")
                        #print(row)
                        print(name) 
                        if name in refList:
                            row.append('   c\t\t '+refList[name])
                            print(row)
                wstr = ""
                for i in row:
                    wstr=wstr+i
                fw.write(wstr+'\n')
        
def update_kmn(kmnfile,outFile, refList):
    with open(kmnfile, 'r') as fr:
        with open(outFile, 'w') as fw:
            kmnData = fr.readlines()
            # 'Aaron' + ' ' > U+Eb0d
            for row in kmnData:
                row = row.rstrip(os.linesep)
                line = row.split('+')
                if len(line) > 2:
                    if '>'  in line[1]:
                        #csvRow = [None, None, None, None]
                        #log_info(row)
                        unicode = line[2].strip().strip('\"').strip("\'").lower()
                        name = line[0].strip().strip('\"').strip("\'")
                        #print(row)
                        print(name) 
                        if name in refList:
                            row = row + '   c\t\t '+refList[name]
                            print(row)
                
                fw.write(row+'\n')
                



def readRefs():
    refsList = {}
    # Abel	ea96	Gen 25:4

    with open('refs.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))
        #print(data)
        for n in data:
            #print(n)
            refsList[n[0]] = n[2]  # name as key, ref as value
    return refsList       

def main(argv):
    rc = 0
    if len(argv) == 3: 
        kmnFile = argv[1]
        outFile = argv[2]
        try:
            refArry = readRefs()
            if refArry:
                update_kmn(kmnFile,outFile, refArry)
            else:
                rc = 1
        except Exception as e:
            print('Error ', e)
            traceback.print_exc()
            rc = 1
        
    else:
        print("\nsyntax: fontforge -script merge.py kmnfile refsfile")
        print("  i.e. - script Python script file,  SUN7_251.kmn kmnout.kmn")
        print("expects refs.csv to exist as name, unicode, reference")
        rc = 1
  
    if rc == 0:
        print('done file is in %s',outFile)
    else:
        print("failed status = %s",rc)
    

    return(rc)

            
if __name__ == "__main__":

    sys.exit(main(sys.argv))