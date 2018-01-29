package main

import (
	"io/ioutil"
	"regexp"
	"strings"
	"os"
	"strconv"
	"fmt"
	"bufio"
)

// create and set global variables
// the Path array will contain all the starting paths
var Path = []string{}
// used to keep track of how deep we are
var Index = 0
// here we will temporary store directory names
var Directories = [200][200]string{}
// this is used to keep track of the different regex results
var Regex = []bool{}
// used to check if an index.txt is found
var Indextxt = false
// used to check if Files should be names
var RenameFiles = false
// used to check if the directorie name should be chcked with a regex
var SkipRegex = false

// main function reads a config file, compiles the regexes
// and then goes trough the directories in the paths it got from the config file
func main() {
	inFile, _ := os.Open("config.txt")
	defer inFile.Close()
	scanner := bufio.NewScanner(inFile)
	scanner.Split(bufio.ScanLines)
	for scanner.Scan() {
		Path = append(Path, scanner.Text())
	}
	myRegex1 := `(\\\.\w)`
	myRegex2 := `(\d\.  .)`
	myRegex3 := `(\d\. \w)`
	myRegex4 := `(_gsdata_)`
	re1 := regexp.MustCompile(myRegex1)
	re2 := regexp.MustCompile(myRegex2)
	re3 := regexp.MustCompile(myRegex3)
	re4 := regexp.MustCompile(myRegex4)
	for k, v := range Path {
		getDirectories(v, re1, re2, re3, re4, "", k)
	}
}

