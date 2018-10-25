#!/usr/bin/env python
# -*- coding: utf-8 -*-
import lxml.etree as ET
#import xml.etree.ElementTree as ET
import re, sys, getopt




# http://stackoverflow.com/questions/33573807/faithfully-preserve-comments-in-parsed-xml-python-2-7
# class CommentedTreeBuilder(ET.TreeBuilder):
#     def __init__(self, *args, **kwargs):
#         super(CommentedTreeBuilder, self).__init__(*args, **kwargs)
#
#     def comment(self, data):
#         self.start(ET.Comment, {})
#         self.data(data)
#         self.end(ET.Comment)

class RawTranslationsTextParser():
    xmlTree = ''
    currentTranslation = 0;
    currentIdx = 0
    newTranslationStartPattern=re.compile('^([\d]*):(.*)')
    # use to escape all instances of ' found in the translation text any other characters that need prefixing with '\' should just be added inside the 2nd square brackets
    characterEscapingPattern=re.compile('([^\\\\])([\'])')

    def translateXmlFile(self, templateXmlFileName, translationsFilename, xmlOutputFilename):
        xmlTemplateRoot = self.loadBaseXmlFile(templateXmlFileName)
        translations = self.loadTranslations(translationsFilename)
        self.mergeTranslations(xmlTemplateRoot, translations)
        self.writeXmlToFile(xmlTemplateRoot, xmlOutputFilename)

    def writeXmlToFile(self, xmlTemplateRoot, xmlOutputFilename):
        xmlTemplateRoot.write(xmlOutputFilename, encoding='utf-8')

    def loadTranslations(self, translationsFilename):
        file = open(translationsFilename,'r')
        translations=file.readlines();
        file.close()
        return translations

    def loadBaseXmlFile(self, xmlTemplateFilename):
        # cparser = ET.XMLParser(target = CommentedTreeBuilder())

        # def read_xml_file(f):
            # return ET.parse(f, parser=cparser)

        # prepare things
        #tree = ET.parse(XMLINFILE)
        # xmlTree = read_xml_file(xmlTemplateFilename)
        xmlTree = ET.parse(xmlTemplateFilename)
        return xmlTree

    def mergeTranslations(self, xmlFileRoot, translations):
        xmlRoot = xmlFileRoot.getroot()
        translationLines=len(translations)-1
        for i in range(len(xmlRoot)):
            isTranslatable=xmlRoot[i].get('translatable')
            if(xmlRoot[i].tag=='string') & (isTranslatable!='false'):
                value = self.getNextTranslation(translations)
                xmlRoot[i].text=value.rstrip()
            else:
                if(xmlRoot[i].tag=='string-array') & (isTranslatable!='false'):
                    for j in range(len(xmlRoot[i])):
                        if(xmlRoot[i][j].tag=='item'):
                            value = self.getNextTranslation(translations)
                            xmlRoot[i][j].text=value.rstrip()

    def hasMoreTranslations(self, translations):
        return self.currentTranslation < len(translations)

    def getNextTranslation(self, translations):
        print('Looking for translation number ',(self.currentTranslation + 1))
        currentLine = translations[self.currentIdx]
        multiLine = False
        match = self.newTranslationStartPattern.match(currentLine)
        if(match is not None):
            newTranslationId = int(match.group(1))
            if(self.currentTranslation + 1 != newTranslationId):
                # This catches a bug in this code where if a translation matches our pattern we have a problem because it gets out of sync!
                raise ValueError('The current translation id (',newTranslationId,') does not match that expected (',(self.currentTranslation+1),')')
            self.currentTranslation += 1
            self.currentIdx += 1
            thisTranslation = match.group(2)
            #print('translation start: ', self.currentTranslation)

            if(self.currentIdx < len(translations)):
                # Now loop until this translation is ended
                currentLine = translations[self.currentIdx]
                match = self.newTranslationStartPattern.match(currentLine)
                while((match is None) & (self.currentIdx < len(translations))):
                    self.currentIdx += 1
                    if(not multiLine):
                        thisTranslation += '\n'
                    thisTranslation += currentLine
                    multiLine = True
                    if(self.currentIdx < len(translations)):
                        currentLine = translations[self.currentIdx]
                        match = self.newTranslationStartPattern.match(currentLine)
                        #print('translation continues: ')
                        # There is a potential bug here if the line of the translation starts matching the pattern.... it'll be caught on the next translation parse execution though.
        else:
            raise SyntaxError('Expected a new translation, but didn\'t match pattern')

        # fix incorrect addition of fullstop by translation service.
        thisTranslation.replace('".','"')
        thisTranslation = self.characterEscapingPattern.sub('\\1\\\\\\2', thisTranslation)
        print('translation number ',self.currentTranslation,' is ', thisTranslation)
        return thisTranslation

#------------------------------------------------------------------------------

def showUsage():
    print('dtranslate_text_to_xml.py -i <inputfile> -t <translations> -o <outputfile>')

def main(argv):
    inputfile = ''
    translationsFile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:t:o:",["ifile=","tfile=","ofile="])
    except getopt.GetoptError:
        showUsage()
        sys.exit(2)
    if(len(opts) != 3):
        showUsage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            showUsage()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-t", "--tfile"):
            translationsFile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    print('Input file is        : ', inputfile)
    print('Translations file is : ', translationsFile)
    print('Output file is       : ', outputfile)
    rawTranslationsTextParser = RawTranslationsTextParser()
    rawTranslationsTextParser.translateXmlFile(inputfile, translationsFile, outputfile)

if __name__ == "__main__":
    main(sys.argv[1:])
