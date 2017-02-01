import sys
import csv
import os
import pprint
from collections import OrderedDict
from operator import itemgetter

class FileInspector:
    ''' The FileInspector class is designed to traverse through a directory
        structure, find all houdini files and create a csv with an ordered list
        of SOP nodes based on their usage frequency
    '''

    def __init__(self, frequencyFile, pathToTraverse):
        self.frequencyFile = frequencyFile
        self.pathToTraverse = pathToTraverse
        self.allFiles = []
        self.fileErrorList = []
        self.nodeList = {}
        self.processedFilesList = "%s_processedFiles.txt" % self.frequencyFile.split(".")[0]

    def readCsv(self, frequencyFile):
        ''' This function will read an existing csv file expecting the first 
            column to list the node type and the second column to hold a value
            for how often that node has occured.  All other columsn are ignored.
        '''
        rowItems = {}
        if os.path.isfile(frequencyFile):
            with open(frequencyFile, 'rb') as csvfile:
                csvreader = csv.reader(csvfile, delimiter = ',')
                for row in csvreader:
                    if 'NodeType' not in row and 'Total' not in row:
                        rowItems[row[0]] = int(row[1])
            return rowItems
        else:
            return rowItems

    def writeCsv(self, frequencyFile, nodeList):
        ''' This function will take a dictionary of node types and the number of
            instances and write it to an existing csv file.  It will also calculate
            the usage as a percentage of the total count of node instances as well
            as the total percentage for all previous entries in the ordered list
        '''
        sumTotal = sum(nodeList.values())
        orderedNodeList = sorted(nodeList.items(), key=lambda x:x[1], reverse=True)

        with open(frequencyFile, 'wb') as f:
            w = csv.writer(f)
            w.writerow(['NodeType', 'Count', 'Percentage', 'Total Percentage'])
            previousPercentage = 0.0
            
            for item in orderedNodeList:
                key = item[0]
                value = item[1]
                percentage = (value / float(sumTotal)) * 100
                percentageTotal = percentage + previousPercentage
                w.writerow([key, value, "%.3f" % percentage, "%.3f" % percentageTotal])
                previousPercentage = percentageTotal
            w.writerow(['Total', '%s' % sum(nodeList.values())])

    def readProcessedFilesList(self):
        if os.path.isfile(self.processedFilesList):
            with open(self.processedFilesList) as f:
                processedFiles = f.readlines()
                processedFiles = [x.strip() for x in processedFiles]
            return processedFiles
        else:
            return None

    def writeToProcessedFilesList(self, processedFile):
        with open(self.processedFilesList, 'a') as f:
            f.write("%s\n" % processedFile)


    def inspectFiles(self):
        ''' Given a directory to traverse this function will find all houdini
            files and parse them.  For each file a dictionary of nodetypes and
            instance count will be created which is then written to a csv file.
        '''
        for dirpath,_,filenames in os.walk(self.pathToTraverse):
            for f in filenames:
                if "backup" not in dirpath:
                    if "hip" in f.split(".")[-1]:
                        self.allFiles.append(os.path.abspath(os.path.join(dirpath, f)))

        alreadyProcessed = self.readProcessedFilesList()
        print "Already processed..."
        pprint.pprint(alreadyProcessed)

        if alreadyProcessed is not None:
            listOfFilesToProcess = [x for x in self.allFiles if x not in alreadyProcessed]
        else:
            listOfFilesToProcess = self.allFiles

        if len(listOfFilesToProcess)>0:
            print "Files to process..." 
            pprint.pprint(listOfFilesToProcess)
        else:
            print "These files have already been processed"

        for file in listOfFilesToProcess:
            print "Processing: %s" % file
            nodeList = self.readCsv(self.frequencyFile)
            try:
                hou.hipFile.load(file, ignore_load_warnings=True)

                obj = hou.node('/obj')
                allNodes = obj.allSubChildren()
                for node in allNodes:
                    if node.type().category() == hou.sopNodeTypeCategory():
                        nodeType = node.type().description()
                        if nodeType in nodeList:
                            nodeList[nodeType] = nodeList[nodeType] + 1
                        else:
                            nodeList[nodeType] = 1

            except:
                self.fileErrorList.append(file)

            self.writeCsv(self.frequencyFile, nodeList)
            hou.hipFile.clear()
            self.writeToProcessedFilesList(file)


def main():
    frequencyFile = sys.argv[1]
    pathToTraverse = sys.argv[2]
    fileInspector = FileInspector(frequencyFile, pathToTraverse)
    fileInspector.inspectFiles()
    if len(fileInspector.fileErrorList)>0:
        print "Files that errored out...    "
        pprint.pprint(fileInspector.fileErrorList)

main()