// this function recursively loops trough the directories
// and add a prefix the the directories that do not have one
func getDirectories(path string, re1 *regexp.Regexp, re2 *regexp.Regexp, re3 *regexp.Regexp, re4 *regexp.Regexp, prefix string, index int) {
	// empty or set variable to false
	Regex = nil
	rename := false
	Indextxt = false
	if path != "\\" {
		// get all the files in a given directory
		files, _ := ioutil.ReadDir(path)
		// if there is 1 or more files
		if len(files) != 0 {
			// a is the index in which the file while be stored
			// we dont use the key value because we will skip over every thing that is not a directory
			a := 0
			// this variable will tell the script if there are directories in the current directory
			dir := false
			// loop over all the files in the directory
			for _, v := range files {
				// if the file is a directory
				if v.IsDir() {
					// if the path+directory name doe not contain "_gsdata_" or "\." (hidden directory)
					// we add it the the directories array and set dir to true
					if !strings.Contains(path+v.Name(), "_gsdata_") {
						if !strings.Contains(path+v.Name(), "\\.") {
							Directories[Index][a] = v.Name()
							a++
							dir = true
						}
					}
				}
				// if a file called "index.txt" is found tell the script an index.txt exist
				if v.Name() == "index.txt" {
					Indextxt = true
				}
			}
			// if Indextxt is false create an index.txt in the current folder
			if Indextxt == false {
				if dir == true {
					createIndex(path)
				}
			}
			// read the index file
			// this will set RenameFiles to true if the index.txt contains "index = true"
			if dir == true {
				checkIndex(path)
			}
			// return when files should not be renamed
			if RenameFiles == false {
				return
			}
			// if skip regex is false check all files with the regex
			// if it is true dont check the files and rename them
			if SkipRegex == false {
				// loop over all the filles in directories[Index] and check the with the regexes we pre compiled
				for _, v := range Directories[Index] {
					if v != "" {
						regexCheck(v, re1, re2, re3, re4, index)
					}
				}
				// if any of the files need to be renamed rename all files in the current directory and lower directories
				// and set SkipRegex to true so it will rename all files without wasting time on the regex checks
				// if no files in the current directory need to be renamed set rename to false
				for _, v := range Regex {
					if v == true {
						rename = true
						SkipRegex = true
						break
					} else {
						rename = false
					}
				}
			} else {
				rename = true
			}
			// if RenameFiles and rename are true loop over the directories array and rename the files
			if RenameFiles == true {
				if rename == true {
					for k, v := range Directories[Index] {
						// check if v is not empty because we created a [200][200] array which can have a lot of empty indexes
						if v != "" {
							// split the string to get the prefex and directory name seperately
							mystring := strings.Split(v, ".  ")
							// if the name contains a prefix not create by this script
							if strings.Contains(mystring[len(mystring)-1], ". ") {
								// split the name in the existing prefix and file name
								mystring2 := strings.Split(mystring[len(mystring)-1], ". ")
								// check if we got atleast 2 values from strings.split in mystring, 1 or less would mean there is only a prefix and no filename
								if len(mystring) > 1 {
									// if the current path+filename is not the same as path + prefix(prefix+strconv.Itoa(k+1)) + name then rename the file
									if path+v != path+prefix+strconv.Itoa(k+1)+".  "+mystring2[len(mystring2)-1] {
										fmt.Printf("%s --> %s\n", path+v, path+prefix+strconv.Itoa(k+1)+".  "+mystring2[len(mystring2)-1])
										err := os.Rename(path+v, path+prefix+strconv.Itoa(k+1)+".  "+mystring2[len(mystring2)-1])
										Directories[Index][k] = prefix+strconv.Itoa(k+1)+".  "+mystring2[len(mystring2)-1]
										// if there is an error renaming print it but dont stop the script
										if err != nil{
											fmt.Println(err)
										}
									}
								} else {
									// else check if mystring2 has 2 or more values
									if len(mystring2) > 1 {
										if path+v != path+prefix+strconv.Itoa(k+1)+".  "+mystring2[1] {
											// if the current path+filename is not the same as path + prefix(prefix+strconv.Itoa(k+1)) + name then rename the file
											fmt.Printf("%s --> %s\n", path+v, path+prefix+strconv.Itoa(k+1)+".  "+mystring2[1])
											err := os.Rename(path+v, path+prefix+strconv.Itoa(k+1)+".  "+mystring2[1])
											Directories[Index][k] = prefix+strconv.Itoa(k+1)+".  "+mystring2[1]
											// if there is an error renaming print it but dont stop the script
											if err != nil{
												fmt.Println(err)
											}
										}
									}
								}
							} else {
								// if the filename does not contain a prefix that was not generated by this script
								// and the string was split in 2 or more parts
								if len(mystring) > 1 {
									// check if the current path+name is not that same as the new name
									// if it is not the same rename the directory
									if path+v != path+prefix+strconv.Itoa(k+1)+".  "+mystring[1] {
										fmt.Printf("%s --> %s\n", path+v, path+prefix+strconv.Itoa(k+1)+".  "+mystring[1])
										err := os.Rename(path+v, path+prefix+strconv.Itoa(k+1)+".  "+mystring[1])
										Directories[Index][k] = prefix+strconv.Itoa(k+1)+".  "+mystring[1]
										// if there is an error print it but don't stop the script
										if err != nil{
											fmt.Println(err)
										}
									}
								}
							}
						}
					}
					// last is used to compare the current prefix with the prefix of the previously checked directory
					last := ""
					// loop over the directories
					for k, v := range Directories[Index] {
						if v != "" {
							// split the file name to het the prefix and name seperately
							mystring := strings.Split(v, ".  ")
							// if the current prefix is the same as the last prefix change the prefix of the directory
							if mystring[0] == last {
								fmt.Printf("%s <--> %s are equal %s\n", mystring[0], last, v)
								err := os.Rename(path+v, path+prefix+strconv.Itoa(k+1)+".  "+mystring[len(mystring)-1])
								if err != nil {
									fmt.Println(err)
								}
								Directories[Index][k] = prefix + strconv.Itoa(k+1) + ".  " + mystring[len(mystring)-1]
								// put the new prefix into last
								last = prefix + strconv.Itoa(k+1)
							} else {
								// if it is not the same put the current prefix into last
								last = prefix + mystring[0]
							}
						}
					}
				}
			}
			// this part renames directories that do not have a prefix
			if rename == true {
				for k, v := range Directories[Index] {
					if v != "" {
						mystring := strings.Split(v, ".  ")
						if path+v != path+prefix+strconv.Itoa(k+1)+".  "+mystring[len(mystring)-1] {
							err := os.Rename(path+v, path+prefix+strconv.Itoa(k+1)+".  "+mystring[len(mystring)-1])
							if err != nil {
								fmt.Println(err)
							}
							Directories[Index][k] = path + prefix + strconv.Itoa(k+1) + ".  " + mystring[len(mystring)-1]
							SkipRegex = true
						}
					}
				}
			}
			// increase the index because we are going a level deeper into the directories
			Index++
			for k, v := range Directories[Index-1] {
				if v != "" {
					// split the full name because we don't want to pass the prefix in the recursive call
					mystring := strings.Split(v, "  ")
					if rename == true {
						SkipRegex = true
						getDirectories(path+prefix+strconv.Itoa(k+1)+".  "+mystring[len(mystring)-1]+"\\", re1, re2, re3, re4, prefix+strconv.Itoa(k+1)+".", index)
					} else {
						getDirectories(path+v+"\\", re1, re2, re3, re4, mystring[0], index)
					}
				}
			}
			// decrease the index because we are going a level up in the directories
			Index--
			// empty the last used directories array so it can be used again
			for k := range Directories[Index] {
				Directories[Index][k] = ""
			}
			// set SkipRegex back to false
			SkipRegex = false
		}
	}
}

