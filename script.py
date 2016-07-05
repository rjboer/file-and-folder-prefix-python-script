import glob 
import os
import sys
import string
import re

#This script is to controll a network directory, coupled to a document managment system
#It renumbers all files (and subdirectories) with a numbered file path in a string e.g.:
#
#100 (or something else) base dir
#100.1 sub dir
#    100.1 file in subdir 1
#100.2 subdir
#100 file in base dir
clear()
startpath = "/home/bi/Desktop/proeftuin"
#teststring1 = re.compile('(\d+(\.| |\_))+')
#teststring2 = re.compile('\/(\w+\/)+(\d+(\.| |\_))+\w+$')
#teststring3 = re.compile('((\d+)(\.| |\_))+')
#teststring4 = re.compile('^(((\d+)\.?)+)+[^a-z]\w+$')
#teststring5 = re.compile('(\d+$)')
#teststring6 = re.compile('(^(\d+\.)+)')
#teststring7 = re.compile('(\d\d+)')
teststr7 = re.compile('([^\d\W])')
dnumberlist = []
#pastl1=[]
#pastl2=[]
#pastl3=[]
#pastl4=[]
#faill1=[]
#faill2=[]
#faill3=[]
#faill4=[]
#faill12=[]
#faill22=[]
#blist=[]
#filenamels=[]
debug=False
files=True
folders=True
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





def printvars(var1,var2):
    print("root dir en subdir respectively")
    print("############################################")
    print var1
    print var2
    print("############################################")

def urify(s):
     # verwijder alle niet letters (alles anders dan nummers en letters)
     s = re.sub(r"[^\w^\.\s]", '', s)
     # verwijder alle whitespaces
     s = re.sub(r"\s+", '_', s)
     # return de nieuwe naam
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
        var5=urify(var4) #make nice name without losign original
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
        var2.append(os.path.join(dirname,'%s.%s_%s' % (bcode, (maxd+y), urify(newname[y]))))
    return(var2)
    
def main(startpath):
    tobe, oldname, newname=[], [], []
    maxd = int
    for dirname, subdirList, filenames in os.walk(startpath):
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
            #changeur(oldname,tobe)
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
#print subdirList
#print dirName
#print fileList

main(startpath)
print("finished, kill")
exit()

#
#def old():
#    i=0
#    for dirname, subdirList, filenames in os.walk(startpath):
#        i+=1 
#        #skip the source directory (do not rename this) 
#        if dirname == startpath:
#            continue
#        var1 = os.path.basename(dirname)
#        print(" condition the pathname")
#        compbasecode, basecode, var4 = mangler(var1, True)
#    #    filenamels.append(var4)
#    #    for base in basecode:
#     #       compbasecode = '%s.%s' % (compbasecode, base)
#        #print (basecode)
#        lensdl = len(subdirList)
#        x=0
#        for subdir in subdirList:
#            var2,var4=mangler(subdir, False)
#            var3=list(var2)
#            var3.pop()
#            var5=urify(var4)
#            if var3==basecode:
#                print ("test last element")
#                dnumberlist.append(int(var2[-1]))
#                if var5 != var4:
#                    faill1.append(subdir)
#                    faill3.append(var5)
#                    faill2.append(os.path.join(dirname,subdir))
#                    faill4.append(x)
#                else:
#                    continue
#            else:
#                faill1.append(subdir)
#                faill3.append(var4)
#                faill2.append(os.path.join(dirname,subdir))
#                faill4.append(x)
#            x+=1
#        maxd=max(dnumberlist)
#        y=0
#        for y in range(len(faill1)):
#            maxd+=1
#            test = '%s.%s_%s' % (compbasecode, maxd, urify(faill3[y]))
#            test2=os.path.join(dirname,test)
#            faill12.append(test)
#            faill22.append(test2)
#        changeur(faill2,faill22)
#    return()
#    printvars(dirname, subdirList)
#        
#    if len(var1) <=3:
#        print("korte pathname")
#        var2 = re.match(teststring7,var1)
#        if var2 is not None:
#            print("alleen nummers, te korte pathname negeren")
#            continue
#    else:
#        print(var1)
#        print(dirname.count(os.sep))
#        print( dirname.count(os.sep) - startlevel)
#        currentlevel.append(dirname.count(os.sep) - startlevel)
#        #regmatch(var1, teststring4)
#        dirnamelist.append(var1)
#        pathlist.append(dirname)
#        
#        #print(os.path.join(dirname, subdirname))
#        # print path to all filenames.
#        #for filename in filenames:
#        #    print(os.path.join(dirname, filename))
#        #   Advanced usage:
#        # editing the 'dirnames' list will stop os.walk() from recursing into there.
#        if '.git' in dirname:
#            # don't go into any .git directories.
#            dirname.remove('.git')
#
#
