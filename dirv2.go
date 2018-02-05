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

var Path = []string{}
var Index = 0
var Directories = [200][200]string{}
var Indextxt = false
var RenameFiles = false

func main() {
	inFile, _ := os.Open("config.txt")
	defer inFile.Close()
	scanner := bufio.NewScanner(inFile)
	scanner.Split(bufio.ScanLines)
	for scanner.Scan() {
		Path = append(Path, scanner.Text())
	}
	myRegex1 := `(\\\..)`
	myRegex2 := `(\d\.  .)`
	myRegex3 := `(\d\. \w)`
	myRegex4 := `(_gsdata_)`
	re1 := regexp.MustCompile(myRegex1)
	re2 := regexp.MustCompile(myRegex2)
	re3 := regexp.MustCompile(myRegex3)
	re4 := regexp.MustCompile(myRegex4)
	for k, v := range Path {
		getDirectories(v, re1, re2, re3, re4, "", k, "")
	}
}

func getDirectories(path string, re1 *regexp.Regexp, re2 *regexp.Regexp, re3 *regexp.Regexp, re4 *regexp.Regexp, prefix string, index int, prevPrefix string) {
	rename := false
	Indextxt = false
	if path != "\\" {
		files, _ := ioutil.ReadDir(path)
		if len(files) > 0 {
			a := 0
			dir := false
			for _, v := range files {
				if v.IsDir() {
					regex1 := re1.FindStringSubmatch(path + v.Name())
					Regex2 := re4.FindStringSubmatch(path + v.Name())
					if len(regex1) == 0 && len(Regex2) == 0 {
						Directories[Index][a] = v.Name()
						a++
						dir = true
					}
				}
				if v.Name() == "index.txt" {
					Indextxt = true
				}
			}
			if Indextxt == false {
				if dir == true {
					createIndex(path)
				}
			}
			if dir == true {
				checkIndex(path)
			}
			if RenameFiles == false {
				return
			}
			for k, v := range Directories[Index] {
				if !strings.Contains(v, prevPrefix) {
					if strings.Contains(v, ".  ") {
						tstring := strings.Split(v, ".  ")
						os.Rename(path+v, path+tstring[len(tstring)-1])
						Directories[Index][k] = tstring[len(tstring)-1]
					}
				}
			}
			if RenameFiles == true {
				for k, v := range Directories[Index] {
					if v != "" {
						rename = regexCheck(path, v, re1, re2, re3, re4)
						if rename == true {
							tstring := strings.Split(v, ". ")
							if len(tstring) > 1 {
								err := os.Rename(path+v, path+tstring[len(tstring)-1])
								if err != nil {
									fmt.Println(err)
								}
								Directories[Index][k] = tstring[len(tstring)-1]
							}
							if len(tstring) == 1 {
								err := os.Rename(path+v, path+prefix+strconv.Itoa(k+1)+".  "+v)
								if err != nil {
									fmt.Println(err)
								}
								Directories[Index][k] = prefix + strconv.Itoa(k+1) + ".  " + v
							}
						}
					}
				}
				last := ""
				for k, v := range Directories[Index] {
					if v != "" {
						mystring := strings.Split(v, ".  ")
						if mystring[0] == last {
							tlast, _ := strconv.Atoi(last)
							for mystring[0] == last {
								tlast++
								err := os.Rename(path+v, path+prefix+strconv.Itoa(tlast)+".  "+mystring[len(mystring)-1])
								if err != nil {
									fmt.Println(err)
								}
								Directories[Index][k] = prefix + strconv.Itoa(tlast) + ".  " + mystring[len(mystring)-1]
								last = prefix + strconv.Itoa(tlast)
							}
						} else {
							last = mystring[0]
						}
					}
				}
			}
			for k, v := range Directories[Index] {
				if v != "" {
					rename = regexCheck(path, v, re1, re2, re3, re4)
					if rename == true {
						mystring := strings.Split(v, ".  ")
						if path+v != path+prefix+strconv.Itoa(k+1)+".  "+mystring[len(mystring)-1] {
							err := os.Rename(path+v, path+prefix+strconv.Itoa(k+1)+".  "+mystring[len(mystring)-1])
							if err != nil {
								fmt.Println(err)
							}
							Directories[Index][k] = path + prefix + strconv.Itoa(k+1) + ".  " + mystring[len(mystring)-1]
						}
					}
				}
			}
			Index++
			for k, v := range Directories[Index-1] {
				if v != "" {
					mystring := strings.Split(v, "  ")
					if rename == true {
						getDirectories(path+prefix+strconv.Itoa(k+1)+".  "+mystring[len(mystring)-1]+"\\", re1, re2, re3, re4, prefix+strconv.Itoa(k+1)+".", index, mystring[0])
					} else {
						getDirectories(path+v+"\\", re1, re2, re3, re4, mystring[0], index, mystring[0])
					}
				}
			}
			Index--
			for k := range Directories[Index] {
				Directories[Index][k] = ""
			}
		}
	}
}

func regexCheck(path string, name string, re1 *regexp.Regexp, re2 *regexp.Regexp, re3 *regexp.Regexp, re4 *regexp.Regexp) bool {
	for _, match := range re1.FindAllStringSubmatch(path+name, -1) {
		_ = match
		return false
	}
	for _, match := range re2.FindAllStringSubmatch(name, -1) {
		_ = match
		return false
	}
	for _, match := range re3.FindAllStringSubmatch(name, -1) {
		_ = match
		return true
	}
	for _, match := range re4.FindAllStringSubmatch(path+name, -1) {
		_ = match
		return false
	}
	return true
}

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

func checkIndex(path string) {
	dat, err := ioutil.ReadFile(path + "index.txt")
	if err != nil {
		fmt.Println(err)
	}
	if strings.Contains(string(dat), "index = true") {
		RenameFiles = true
		return
	}
	RenameFiles = false
}
