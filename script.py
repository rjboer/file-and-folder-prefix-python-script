import os
import sys
import string
import re
import time

startpath = "/home/bi/Desktop/test"

pattern1 = re.compile(r"[^\d\W]")# compiled regex string
pattern2 = re.compile(r"[^\w^\.^\-\s]")
pattern3 = re.compile(r"\s+")
dnumberlist = []#cannot remember why I added this...


debug=False # print debug messages
files=True #number files
folders=True  #number folders
gitignore=True # ignore .git files
searchstr='.git'# or other directories....
sanatizename=True #cleanup filenames
sanatationchar='-' # cleanup names aaa bbb ccc becomes aaa-bbb-ccc
timeout=10.00
timeouts=True #restart loop after timeout
Overwrite=False # in the case of a double number the latter in order gets relocated
diffnumb=True # count folders,then files, files have own numbering system:
#diffn=False        True
#1.1 folder1 vs     1.1
#1.2 folder2        1.2
#1.1 file1          1.3
#1.2 file2          1.4

clear = lambda: os.system('cls')

def sanatize(s):
    print(s)
    if (sanatizename==True):
        s = re.sub(pattern2, '', s)
        s = re.sub(pattern3, sanatationchar, s)
        print(s)
    return s

def splitter(var1,var4):
    var3, var2=[], []
    try:
        var2 = var1.split ("_",1) #split on first occuring _
        if (len(var2)<2 or (re.search(pattern1, var2[0])is not None)):
            var2.insert (0, "001.03") # if it has no number, assign new number
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

def changer (current,tobe):
    for i in range(len(current)):
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
    newname, dnumberlist, oldpath, var2, var3=[], [0], [], [], []
    # if lists are large, this will become slow, hence both list and set, http://stackoverflow.com/questions/14667578/check-if-a-number-already-exist-in-a-list-in-python
    for subdir in dirlist:
        var2,var3,var4=splitter(subdir, False)
        var3.pop() #shed last element
        var5=sanatize(var4) #make nice name without losign original
        if (var3==basecode and (var2[1] not in dnumberlist)*(not Overwrite)): #if equal to topnumber is equal to root, check for nice name, else continue
            dnumberlist.append(int(var2[-1]))
            if var5 != var4:
                newname.append(var5)
                oldpath.append(os.path.join(root,subdir))               
            else:
                continue
        else:
            newname.append(var5)
            oldpath.append(os.path.join(root,subdir))
    maxd=max(dnumberlist)
    return (maxd,oldpath,newname)
    

def architect (dirname,bcode,maxd,newname):
    var2=[]
    for y in range(len(newname)):
        var2.append(os.path.join(dirname,'%s.%s_%s' % (bcode, (maxd+1+y), newname[y])))
    return(var2)
    

def main(startpath):
    tobe, oldname, newname, checklist =[], [], [], []
    maxd = int
    for dirname, subdirList, filenames in os.walk(startpath):
        if (dirname == startpath or (len(subdirList)==0 and len(filenames)==0)):
            continue
        if (gitignore==True and ((searchstr in subdirList) or (searchstr in dirname))):
            #subdirList.remove('.git')
            continue
            #don't go into git dirs
        maxd =0
        if (folders|(files*diffnumb)):
            compbasecode, basecode, var4 = splitter(os.path.basename(dirname), True)
            checklist = subdirList * folders + filenames * files * diffnumb
            maxd,oldname,newname=lecteur(dirname,basecode,checklist)
            tobe=architect(dirname,compbasecode,maxd,newname)
            changer(oldname,tobe)
            tobe, oldname, newname=[], [], []
            maxd=(maxd * diffnumb)
        if (files * (not diffnumb)):
            maxd,oldname,newname=lecteur(dirname,basecode,filenames)
            tobe=architect(dirname,compbasecode,maxd,newname)
            changer(oldname,tobe)
            tobe, oldname, newname=[], [], []
    return()



while timeouts:
     clear
     main(startpath)
     time.sleep(timeout)
sys.exit()
