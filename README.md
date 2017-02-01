# frequencyList
Generate a frequency list of SOP nodes used in your houdini files

This script is designed to traverse all folders within a given directory looking for hip files (should cover apprentice and indie).  Once it has a list of files it opens each one and counts the instances of every SOP node. The created list is written to a csv file so you can see which are the most commonly used SOP nodes.

## INSTALL
You can run this file from anywhere but I'd suggest copying it to your root project folder. That could be something like:
```
/Users/mike/Documents/projects
OR
C:\Users\mike\Documents\projects.
```
## USAGE
This script requires hython - the houdini instance of python.

1. Open Houdini's command line tool
### Windows
	Choose start > All Programs > Side Effects Software > Houdini X.X.XXX > Command Line Tools

### Mac
	Open /Applications/Houdini X.X.XXX/Utilities and double-click Houdini Terminal.
	
### Linux
	cd to the Houdini install directory and type source houdini_setup or source houdini_setup.bash depending on your shell.

2. Navigate to the directory containing createFrequencyList.py
		cd /Users/mike/Documents/projects

3. Run the hython script with 2 arguments - name of csv file and folder to traverse.
	hython createFrequencyList.py nodeList.csv /Users/mike/Documents/projects

4. 2 files are created. The node frequency list and a list of hip files that have been processed. I found that hython would sometimes crash or I would want to run the script on multiple locations. The processed files list makes sure you're not doubling up counting the same file and allows you to run the script again if something crashes.

## TODO:
* Add logic to deal with versioning of files. Currently the script will count each version of a hip file as a separate file which would skew the data.

## NOTES:
* The script ignores the backup folder so don't worry about it counting those towards the total
* If you run this script at work and you have a special houdini environment setup you might get errors with custom otl's, etc.
