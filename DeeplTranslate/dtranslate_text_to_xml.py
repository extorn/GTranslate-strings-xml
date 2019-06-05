#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getopt
import re
import sys

import lxml.etree as ET


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
    xml_tree = ''
    currentTranslation = 0
    currentIdx = 0
    # Is \d really an invalid escape sequence???! TODO check if should be \\d
    newTranslationStartPattern = re.compile('^([\d]*):(.*)')
    # use to escape all instances of ' found in the translation text any other 
    # characters that need prefixing with '\' should just be added inside the 2nd square brackets
    characterEscapingPattern = re.compile('([^\\\\])([\'])')

    def translate_xml_file(self, template_xml_file_name, translations_filename,
                           xml_output_filename):
        xml_template_root = self.load_base_xml_file(template_xml_file_name)
        translations = self.load_translations(translations_filename)
        self.merge_translations(xml_template_root, translations)
        self.write_xml_to_file(xml_template_root, xml_output_filename)

    def write_xml_to_file(self, xml_template_root, xml_output_filename):
        xml_template_root.write(xml_output_filename, encoding='utf-8')

    def load_translations(self, translations_filename):
        file = open(translations_filename, 'r')
        translations = file.readlines()
        file.close()
        return translations

    def load_base_xml_file(self, xml_template_filename):
        # cparser = ET.XMLParser(target = CommentedTreeBuilder())

        # def read_xml_file(f):
        # return ET.parse(f, parser=cparser)

        # prepare things
        # tree = ET.parse(XMLINFILE)
        # xml_tree = read_xml_file(xml_template_filename)
        xml_tree = ET.parse(xml_template_filename)
        return xml_tree

    def merge_translations(self, xml_file_root, translations):
        xml_root = xml_file_root.getroot()
        # translation_lines=len(translations)-1
        for i in range(len(xml_root)):
            is_translatable = xml_root[i].get('translatable')
            if (xml_root[i].tag == 'string') & (is_translatable != 'false'):
                value = self.get_next_translation(translations)
                xml_root[i].text = value.rstrip()
            else:
                if (xml_root[i].tag == 'string-array') & (is_translatable != 'false'):
                    for j in range(len(xml_root[i])):
                        if xml_root[i][j].tag == 'item':
                            value = self.get_next_translation(translations)
                            xml_root[i][j].text = value.rstrip()

    def has_more_translations(self, translations):
        return self.currentTranslation < len(translations)

    def get_next_translation(self, translations):
        print('Looking for translation number ', (self.currentTranslation + 1))
        current_line = translations[self.currentIdx]
        multi_line = False
        match = self.newTranslationStartPattern.match(current_line)
        if (match is not None):
            new_translation_id = int(match.group(1))
            if self.currentTranslation + 1 != new_translation_id:
                # This catches a bug in this code where if a translation matches our 
                # pattern we have a problem because it gets out of sync!
                raise ValueError('The current translation id (', new_translation_id,
                                 ') does not match that expected (', (self.currentTranslation + 1),
                                 ')')
            self.currentTranslation += 1
            self.currentIdx += 1
            this_translation = match.group(2)
            # print('translation start: ', self.currentTranslation)

            if (self.currentIdx < len(translations)):
                # Now loop until this translation is ended
                current_line = translations[self.currentIdx]
                match = self.newTranslationStartPattern.match(current_line)
                while (match is None) & (self.currentIdx < len(translations)):
                    self.currentIdx += 1
                    if not multi_line:
                        this_translation += '\n'
                    this_translation += current_line
                    multi_line = True
                    if self.currentIdx < len(translations):
                        current_line = translations[self.currentIdx]
                        match = self.newTranslationStartPattern.match(current_line)
                        # print('translation continues: ')
                        # There is a potential bug here if the line of the translation starts 
                        # matching the pattern.... it'll be caught on the next translation parse execution though.
        else:
            raise SyntaxError('Expected a new translation, but didn\'t match pattern')

        # fix incorrect addition of full-stop by translation service.
        this_translation.replace('".', '"')
        this_translation = self.characterEscapingPattern.sub('\\1\\\\\\2', this_translation)
        print('translation number ', self.currentTranslation, ' is ', this_translation)
        return this_translation


# ------------------------------------------------------------------------------


def show_usage():
    print('dtranslate_text_to_xml.py -i <inputfile> -t <translations> -o <outputfile>')


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:t:o:", ["ifile=", "tfile=", "ofile="])
    except getopt.GetoptError:
        show_usage()
        sys.exit(2)
    if (len(opts) != 1) | (len(opts) != 3):
        show_usage()
        sys.exit(2)

    input_file = ''
    translations_file = ''
    output_file = ''

    for opt, arg in opts:
        if opt == '-h':
            show_usage()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-t", "--tfile"):
            translations_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg

    print('Input file is        : ', input_file)
    print('Translations file is : ', translations_file)
    print('Output file is       : ', output_file)

    RawTranslationsTextParser().translate_xml_file(input_file, translations_file, output_file)


if __name__ == "__main__":
    main(sys.argv[1:])
