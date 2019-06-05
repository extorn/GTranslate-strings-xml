#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt
import lxml.etree as ET
import sys


def extract_text_from_file(input_xml_filename, output_text_filename):
    tree = ET.parse(input_xml_filename)
    root = tree.getroot()
    file = open(output_text_filename, 'w')

    counter = 0

    for i in range(len(root)):
        is_translatable = root[i].get('translatable')
        if (root[i].tag == 'string') & (is_translatable != 'false'):
            counter = counter + 1
            file.write(str(counter) + ':' + root[i].text + '\n')
        if (root[i].tag == 'string-array') & (is_translatable != 'false'):
            for j in range(len(root[i])):
                if root[i][j].tag == 'item':
                    counter = counter + 1
                    file.write(str(counter) + ':' + root[i][j].text + '\n')
    file.close()
    print('Text extracted to ', output_text_filename)


# ------------------------------------------------------------------------------


def show_usage():
    print('dtranslate_xml_to_text.py -i <inputfile> -o <outputfile>')


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        show_usage()
        sys.exit(2)
    if (len(opts) < 1) | (len(opts) > 2):
        show_usage()
        sys.exit(2)

    input_file = ''
    output_file = ''

    for opt, arg in opts:
        if opt == '-h':
            show_usage()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg

    print('Input file is        : ', input_file)
    print('Output file is       : ', output_file)
    extract_text_from_file(input_file, output_file)


if __name__ == "__main__":
    main(sys.argv[1:])