// this function compares the path and filename to the regexps we compiled in the main function.
// if a match is found we return and the next directory will be checked.
// if no match is found we will assume the directory needs to be renamed.
// we put the results in an array because if 1 file needs to renamed the script will rename all files in the current and deeper directories.
// this is because go uses a lexical order when going trough the files.
func regexCheck(path string, re1 *regexp.Regexp, re2 *regexp.Regexp, re3 *regexp.Regexp, re4 *regexp.Regexp, index int) {
	filename := strings.TrimPrefix(path, Path[index])
	for _, match := range re1.FindAllStringSubmatch(path, -1) {
		_ = match
		Regex = append(Regex, false)
		return
	}
	for _, match := range re2.FindAllStringSubmatch(filename, -1) {
		_ = match
		Regex = append(Regex, false)
		return
	}
	for _, match := range re3.FindAllStringSubmatch(filename, -1) {
		fmt.Println(match)
		_ = match
		Regex = append(Regex, true)
		return
	}
	for _, match := range re4.FindAllStringSubmatch(path, -1) {
		_ = match
		Regex = append(Regex, false)
		return
	}
	fmt.Println(filename)
	Regex = append(Regex, true)
}

// this function creates an "index.txt" file which contains index = true so all directories will be renamed
// to prevent this you can manually add a index.txt which contain index = false where you dont want directories to be ranamed
func createIndex(path string) {
	tempfile, err := os.OpenFile(path+"\\index.txt", os.O_RDWR|os.O_CREATE|os.O_RDONLY, os.ModePerm)
	tempfile.WriteString(`index = true

This is the index file of Resato's auto indexer,
change the index in true to let it crawl through your folders and re-number them

e.g. examplefolder -> 250.1.1 example folder`)
	if err != nil {
		fmt.Printf("Error creating or opening index.txt\n Error: %s\n", err)
	}
	defer tempfile.Close()
}

// check if the "index.txt" contains index = true if it does not do not rename the directories
// it was made this way so you can easily add more options to the index.txt
func checkIndex(path string) {
	dat, err := ioutil.ReadFile(path + "index.txt")
	if err != nil {
		fmt.Println(err)
	}
	// if index = true is found set RenameFiles to true so the script will rename the files
	if strings.Contains(string(dat), "index = true") {
		RenameFiles = true
		return
	}
	RenameFiles = false
}
