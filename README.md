# file-and-folder-prefix-go-script
This script goes trough directories and renames them. 
IT WILL ONLY RENAME DIRECTORIES AND NO OTHER FILES

Works as follows:
```
1_Folder1
    |_____ 1.1_subfolder1
    |_____ 1.2_subfolder2
              |_____ 1.2.1_sub of subfolder2
                          |_____ 1.2.1.1_file1
                           |_____ 1.2.1.2_file2
```
The script reads the config.txt and puts all given paths in an array and then loop trough all the folders in the given path(s).

it looks trough the directories using ioutil.Readir() it checks if the directorie contains an index.txt if it does not exist it will create one (standard value is index = true).

then it will check the content of the index.txt for “index = true” if that is found it will rename the directories if not it will not rename the directories. If “index = false” it will also not rename any deeper directories.
script provided as is, released GPLv3
