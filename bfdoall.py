
# https://www.tcl.tk/man/tcl/TkCmd/ttk_widget.htm
# https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-state-spec.html

import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkFont
from tkinter import ttk
from tkinter import scrolledtext
import subprocess
from csv import reader
from bfConfig import *

root = tk.Tk()

root.title("SUN Font Utility    "+bfVersion)
root.resizable(width=False, height=False)
#root.geometry('{}x{}+{}+{}'.format(300, 200, 100, 150))
 
# Gets the requested values of the height and widht.
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
#print("Width",windowWidth,"Height",windowHeight)
 
# Gets both half the screen width/height and window width/height
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/5 - windowHeight/2)
 
# Positions the window in the center of the page.
root.geometry("+{}+{}".format(positionRight, positionDown))
 
#hFont = tkFont.Font(family="Helvecta", size=10)
default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(size=11)
root.option_add("*Font", default_font)

cfg = readCfg()
cfg["eFilter"] = "" 
#updateVars()
    
lb_entry = {}
# https://www.loc.gov/standards/iso639-2/php/code_list.php
'''
ISO 639-2 Code,	ISO 639-1 Code,	English name of Language,	French name of Language,	German name of Language,	Comment 
    aar,                	aa,                     	Afar,                                           	afar,                       	Danakil-Sprache	          
'''
#import sys
def get_langlist(lb_entry, csv_file):
    print('get_langlist')
    csv_file = cfg["language_codes"]
    ALIASCOL = 1    # col 0 = 3 letter alias,  col 1 = 2 letter alias
    if ALIASCOL ==1:
        ACOLLEN = 2   
    else:
        ACOLLEN = 3
    NAMECOL = 2
    with open(csv_file, 'r') as read_obj:
        csv_reader = reader(read_obj)
        x = 0
        for item in list(csv_reader):
            lang = item[NAMECOL]
            #print(item[NAMECOL], item[0], item[1], len(item[ALIASCOL]))
            if x > 0:
                #listbox.insert("end", item[1]) 
                if len(item[ALIASCOL]) == ACOLLEN:
                    lb_entry[lang] = item[ALIASCOL].upper()
            x = x+1
    print('lb_entry',type(lb_entry), lb_entry)   
    #name_sort = sorted(lb_entry.items(), key=lambda kv: kv[NAMECOL].lower()) 
    key_sort = dict(sorted(lb_entry.items(), key=lambda item: item[0]))
    print('key sort', key_sort)
    #sys.exit(1)
    return key_sort

def updateVars():
    print('update vars',cfg["alias"], 'vars updated')
    #cfg["sunFontName"] = os.path.basename(cfg["sfdFile"]).split('.')[0]
    updateCfg(cfg)
    CB.setState()
    e0.delete(0,tk.END)
    e0.insert(0,cfg["version"])
    
    e1.delete(0,tk.END)
    e1.insert(0,cfg["language"])
    _alias.delete(0,tk.END)
    _alias.insert(0,cfg["alias"])
    
    ttfName = os.path.basename(cfg["ttf"])
    ttf.delete(0, tk.END)
    ttf.insert(0, ttfName)
    sfdName = os.path.basename(cfg["sfdFile"])
    sfd.delete(0, tk.END)
    sfd.insert(0, sfdName)
    kmnName = os.path.basename(cfg["kmnFile"])
    kmn.delete(0, tk.END)
    kmn.insert(0, kmnName)
    trlName = os.path.basename(cfg["trlangFile"])
    trl.delete(0, tk.END)
    trl.insert(0, trlName)
    
    #print('end updatevars',cfg["alias"])
    return
   


def bfExit(e):
    saveCfg(cfg)
    writeBat(cfg)
    root.destroy()
    quit()

def bfCancel(e):
    root.destroy()
    quit()
    
