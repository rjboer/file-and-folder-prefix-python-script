# file-and-folder-prefix-python-script
This script uses os walk to identify files and folders, after which it ads a prefix (if it is not there already) in the form of (parentfoldernumber).x_foldername &lt;-where x depends on the highest numbered folder

Works as follows:
```
1_Folder1
    |_____ 1.1_subfolder1
    |_____ 1.2_subfolder2
              |_____ 1.2.1_sub of subfolder2
                          |_____ 1.2.1.1_file1
                           |_____ 1.2.1.2_file2
```
The os.walk method in python looks through folder 1;
finds an unnumbered subfolder, looks at the highest numbered subfolder (that comes up in os.walk) and renames the unnumbered subfolder in the parent folder number and the 

The same goes with files, files at the bottom of a subfolder get a new number...
1 glitch ( if files are placed in a higher directory the numbering restarts)
like this:
```
1_Folder1
    |_____ 1.1_subfolder1
    |_____ 1.2_subfolder2
    |_____ 1.1_file1
    |_____ 1.2_file2
              |_____ 1.2.1_sub of subfolder2
```
(we dont need it, al our files are in the lowest hirarchy level)

script provided as is
