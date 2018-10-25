#!/usr/bin/env python
# -*- coding: utf-8 -*-

import lxml.etree as ET
import sys, getopt

def extractTextFromFile(inputXmlFilename, outputTextFilename):
    tree = ET.parse(inputXmlFilename)
    root = tree.getroot()
    file = open(outputTextFilename,'w')

    counter=0

    for i in range(len(root)):
        isTranslatable = root[i].get('translatable')
        if(root[i].tag=='string') & (isTranslatable!='false'):
            counter=counter+1
            file.write(str(counter)+':'+root[i].text+'\n')
        if(root[i].tag=='string-array') & (isTranslatable!='false'):
            for j in range(len(root[i])):
                if(root[i][j].tag=='item'):
                    counter=counter+1
                    file.write(str(counter)+':'+root[i][j].text+'\n')
    file.close()
    print('Text extracted to ', outputTextFilename)



#------------------------------------------------------------------------------

def showUsage():
    print('dtranslate_xml_to_text.py -i <inputfile> -o <outputfile>')

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        showUsage()
        sys.exit(2)
    if(len(opts) != 2):
        showUsage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            showUsage()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    print('Input file is        : ', inputfile)
    print('Output file is       : ', outputfile)
    extractTextFromFile(inputfile, outputfile)

if __name__ == "__main__":
    main(sys.argv[1:])