def langClicked(event):
    # https://www.loc.gov/standards/iso639-2/php/code_list.php
    '''
   ISO 639-2 Code,	ISO 639-1 Code,	English name of Language,	French name of Language,	German name of Language,	Comment 
        aar,                	aa,                     	Afar,                                           	afar,                       	Danakil-Sprache	          
    '''
    selection = event.widget.curselection()
    #print('langclicked',selection)
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        print(data)
        e1.delete(0, tk.END)
        e1.insert(0, data)
        #e1.configure(text=data)
        print(lb_entry[data])
        cfg["language"] = data
        cfg["alias"] = lb_entry[data]
        _alias.delete(0, tk.END)
        _alias.insert(0, lb_entry[data])
    else:
        e1.configure(text="")
    
def versionClicked(e):
    sv = e0.get()
    b = sv
    cfg["version"] = sv
    print('versionclicked',sv, cfg["version"])
    updateVars()
    
def xaliasClicked(v):
    global cfg
    a = _alias.get().upper()
    #lookup = {value: key for key, value in cg.langParms}
    found = False
    #print('ac',a)
    for k in langParms:
        value = langParms[k]
        #print(k, value)
        if value == a:
            found = True
            break
    print('aliasclicked',k,value, found)
    if found:
        cfg["language"] = k
        cfg["alias"] = a
        #setVisible()
        updateVars()  

def efltrClicked(e):
    cfg["eFilter"] = efltr.get()
    updateCfg(cfg)
        
    
def ttfClicked(e):
    cfg["ttf"] = filedialog.askopenfilename(filetypes = (("Text files","*.ttf"),("all files","*.*")))
    updateVars()
 
def sfdClicked(e):
    cfg["sfdFile"] = filedialog.askopenfilename(filetypes = (("Text files","*.sfd"),("all files","*.*")))
    #sfdName = os.path.basename(cfg["sfdFile"])
    #sfd.delete(0, tk.END)
    #sfd.insert(0, sfdName)
    updateVars()
    
def kmnClicked(e):
    cfg["kmnFile"] = filedialog.askopenfilename(filetypes = (("Text files","*.kmn"),("all files","*.*")))
    updateVars()
    
def trlClicked(e):
    cfg["trlangFile"] = filedialog.askopenfilename(filetypes = (("Text files","*.ods"),("all files","*.*")))
    updateVars()
    


class TextIO:
    def __init__(self, text):
        self.text = text
    def write(self, msg):
        self.text.update_idletasks()
        self.text.insert(END, msg)
        self.text.see(END)
    def flush(self):
        pass 

class CB(tk.Frame):
    # https://stackoverflow.com/questions/4236910/getting-checkbutton-state
    alias = cfg["alias"]
    chkbs = []  # array of checkboxes
    def __init__(self, parent=None, cheater=""):
        tk.Frame.__init__(self, parent)
        #self.var = tk.BooleanVar()
        #self.chkbs = []    # array of checkboxes
        ckbtn = ttk.Checkbutton(self, text=cheater)   #, anchor=tk.W)
        #      variable=self.var, onvalue=1,\
        #      offvalue=0, command=runCmd)
        ckbtn.state(['!disabled','!selected','!alternate']) # clear the checkbox
        ckbtn.pack(side=tk.LEFT, expand=1, fill=tk.X)

        CB.chkbs.append(ckbtn)
        self.grid(columnspan=2, sticky='w')     #, columnspan=2)
        CB.cbState(ckbtn)
    
    def cbState(chk):
        ste = bfCmds(cfg, chk.cget("text"))[0]
        print(CB.alias, ste, chk.cget("text"))
        s = False
        if ste == 'both':
            s = True
        elif CB.alias == 'eng' and ste == CB.alias:
            s = True
        elif ste != 'eng' and CB.alias != 'eng':
            s = True
        if s:
            chk.state(['!disabled','!selected','!alternate'])
        else:
            chk.state(['disabled','!selected','!alternate'])

    def setState():
        CB.alias = cfg["alias"]
        for i in CB.chkbs:
            CB.cbState(i)
            
    def clrAll(self):
        CB.alias = cfg["alias"]
        for i in CB.chkbs:
            i.state(['!selected'])
            
    def setAll(self):
        CB.alias = cfg["alias"]
        for i in CB.chkbs:
            i.state(['selected'])
    
    
    #chkbs = []  # array of checkboxes
    def runCmd(self):
        updateCfg(cfg)
        for i in CB.chkbs:
            #print(i.state())
            cmd = bfCmds(cfg, i.cget("text"))[1]
            lge = bfCmds(cfg, i.cget("text"))[0]   #" language"
            sel = i.instate(['selected','!disabled'])
            #ena = i.instate(['!disabled'])
            print('rncmd', lge, i.cget("text"), sel, cmd)
            if not sel:
                continue

            ffcmd = ['cmd', '/c', 'fontforge', '-quiet', '-script']
         
            for c in cmd:
                ffcmd.append(c)
            
            p = subprocess.Popen(ffcmd,
                               stdout=subprocess.PIPE,
                               #stderr=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               text=True,
                               bufsize=1,
                               #cwd='C:\\',
                               shell=True)
                               
            for line in p.stdout:
                print(line, end='')
                textBox.insert(tk.END, line)
                textBox.see(tk.END)
                textBox.update_idletasks()
            print('returncode',p.returncode)
  

