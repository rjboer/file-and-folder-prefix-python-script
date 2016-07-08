import os
import sys
import string
import re
import time

#Rip of the other script....dirty code..., meant for one time run
#
#

startpath = r'C:\Users\roelofjanboer\Documents\DMS2'

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
sanatationchar='_' # cleanup names aaa bbb ccc becomes aaa-bbb-ccc
timeout=10.00
timeouts=True #restart loop after timeout
Overwrite=False # in the case of a double number the latter in order gets relocated
diffnumb=True # count folders,then files, files have own numbering system:
#diffn=False        True
#1.1 folder1 vs     1.1
#1.2 folder2        1.2
#1.1 file1          1.3
#1.2 file2          1.4



def sanatize(s):
    print(s)
    if (sanatizename==True):
        s = re.sub(pattern2, '', s)
        s = re.sub(pattern3, sanatationchar, s)
        print(s)
    return s


def changer (current,tobe):
    for i in range(len(current)):
        try:
            os.rename(current[i], tobe[i])
            if debug:
                print('changed %s into %s'%(current[i], tobe[i]))
        except:
            if debug:
                print('%s is not changed, since it is currently in use (or other error,rights etc)'%(current[i]))
    if debug:
        print("changer done")
    return()
   


def lecteur(root,dirlist):
    newname, oldpath, var2, var3=[], [], [], []
    # if lists are large, this will become slow, hence both list and set, http://stackoverflow.com/questions/14667578/check-if-a-number-already-exist-in-a-list-in-python
    for subdir in dirlist:
        var5=sanatize(subdir) #make nice name without losign original
        if not(var5==subdir):
            newname.append(var5)
            oldpath.append(os.path.join(root,subdir))               
    return (oldpath,newname)
    

def architect (dirname,newname):
    var2=[]
    for y in range(len(newname)):
        var2.append(os.path.join(dirname, newname[y]))
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
        if (folders|(files*diffnumb)):
            checklist = subdirList * folders + filenames * files * diffnumb
            oldname,newname=lecteur(dirname,checklist)
            tobe=architect(dirname,newname)
            changer(oldname,tobe)
            tobe, oldname, newname=[], [], []
    return()



while timeouts:
     clear()
     main(startpath)
     time.sleep(timeout)
sys.exit()
