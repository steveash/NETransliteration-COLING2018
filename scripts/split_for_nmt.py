#! /usr/bin/env python3

# Copyright 2018 Amazon.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to 
# deal in the Software without restriction, including without limitation the 
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
# sell copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
# THE SOFTWARE.

import argparse
import sys

def align(input_file, en_output_file, tg_output_file):
	# input file is en\ttg and tg is already space separated so just space separate the en side
	for line in input_file:
		fields = line.rstrip().split('\t')
		en_chars = ' '.join(str(c) for c in fields[0])
		en_output_file.write(en_chars +"\n")
		tg_output_file.write(fields[1] +"\n")
    
# main
parser = argparse.ArgumentParser()
parser.add_argument('input')
args = parser.parse_args()

align(open(args.input, encoding='utf8'), open(args.input + ".en", 'w', encoding='utf8'), open(args.input + ".tg", 'w', encoding='utf8'))
