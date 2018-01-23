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
var Regex = []bool{}
var Indextxt = false
var RenameFiles = false
var SkipRegex = false

func main() {
	inFile, _ := os.Open("config.txt")
	defer inFile.Close()
	scanner := bufio.NewScanner(inFile)
	scanner.Split(bufio.ScanLines)

	for scanner.Scan() {
		Path = append(Path,scanner.Text())
	}
	myRegex1 := `(\\\.\w)`
	myRegex2 := `(\d\.  .)`
	myRegex3 := `(\d\. \w)`
	myRegex4 := `(_gsdata_)`
	re1 := regexp.MustCompile(myRegex1)
	re2 := regexp.MustCompile(myRegex2)
	re3 := regexp.MustCompile(myRegex3)
	re4 := regexp.MustCompile(myRegex4)
	for k, v := range Path{
		getDirectories(v, re1, re2, re3, re4, "", k)
	}
}

func getDirectories(path string, re1 *regexp.Regexp, re2 *regexp.Regexp, re3 *regexp.Regexp, re4 *regexp.Regexp, prefix string, index int) {
	Regex = nil
	rename := true
	Indextxt = false
	if path != "\\" {
		files, _ := ioutil.ReadDir(path)
		if len(files) != 0 {
			a := 0
			dir := false
			for _, v := range files {
				if v.IsDir() {
					if !strings.Contains(path+v.Name(), "_gsdata_") {
						if !strings.Contains(path+v.Name(), "\\.") {
							Directories[Index][a] = v.Name()
							a++
							dir = true
						}
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
			if SkipRegex == false {
				for _, v := range Directories[Index] {
					if v != "" {
						regexCheck(v, re1, re2, re3, re4, index)
					}
				}
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
			if rename == true {
				for k, v := range Directories[Index] {
					if v != "" {
						mystring := strings.Split(v, ".  ")
						if path+v != path+prefix+strconv.Itoa(k+1)+".  "+mystring[len(mystring)-1] {
							err := os.Rename(path+v, path+prefix+strconv.Itoa(k+1)+".  "+mystring[len(mystring)-1])
							if err != nil {
								fmt.Println(err)
							} else {
								fmt.Printf("Renamed %s --> %s\n", path+v, path+prefix+strconv.Itoa(k+1)+".  "+mystring[len(mystring)-1])
							}
							Directories[Index][k] = path + prefix + strconv.Itoa(k+1) + ".  " + mystring[len(mystring)-1]
							SkipRegex = true
						}
					}
				}
			}
			Index++
			for k, v := range Directories[Index-1] {
				if v != "" {
					mystring := strings.Split(v, "  ")
					if rename == true {
						SkipRegex = true
						getDirectories(path+prefix+strconv.Itoa(k+1)+".  "+mystring[len(mystring)-1]+"\\", re1, re2, re3, re4, prefix+strconv.Itoa(k+1)+".", index)
					} else {
						getDirectories(path+v+"\\", re1, re2, re3, re4, mystring[0], index)
					}
				}
			}
			Index--
			for k := range Directories[Index] {
				Directories[Index][k] = ""
			}
			SkipRegex = false
		}
	}
}

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
	for _, match := range re3.FindAllString(filename, -1) {
		_ = match
		Regex = append(Regex, true)
		return
	}
	for _, match := range re4.FindAllStringSubmatch(path, -1) {
		_ = match
		Regex = append(Regex, false)
		return
	}
	Regex = append(Regex, true)
}

func createIndex(path string) {
	tempfile, err := os.OpenFile(path+"\\index.txt", os.O_RDWR|os.O_CREATE|os.O_RDONLY, os.ModePerm)
	tempfile.WriteString("index = true")
	if err != nil {
		fmt.Printf("Error creating or opening index.txt\n Error: %s\n", err)
	}
	tempfile.Close()
}

func checkIndex(path string) {
	dat, err := ioutil.ReadFile(path + "index.txt")
	if err != nil {
		fmt.Println(err)
	}
	if strings.Contains(string(dat), "false") {
		RenameFiles = false
		return
	}
	RenameFiles = true
}
