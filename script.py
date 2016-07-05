import os
import sys
import string
import re

clear()
startpath = "/home/bi/Desktop/test"
#teststring1 = re.compile('(\d+(\.| |\_))+')
#teststring2 = re.compile('\/(\w+\/)+(\d+(\.| |\_))+\w+$')
#teststring3 = re.compile('((\d+)(\.| |\_))+')
#teststring4 = re.compile('^(((\d+)\.?)+)+[^a-z]\w+$')
#teststring5 = re.compile('(\d+$)')
#teststring6 = re.compile('(^(\d+\.)+)')
#teststring7 = re.compile('(\d\d+)')
teststr7 = re.compile('([^\d\W])')
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

#
#def rename(dir, pattern, titlePattern):
#    for pathAndFilename in glob.iglob(os.path.join(dir, pattern)):
#        title, ext = os.path.splitext(os.path.basename(pathAndFilename))
#        os.rename(pathAndFilename, 
#                  os.path.join(dir, titlePattern % title + ext))
#
#for root,dirname,filenames in os.walk(path):   
#     for filename in filenames:
#        i = filename.split(".")

#filelist = [ f for f in os.listdir(startpath)]
#print filelist





def sanatize(s):
     # remove all non-chars
     if (sanatizename==True):
          s = re.sub(r"[^\w^\.\s]", '', s)
          # remove all whitespace
          s = re.sub(r"\s+", sanatationchar, s)
          # return new name
     return s

def mangler(var1,var4):
    var3, var2=[], []
    try:
        var2 = var1.split ("_",1)
        if (len(var2)<2 and (re.search(teststr7, var2[0])is not None)):
            var2.insert (0, "001.03")
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
    return

def changeur (currently,tobe):
    for i in range(len(currently)):
        try:
            os.rename(current[i], tobe[i])
            if debug==True:
                print('changed %s into %s'%(current[i], tobe[i]))
        except:
            if debug==True:
                print('%s is not changed, since it is currently in use (or other error,rights etc)'%(current[i]))
    if debug==True:
        print("changeur done")
    return()
   


def lecteur(root,basecode,dirlist):
    newname, dnumberlist, oldpath, var2, var3=[], [], [], [], []
    for subdir in dirlist:
        var2,var3,var4=mangler(subdir, False)
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
    

def architecte (bcode,maxd,newname):
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
            compbasecode, basecode, var4 = mangler(os.path.basename(dirname), True)
            maxd,oldname,newname=lecteur(dirname,basecode,subdirList)
            tobe=architecte(compbasecode,maxd,newname)
            changeur(oldname,tobe)
        if (files==True):
            tobe, oldname, newname=[], [], []
            maxd=0
            maxd,oldname,newname=lecteur(dirname,basecode,filenames)
            tobe=architecte(compbasecode,maxd,newname)
            changeur(oldname,tobe)
            maxd=0
            tobe, oldname, newname=[], [], []
    return()



startlevel = startpath.count(os.sep)
def regmatch (dirname,pattern):
    matchg = re.match(pattern, dirname)
    if matchg is not None:
        #print( "numbered dir detected") 
        matchg1 = matchg.groups(1)
        #print(matchg1[1])
        matchg2 = re.match(teststring5, matchg1[1])
        number.append(matchg2[0])
    return()


def test3er():
    for dirName, subdirList, fileList in os.walk(startpath):
        print('Found directory: %s' % dirName)
        for fname in fileList:
            print('\t%s' % fname)
    return()

main(startpath)
print("finished")
sys.exit()