top_frame = tk.Frame(root, bg='cyan', width=400, height=25, pady=1)
center = tk.Frame(root, bg='lightblue', width=395, height=150, padx=5, pady=5)
ctr_btm = tk.Frame(root, bg='lightblue', width=395, height=200, padx=5, pady=5)
#right =  tk.Frame(root, bg='lightgreen', width=100, height=350, padx=5, pady=5)
btm_frame = tk.Frame(root, bg='white', width=400, height=25, pady=3)


top_frame.grid(row=0, columnspan=2,sticky="ew")
center.grid(row=1,column=0, sticky="nsew")
ctr_btm.grid(row=2,column=0, sticky="nsew")
#right.grid(row=1,column=1, rowspan=2, sticky="nsew")
btm_frame.grid(row=3, columnspan=2, sticky="ew")


# create the center frames
center.grid_rowconfigure(0, weight=1)
center.grid_columnconfigure(1, weight=1)
center.grid_columnconfigure(2, weight=1)
center.grid_columnconfigure(3, weight=1)
center.grid_columnconfigure(4, weight=1)

#  add widgets to center left
row = 1
lbl0 = tk.Label(center, bg='lightblue', text="Version", width=8, anchor=tk.W)
lbl0.grid(row=row, column=0, sticky=tk.W)
e0 = tk.Entry(center, width=22, relief=tk.RIDGE) #, textvariable=bfClass.version)
e0.grid(row=row, column=1, sticky=tk.W)
e0.bind('<KeyRelease>', versionClicked)
tk.Label(center, bg='lightblue', text="i.e. 78_1210", anchor=tk.W).grid(row=row, column=3, columnspan=2, sticky=tk.W)

row = row+1
lbl1 = tk.Label(center, bg='lightblue', text="Language", width=8, anchor=tk.E, padx=1,pady=1)
lbl1.grid(row=row, column=0, sticky=tk.W)
#tk.Label(center, bg='lightblue', text="i.e. EN", anchor=tk.W).grid(row=row, column=3, columnspan=2, sticky=tk.W)


lb_frame = tk.Frame(center, bg='lightgray')
lb_frame.grid(row=row, column=1, columnspan=1,  sticky=tk.W)

e1 = tk.Entry(lb_frame)   #, width=12)  #, textvariable=bfClass.language)
e1.grid(row=0, column=1, columnspan=2,sticky="ew")
#e1.bind('<KeyRelease>', langClicked)
#tk.Label(center, bg='lightblue', text="i.e. EN", anchor=tk.E).grid(row=row, column=5, columnspan=2, sticky="ew")
tk.Label(center, bg='lightgreen', text="i.e. EN", anchor=tk.W).grid(row=row, column=2, columnspan=2, sticky=tk.N)

