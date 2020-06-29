
import os
import sys

import json
import version

bfVersion = version.get_version()
print(bfVersion)

cfg = { 
    "bfVersion":"",
    "filePath": "dist/",
    "version": "",
    "alias": "",
    "language": "",
    "sfdFile": "",
    "kmnFile": "", 
    "trlangFile": "",
    "ttf": "",
    "pwFile": "",
    "pwLangFile": "",
    "backFont": "",
    "kmncsv": "",
    "back2doc": "",
    "csv2kmnFile": "",
    "compactFile": "",
    "zipFile": "",
    "synxref":"",
    "readMe":"",
    "sunFontName": "",
    "enColumns": {"index_font": 0, "index_name": 1, "index_unicode": 2},
    "langColumns": {"index_font": 0, "index_name": 1, "index_langName": 2,
                    "index_unicode": 3},
    "eFilter": "",
    "debug": "false"
    }

langParms = {\
    "Russian":"RU",\
    "Spanish":"ES",\
    "French":"FR",\
    "Portuguese":"PT",\
    "English":"EN"}


def updateCfg(cfg):
    #print('updatecfg',cfg["alias"], cfg["version"])
    cfg["pwFile"] = cfg["filePath"]+"pw"+cfg["version"]+"_EN.csv"
    cfg["pwLangFile"] = cfg["filePath"]+"pw"+cfg["version"]+"_"+cfg["alias"]+".csv"
    cfg["backFont"] = cfg["filePath"]+"SUNBF"+cfg["version"]+"_"+cfg["alias"]      
    cfg["kmncsv"] = cfg["filePath"]+"kmn"+cfg["version"]+"_EN.csv"
    cfg["back2doc"] = cfg["filePath"]+"back"+cfg["version"]+"_"+cfg["alias"]+".txt"
    cfg["compactFile"] = cfg["filePath"]+"compact"+cfg["version"]+"_"+cfg["alias"]+".ods"
    cfg["csv2kmnFile"] = cfg["filePath"]+"sun"+cfg["version"]+"_"+cfg["alias"]+".kmn"
    cfg["zipFile"] = cfg["filePath"]+"SUN"+cfg["version"]+"_"+cfg["alias"]+".zip"
    cfg["readMe"]  = cfg["filePath"]+"readMe.csv"
    cfg["debug"] = "False"
    if "debug" in cfg["eFilter"].lower():
        cfg["debug"] = "True"
    if cfg["eFilter"]:
        cfg["debug"] = "True"
    saveCfg(cfg)   

def bfCmds(cfg, script):
    cmd = {\
        "sfd2csv": ['EN',['sfd2csv.py', cfg["sfdFile"], cfg["pwFile"]]],   
        "langpri": ['lang',['langpri.py', cfg["pwFile"], cfg["trlangFile"], cfg["pwLangFile"]]], 
        "kmn2csv": ['EN',['kmn2csv.py', cfg["kmnFile"], cfg["kmncsv"]]],
        "csv2kmn": ['lang',['csv2kmn.py', cfg["pwLangFile"], cfg["version"], cfg["alias"], cfg["csv2kmnFile"]]],
        "csv2svg": ['both',['csv2svg.py', cfg["pwLangFile"], cfg["ttf"], cfg["eFilter"]]],
        "svg2font": ['both',['svg2Font.py', cfg["pwLangFile"], cfg["ttf"], cfg["alias"],\
             cfg["backFont"], cfg["eFilter"]]],
        "back2doc": ['both',['back2doc.py', cfg["pwLangFile"], cfg["back2doc"]]],
        "compact": ['both',['compact4x16.py', cfg["pwLangFile"], cfg["compactFile"]]],
        "bfzip": ['both',['bfZip.py'] ] 
    }
    return cmd[script]

    
def saveCfg(cfg):    
    prevcfg = readCfg()
    if prevcfg != cfg:
        json.dump(cfg, open('config.json', 'w'),  indent=4)
        writeBat(cfg)
        print('cfg saved')

    
def readCfg():  
    #global cfg
    dumpit = False
    cfgFile = os.path.isfile('config.json')
    if cfgFile:
        rdcfg = json.load(open('config.json'))
        
        if bfVersion != rdcfg["bfVersion"]:
            #rdcfg["bfVersion"] = bfVersion
            print('bfversion',bfVersion)
            dumpit = True
        for k in cfg:
            if k not in rdcfg:
                print(k,'not in rdcfg')
                dumpit = True
                break

    if dumpit:
        print('dumpit')
        cfg["bfVersion"]=bfVersion
        json.dump(cfg, open('config.json', 'w'),  indent=4)     
        rdcfg = cfg

    return rdcfg

def writeBat(cfg):
    batEnv = "set sfd="+cfg["sfdFile"]+"\n"\
        +"set kmn="+cfg["kmnFile"]+"\n"\
        +"set ver="+cfg["version"]+"\n"\
        +"set ttffont="+cfg["ttf"]+"\n"\
        +"set alias="+cfg["alias"]+"\n"\
        +'set langIn="'+cfg["trlangFile"]+'"\n'\
        +"set langOut=SUNBF"+cfg["version"]+"_"+cfg["alias"]+".sfd"

    f = open('doEnv.bat', 'w')
    f.write(batEnv) 
    f.close()

if __name__ == "__main__":
   
    cfg = readCfg()
   