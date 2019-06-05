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

import os.path

import getopt
import lxml.etree as ET
import requests
import sys


class Translator():

    def get_output_filename(self, inFile, to_language):
        filename_stem = os.path.splitext(inFile)[0]
        file_ext = os.path.splitext(inFile)[1]
        print(filename_stem)
        print(file_ext)
        out_file = "" + filename_stem + '-' + to_language + file_ext
        return out_file

    def translate(self, to_translate, from_language="auto", to_language="auto"):
        text = to_translate.replace(" ", "+")
        r = requests.get(
            "http://translate.google.com/m?hl=%s&sl=%s&q=%s" % (to_language, from_language, text))
        if r.encoding is None or r.encoding == 'ISO-8859-1':
            r.encoding = r.apparent_encoding
        before_trans = 'class="t0"'
        after_trans = '</div>'
        parsed1 = r.text[r.text.find(before_trans) + len(before_trans):]
        parsed2 = parsed1[:parsed1.find(after_trans)]
        parsed3 = parsed2[parsed2.find('>') + 1:]
        return parsed3


    def translate_xml_file(self, inFile, out_file, fromLanguage, toLanguage):
        tree = ET.parse(inFile)
        root = tree.getroot()
        for i in range(len(root)):
            is_translatable = root[i].get('translatable')
            if root[i].tag == 'string':
                if is_translatable != 'false':
                    totranslate = root[i].text
                    print((str(i) + " ========================="))
                    print(totranslate)
                    print("-->")
                    if (totranslate != None):
                        root[i].text = self.translate(totranslate, fromLanguage, toLanguage)
                        print(root[i].text)
            elif root[i].tag == 'string-array':
                if is_translatable != 'false':
                    for j in range(len(root[i])):
                        if root[i][j].tag == 'item':
                            totranslate = root[i][j].text
                            if totranslate != None:
                                root[i][j].text = self.translate(totranslate, fromLanguage, toLanguage)
                                print((str(i) + "[" + str(j) + "] ========================="))
                                print(totranslate)
                                print(root[i][j].text)
        print('writing to ' + out_file)
        tree.write(out_file, xml_declaration=True, encoding='utf-8')


def show_usage():
    print('gtranslate.py -i <inputfile> -o <outputfile> -l <languageCode e.g. "zh-CN>"')


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:o:l:", ["ifile=", "ofile=", "lfile="])
    except getopt.GetoptError:
        show_usage()
        sys.exit(2)

    if (len(opts) < 1) | (len(opts) > 3):
        show_usage()
        sys.exit(2)

    input_file = ''
    output_language = ''
    output_file = None

    for opt, arg in opts:
        if opt == '-h':
            show_usage()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
        elif opt in ("-l", "--lfile"):
            output_language = arg

    if len(opts) == 3:
        translator = Translator()
        if (output_file is None):
            output_file = translator.get_output_filename(input_file, output_language)

        print('Input file is        : ', input_file)
        print('Output file is       : ', output_file)

        translator.translate_xml_file(input_file, output_file, "auto", output_language)


if __name__ == "__main__":
    main(sys.argv[1:])
