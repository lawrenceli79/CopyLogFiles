import sys
import os
import re
import tkinter as tk

if(len(sys.argv) < 5):
    print ("Usage:")
    print ("    py {} <LogListFile> <PCListFile> <TargetFolder> <nDays> ".format(os.path.basename(__file__)))
    sys.exit()

strLogListFile = sys.argv[1]
strPCListFile = sys.argv[2]
strTargetFolder = sys.argv[3]
nDays = int(sys.argv[4])

rgLogList = []
with open(strLogListFile) as fLogListFile:
    for line in fLogListFile:
        rgLogList.append(line.strip())

rgCheckBoxValue = []
rgCheckButton = []
top = tk.Tk()
for (i,item) in enumerate(rgLogList):
    CheckVar = tk.BooleanVar() 
    CheckVar.set(True)
    rgCheckBoxValue.append(CheckVar)
    CB = tk.Checkbutton(top, text=item, variable=CheckVar)
    CB.grid(sticky=tk.W)
    rgCheckButton.append(CB)
tk.Button(top, text="OK", command=top.quit).grid(sticky=tk.W)
top.mainloop()

def MakeRobocopyCmd(rgLogList, rgCheckBoxValue, src:str, dest:str, days:int) -> str:
    cmdStr = "robocopy {} {}".format(src, dest)
    for (i, LogName) in enumerate(rgLogList):
        if rgCheckBoxValue[i].get() == True:
            cmdStr += " " + rgLogList[i]
    cmdStr += " /nfl"
    cmdStr += " /maxage:{}".format(days)
    cmdStr += " /r:1"
    return cmdStr

with open(strPCListFile) as fPCListFile:
    for line in fPCListFile:
        fields = line.split()
        pcName = fields[0]
        srcFolder = fields[1]
        destFolder = strTargetFolder + "\\" + pcName
        cmdStr = MakeRobocopyCmd(rgLogList, rgCheckBoxValue, srcFolder, destFolder, nDays)
        print(cmdStr)
        os.system(cmdStr)

