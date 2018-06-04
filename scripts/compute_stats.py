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

def align(input_file):
	source_len_sum = 0
	target_len_sum = 0
	records = 0
	source_vocab = set()
	target_vocab = set()

	for line in input_file:
		records += 1
		fields = line.rstrip().split('\t')
		source_len_sum += len(fields[0])
		target = fields[1].split(' ')
		target_len_sum += len(target)
		
		for c in fields[0]:
			source_vocab.add(c)

		for c in target:
			target_vocab.add(c)

	print("For ", input_file)
	print("%d records, source vocab %d, target vocab %d" % (records, len(source_vocab), len(target_vocab)))
	print("avg source len %.1f, avg target len %.1f" % (source_len_sum / records, target_len_sum / records))

	
# main
parser = argparse.ArgumentParser()
parser.add_argument('input')
args = parser.parse_args()

align(open(args.input, encoding='utf8'))
