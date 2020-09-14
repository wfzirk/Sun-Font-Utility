# compare kmn file and sfd file looking for missing or changed items
# kmn file contains both primary and synonyms. 
# log file contains miscompares

import sys
import csv
from util import convert2odt

def exitApp():
    sys.exit() 
script = sys.argv[0]
logname = script.split('.')[0]
#sys.stdout = open(logname+".log", "w",encoding="utf-8")

#kmnfile = "kmnSUN7_24.csv"      #contains all words from kmn file
#pwfile = "pw724.csv"            #contains primary words from sfd file

#kmnname = ""
#kmnuec = ""
kmn_uec = {}
kmn_name = {}
pw_uec = {}
pw_name = {}

def kmn(kmnfile):
    with open(kmnfile, 'r', encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for row in reader:
            name = row[1].strip()
            uec = row[2].strip().lower()
            #kmnname = kmnname+':'+name
            #kmnuec = kmnuec+':'+uec
            kmn_uec[name] = uec
            kmn_name[uec] = name
        #print('kmnname',kmnname)
        #print('kmnuec',kmnuec)


def pw(pwfile):
    #pwname = ""
    #pwuec = ""	
    with open(pwfile, 'r', encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for row in reader:
            name = row[1].strip()
            uec = row[2].strip().lower()
            #pwname = pwname+':'+name
            #pwuec = pwuec+':'+uec
            pw_uec[name] = uec
            pw_name[uec] = name
        #print('pwname',pwname)
        #print('pwuec',pwuec)


def output(out):
    with open(out, 'w') as f:
        '''
        print('Not in '+pwfile+'\n')
        pwlist = pwname.split(':')
        for name in pwlist:
            if name not in kmnname:
                print('o notin kmnname',name)

        ueclist = pwuec.split(':')        
        for uec in ueclist:
            if uec not in kmnuec:
                print('o notin kmnuec',uec)
            
        print('\nNot in '+kmnfile+'\n')
        kmnlist = kmnname.split(':')
        for name in kmnlist:
             if name not in pwname:
                print('n not in pwname',name)
                
        ueclist = kmnuec.split(':')
        for uec in ueclist:
             if uec not in pwuec:
                print('n not in pwuec',uec)
        ''' 
        print('Compare names')
        f.write('Compare names\n')
        for uec in pw_name:
            name = pw_name[uec]
            if uec == 'e316':
                continue
            if uec == 'e37e':
                continue
            #print(uec, name, '****', kmn_name.get(uec),kmn_uec.get(name))
            #print('words incorrect')
            if kmn_uec.get(name) == None:
                #print('Misscompare', uec, name, '\t\t not in kmn found --',kmn_name.get(uec), '-- instead')
                print('{:20s}{:8s} not in kmn found --{}'.format(name, uec, kmn_name.get(uec)))
                f.write('{:20s},{:8s}, not in kmn found --{}\n'.format(name, uec, kmn_name.get(uec)))
        print('\nCompare unicodes\n')
        f.write('\nCompare unicodes\n')
        for name in pw_uec:
            uec = pw_uec[name]
            #print(un, '***', kmn_uec[un])
            if kmn_name.get(uec) == None:
                #print('Misscompare',uec, name, '\t\t not in kmn found --', kmn_uec.get(name), '-- instead')    
                print('{:20s}{:8s} not in kmn found --{}'.format(name, uec, kmn_uec.get(name)))
                f.write('{:20s},{:8s}, not in kmn found --{}\n'.format(name, uec, kmn_uec.get(name)))
        
        print('\nExtra unicodes\n')
        f.write('\nExtra unicodes\n')
        for name in kmn_uec:
            uec = kmn_uec[name]
            #print(un, '***', kmn_uec[un])
            if pw_name.get(uec) == None:
                print('{:20s}{:8s} not in kmn found --{}'.format(name, uec, pw_uec.get(name)))
                f.write('{:20s},{:8s}, not in kmn found --{}\n'.format(name, uec, pw_uec.get(name)))
        f.close()
        print('\nOutput File is in',out) 
    
    convert2odt(out)
 
ix = 0
print(len(sys.argv))
for arg in sys.argv:
    print(ix,arg)
    ix=ix+1
 
#  pw7251.csv xref7251.csv syn.csv  synxref7251.csv
if len(sys.argv) > 3: 
    pw(sys.argv[1])
    kmn(sys.argv[2])
    output(sys.argv[3])

else:
    print("\nsyntax: fontforge -script compare.py primary.csv kmn.csv compare.txt")
    print("Creates a synonym file and a merged xref and synonym file")
    print("Also creates 'syn.csv' as a separate file")

print ('\n*** done ****')


 