listbox = tk.Listbox(lb_frame, width=20, height=6)
scrollbar = tk.Scrollbar(lb_frame, orient="vertical", command=listbox.yview)
listbox.configure(yscrollcommand=scrollbar.set)
listbox.grid(row=1, column = 1, sticky=tk.W)
listbox.bind("<<ListboxSelect>>", langClicked)
scrollbar.grid(row=1, column=2, sticky='ns')

csv_file = ('Language Codes.csv') 
lb_entry= get_langlist(lb_entry, csv_file)
print('lbentry',lb_entry)
for lbe in lb_entry:
    print(lbe)
    listbox.insert("end", lbe)


lbl2 = tk.Label(center, bg='lightblue', text="Alias",width=4, anchor=tk.W)
lbl2.grid(row=row, column=3, sticky=tk.E)
_alias = tk.Entry(center,bg='lightyellow', width=8)
_alias.grid(row=row, column=4, sticky=tk.W)
#e2.bind('<KeyRelease>', aliasClicked)


row = row+2
lbl3a = tk.Label(center, bg='lightblue', text="Font File", width=8, anchor=tk.W)
lbl3a.grid(column=0, row=row, sticky=tk.W)   #, columnspan=1)
ttf = tk.Entry(center,width=22,bg='lightyellow')
ttf.grid(column=1, row=row, sticky=tk.W, columnspan=3)
#ttf.insert(0, bfClass.ttf)
ttf.bind("<1>", ttfClicked)
tk.Label(center, bg='lightblue', text="i.e. times.ttf",  anchor=tk.W).grid(row=row, column=3, columnspan=2, sticky=tk.W)

row = row+1
lbl3 = tk.Label(center, bg='lightblue', text="SFD File")
lbl3.grid(column=0, row=row, sticky=tk.W, columnspan=1)
sfd = tk.Entry(center,width=22)
sfd.grid(column=1, row=row, sticky=tk.W, columnspan=4 )
#sfd.insert(0, bfClass.sfdFile)
sfd.bind("<1>", sfdClicked)
tk.Label(center, bg='lightblue', text="i.e. sun7_8_1210.sfd",  anchor=tk.W).grid(row=row, column=3, columnspan=2, sticky=tk.W)

row = row+1
lbl4 = tk.Label(center, bg='lightblue', text="KMN File")
lbl4.grid(column=0, row=row, sticky=tk.W, columnspan=1)
kmn = tk.Entry(center,width=22)
kmn.grid(column=1, row=row, sticky=tk.W, columnspan=4 )
#kmn.insert(0, bfClass.kmnFile)
kmn.bind("<1>", kmnClicked)
tk.Label(center, bg='lightblue', text="i.e. sun7_8_1210.kmn",  anchor=tk.W).grid(row=row, column=3, columnspan=2, sticky=tk.W)

#Translators Dictionary Sun 7_22 on 8_9_2019_fixed.ods
row = row+1
lbl6 = tk.Label(center, bg='lightblue', text="TRLang File")
lbl6.grid(column=0, row=row, sticky=tk.W, columnspan=1)
trl = tk.Entry(center,width=22)
trl.grid(column=1, row=row, sticky=tk.W, columnspan=4 )
#trl.insert(0, bfClass.trlangFile)
trl.bind("<1>", trlClicked)
tk.Label(center, bg='lightblue', text="Tr...Dict...xxx.ods",  anchor=tk.W).grid(row=row, column=3, columnspan=2, sticky=tk.W)

cncl = tk.Button(btm_frame, text = "Cancel") 
cncl.pack(side=tk.RIGHT)
cncl.bind("<1>", bfCancel)

ext = tk.Button(btm_frame, text = "Save", padx=5) 
ext.pack(side=tk.RIGHT)
ext.bind("<1>", bfExit)
     

if __name__ == "__main__":
    #cfg = readCfg()
    #cfg["eFilter"] = "" 
    updateVars()
    root.mainloop()