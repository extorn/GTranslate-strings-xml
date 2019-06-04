#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This python skript extracts string resources, calls Google translate
# and reassambles a new strings.xml as fitted for Android projects.

# run via "python3.5 gtranslate.py"
# Note: needs module html. To install, run "pip install html" (python package installer)
### Settings 

### LANGUAGE CODES FOR REFERENCE

#   af          Afrikaans
#   ak          Akan
#   sq          Albanian
#   am          Amharic
#   ar          Arabic
#   hy          Armenian
#   az          Azerbaijani
#   eu          Basque
#   be          Belarusian
#   bem         Bemba
#   bn          Bengali
#   bh          Bihari
#   xx-bork     Bork, bork, bork!
#   bs          Bosnian
#   br          Breton
#   bg          Bulgarian
#   km          Cambodian
#   ca          Catalan
#   chr         Cherokee
#   ny          Chichewa
#   zh-CN       Chinese (Simplified)
#   zh-TW       Chinese (Traditional)
#   co          Corsican
#   hr          Croatian
#   cs          Czech
#   da          Danish
#   nl          Dutch
#   xx-elmer    Elmer Fudd
#   en          English
#   eo          Esperanto
#   et          Estonian
#   ee          Ewe
#   fo          Faroese
#   tl          Filipino
#   fi          Finnish
#   fr          French
#   fy          Frisian
#   gaa         Ga
#   gl          Galician
#   ka          Georgian
#   de          German
#   el          Greek
#   gn          Guarani
#   gu          Gujarati
#   xx-hacker   Hacker
#   ht          Haitian Creole
#   ha          Hausa
#   haw         Hawaiian
#   iw          Hebrew
#   hi          Hindi
#   hu          Hungarian
#   is          Icelandic
#   ig          Igbo
#   id          Indonesian
#   ia          Interlingua
#   ga          Irish
#   it          Italian
#   ja          Japanese
#   jw          Javanese
#   kn          Kannada
#   kk          Kazakh
#   rw          Kinyarwanda
#   rn          Kirundi
#   xx-klingon  Klingon
#   kg          Kongo
#   ko          Korean
#   kri         Krio (Sierra Leone)
#   ku          Kurdish
#   ckb         Kurdish (Soranî)
#   ky          Kyrgyz
#   lo          Laothian
#   la          Latin
#   lv          Latvian
#   ln          Lingala
#   lt          Lithuanian
#   loz         Lozi
#   lg          Luganda
#   ach         Luo
#   mk          Macedonian
#   mg          Malagasy
#   ms          Malay
#   ml          Malayalam
#   mt          Maltese
#   mi          Maori
#   mr          Marathi
#   mfe         Mauritian Creole
#   mo          Moldavian
#   mn          Mongolian
#   sr-ME       Montenegrin
#   ne          Nepali
#   pcm         Nigerian Pidgin
#   nso         Northern Sotho
#   no          Norwegian
#   nn          Norwegian (Nynorsk)
#   oc          Occitan
#   or          Oriya
#   om          Oromo
#   ps          Pashto
#   fa          Persian
#   xx-pirate   Pirate
#   pl          Polish
#   pt-BR       Portuguese (Brazil)
#   pt-PT       Portuguese (Portugal)
#   pa          Punjabi
#   qu          Quechua
#   ro          Romanian
#   rm          Romansh
#   nyn         Runyakitara
#   ru          Russian
#   gd          Scots Gaelic
#   sr          Serbian
#   sh          Serbo-Croatian
#   st          Sesotho
#   tn          Setswana
#   crs         Seychellois Creole
#   sn          Shona
#   sd          Sindhi
#   si          Sinhalese
#   sk          Slovak
#   sl          Slovenian
#   so          Somali
#   es          Spanish
#   es-419      Spanish (Latin American)
#   su          Sundanese
#   sw          Swahili
#   sv          Swedish
#   tg          Tajik
#   ta          Tamil
#   tt          Tatar
#   te          Telugu
#   th          Thai
#   ti          Tigrinya
#   to          Tonga
#   lua         Tshiluba
#   tum         Tumbuka
#   tr          Turkish
#   tk          Turkmen
#   tw          Twi
#   ug          Uighur
#   uk          Ukrainian
#   ur          Urdu
#   uz          Uzbek
#   vi          Vietnamese
#   cy          Welsh
#   wo          Wolof
#   xh          Xhosa
#   yi          Yiddish
#   yo          Yoruba
#   zu          Zulu

