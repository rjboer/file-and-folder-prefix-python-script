import os
import sys
import string
import re
import time

startpath = "/home/bi/Desktop/test"

pattern1 = re.compile(r"[^\d\W]")
pattern2 = re.compile(r"[^\w^\.\s]")
pattern3 = re.compile(r"\s+")
dnumberlist = []
#cannot remember why I added this...

debug=False
# print debug messages

files=True
#number files

folders=True
#number folders

gitignore=True
# ignore .git files

sanatizename=True
sanatationchar='-'
# cleanup names aaa bbb ccc becomes aaa-bbb-ccc

timeout=10.00
timeouts=True
#restart loop after timeout


def sanatize(s):
     if (sanatizename==True):
          s = re.sub(pattern2, '', s)
          s = re.sub(pattern3, sanatationchar, s)
     return s

def splitter(var1,var4):
    var3, var2=[], []
    try:
        var2 = var1.split ("_",1) #split on first occuring _
        if (len(var2)<2 or (re.search(pattern1, var2[0])is not None)):
            var2.insert (0, "001.03") # if it has no number, assign no number
        var3 = map(int, var2[0].split ("."))
        if all(isinstance(x,int) for x in var3):
            if var4 is True:
                return (var2[0], var3, var2[-1])
            else:
                return (list(var3), var3, var2[-1])
        else:
            if debug==True:
                print ("error, no integers")
    except:
        if debug==True:
            print ("no split possible")
    return()

def changer (currently,tobe):
    for i in range(len(currently)):
        try:
            os.rename(current[i], tobe[i])
            if debug==True:
                print('changed %s into %s'%(current[i], tobe[i]))
        except:
            if debug==True:
                print('%s is not changed, since it is currently in use (or other error,rights etc)'%(current[i]))
    if debug==True:
        print("changer done")
    return()
   


def lecteur(root,basecode,dirlist):
    newname, dnumberlist, oldpath, var2, var3=[], [], [], [], []
    for subdir in dirlist:
        var2,var3,var4=splitter(subdir, False)
        var3.pop() #shed last element
        var5=sanatize(var4) #make nice name without losign original
        if var3==basecode: #if equal to topnumber is equal to root, check for nice name, else continue
            dnumberlist.append(int(var2[-1]))
            if var5 == var4:
                newname.append(var5)
                oldpath.append(os.path.join(root,subdir))               
            else:
                continue
        else:
            newname.append(var5)
            oldpath.append(os.path.join(root,subdir))
    maxd=max(dnumberlist)
    return (maxd,oldpath,newname)
    

def architect (bcode,maxd,newname):
    var2=[]
    for y in range(len(newname)):
        var2.append(os.path.join(dirname,'%s.%s_%s' % (bcode, (maxd+y), sanatize(newname[y]))))
    return(var2)
    
def main(startpath):
    tobe, oldname, newname=[], [], []
    maxd = int
    for dirname, subdirList, filenames in os.walk(startpath):
        if (gitignore==True and ('.git' in dirname)):
            dirname.remove('.git')
            #don't go into git dirs
        if (folders==True):
            if (dirname == startpath or (len(subdirList)==0 and len(filenames)==0)):
                continue
            compbasecode, basecode, var4 = splitter(os.path.basename(dirname), True)
            maxd,oldname,newname=lecteur(dirname,basecode,subdirList)
            tobe=architect(compbasecode,maxd,newname)
            changer(oldname,tobe)
        if (files==True):
            tobe, oldname, newname=[], [], []
            maxd=0
            maxd,oldname,newname=lecteur(dirname,basecode,filenames)
            tobe=architect(compbasecode,maxd,newname)
            changer(oldname,tobe)
            maxd=0
            tobe, oldname, newname=[], [], []
    return()

while timeouts:
     clear()
     main(startpath)
     time.sleep(timeout)
sys.exit()
