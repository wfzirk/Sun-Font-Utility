# create synonymn list
#  requires input list sorted by unicode
# syntax:  synonyms.py infile > outfile

import sys
# to do sort list 
# todo sorted(list, key=lambda x: x[1])
script = sys.argv[0]
logname = script.split('.')[0]
sys.stdout = open(logname+".log", "w",encoding="utf-8")

if len(sys.argv) > 1:
    with open(sys.argv[1], 'r', encoding='utf8') as f:
        fw = open('syn.csv', 'w')
        prevuec = '***'
        prevname = '***'
        count = 0
        for line in f:
            ln = line.split(",")
            ref = ln[3].strip()
            if len(ref) > 0:
                ref = '('+ref+')'
                
            name = ln[1].strip()+' '+ref
            uec = ln[2].strip()
            #ref = '('+ln[3].strip()+')'
            #symbol,name,uec=line.split(",")
            if uec == prevuec:
                count = count+1
                if count > 1:
                    fw.write(' '+ name)
                else:	
                    fw.write('\n'+uec+', '+ name+' '+prevname)
            else:
                count = 0
                fw.write('\n'+uec+', '+ ref)

            prevuec = uec
            prevname = name

    print ('\n*** done ****')
else:
    print("\nsyntax: fontforge -script synonyms.py kmn.csv")
    print("   i.e. fontforge -script synonyms.py kmnSUN7_6.csv")
    print(" NOTE: must be sorted by unicode column")
    print("   creates 'syn.csv' - list of synonyms in the kmn file")