import html
import requests
#import xml.etree.ElementTree as ET
import lxml.etree as ET
import sys, getopt
import os.path
from io import BytesIO

class Translator():

    def getOutputFilename(self, inFile, toLanguage):
        filenameStem = os.path.splitext(inFile)[0]
        fileExt = os.path.splitext(inFile)[1]
        print(filenameStem)
        print(fileExt)
        outFile = "" + filenameStem + '-' + toLanguage + fileExt
        return outFile



    def translate(self, to_translate, from_language="auto", to_language="auto"):
#     print('translating to ', to_language, ' from ', from_language)
     r = requests.get("http://translate.google.com/m?hl=%s&sl=%s&q=%s"% (to_language, from_language, to_translate.replace(" ", "+")))
     if r.encoding is None or r.encoding == 'ISO-8859-1':
         r.encoding = r.apparent_encoding
#     print('Encoding :',r.encoding)
#     print('processing text ',r.text)
#     text=html.unescape(r.text)    
     before_trans = 'class="t0"'
     after_trans='</div>'
#     print('found at pos ',r.text.find(before_trans))
     parsed1=r.text[r.text.find(before_trans)+len(before_trans):]
     parsed2=parsed1[:parsed1.find(after_trans)]
     parsed3=parsed2[parsed2.find('>')+1:]
     #print('translated text : ',parsed3)
     
     return parsed3

    def translateXmlFile(self, inFile, outFile, fromLanguage, toLanguage):
        tree = ET.parse(inFile)
        root = tree.getroot()
        for i in range(len(root)):
            isTranslatable = root[i].get('translatable')
            if(root[i].tag=='string'):
#                if(isTranslatable=='false'):
#                    print(root[i].text)
#                else:
                if(isTranslatable!='false'):
                    totranslate=root[i].text
                    print((str(i)+" ========================="))
                    print(totranslate)
                    print("-->")
                    if(totranslate!=None):
                        root[i].text=self.translate(totranslate,fromLanguage,toLanguage)
                        print(root[i].text)
            elif(root[i].tag=='string-array'):
#                if(isTranslatable=='false'):
#                    for j in range(len(root[i])):	
#                        print((str(i)+" ========================="))
#                        if(root[i][j].tag=='item'):
#                            print(root[i][j].text)
#                else:
                if(isTranslatable!='false'):
                    for j in range(len(root[i])):	
                        if(root[i][j].tag=='item'):
                            totranslate=root[i][j].text
                            if(totranslate!=None):
                                root[i][j].text=self.translate(totranslate,fromLanguage,toLanguage)
                                print((str(i)+"["+str(j)+"] ========================="))
                                print(totranslate)
                                print(root[i][j].text)
        print('writing to '+outFile)
        tree.write(outFile, xml_declaration=True, encoding='utf-8')


def showUsage():
    print('gtranslate.py -i <inputfile> -o <outputfile> -l <languageCode e.g. "zh-CN>"')

def main(argv):
    inputfile = ''
    translationsFile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:l:",["ifile=","ofile=","lfile="])
    except getopt.GetoptError:
        showUsage()
        sys.exit(2)
    if(len(opts) < 2 | len(opts) > 3):
        showUsage()
        sys.exit(2)

    outputFile = None

    for opt, arg in opts:
        if opt == '-h':
            showUsage()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputFile = arg
        elif opt in ("-o", "--ofile"):
            outputFile = arg
        elif opt in ("-l", "--lfile"):
            outputLanguage = arg

    translator = Translator()
    if(outputFile is None):
        outputFile = translator.getOutputFilename(inputFile, outputLanguage)

    print('Input file is        : ', inputFile)
    print('Output file is       : ', outputFile)

    translator.translateXmlFile(inputFile, outputFile, "auto", outputLanguage)

if __name__ == "__main__":
    main(sys.argv[1:])

