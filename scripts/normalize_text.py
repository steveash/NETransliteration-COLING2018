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
import re

# . often indicates an abberviation so we don't remove it
# ' often used as a pronunication symbol so we don't remove it
punct_list = ['!', ';', '_', ":", "{", "}", "[", "]", "-", "–", "|", "·", "・", "‧", "・", "&"]
flip_punc = ','

def fix_flip(input):
	idx = input.find(flip_punc)
	if (idx < 0):
		return input
	else: 
		return input[idx+1:].strip() + " " + input[:idx]

def normalize(input_file, output_file):
	for line in input_file:
		# ive seen some lines ending in flip punc
		line = line.rstrip(flip_punc).rstrip()
		fields = line.split("\t")
		assert len(fields) == 2
		
		line = fix_flip(fields[0]) + "\t" + fix_flip(fields[1])

		normalized = line.translate({ord(x): ' ' for x in punct_list}).lower()
		output_file.write(normalized)
		output_file.write("\n")
         
    
# main
parser = argparse.ArgumentParser()
parser.add_argument('input')
parser.add_argument('output')
args = parser.parse_args()

normalize(open(args.input, encoding='utf8'), open(args.output, 'w', encoding='utf8'))
