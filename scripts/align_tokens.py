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
from collections import defaultdict
from collections import Counter

def align(input_file, output_file, nbest):
     skipped = 0
     total = 0
     source_to_targets = defaultdict(list)
     
     for line in input_file:
         fields = line.rstrip().split('\t')
         source_tokens = fields[0].split()
         target_tokens = fields[1].split()
         total += 1
         if len(source_tokens) != len(target_tokens):
              print("Skipping line, counts? ", len(source_tokens), len(target_tokens), "[", source_tokens, " vs ", target_tokens, "]", line)
              skipped += 1
              continue
         for idx, val in enumerate(source_tokens):
              source_to_targets[source_tokens[idx]].append(target_tokens[idx])
         
     for key, vals in source_to_targets.items():
          for n in Counter(vals).most_common(nbest):
               target, freq = n[0], n[1]
               output_file.write(key + '\t' + target + "\t" + str(freq))
               output_file.write('\n')     

     return (skipped, total)            
     
# main
parser = argparse.ArgumentParser()
parser.add_argument('input')
parser.add_argument('output')
parser.add_argument('nbest', help="Positive integer. Each source maps to the n most common targets.")

args = parser.parse_args()
skipped, total = align(open(args.input, encoding='utf8'), open(args.output, 'w', encoding='utf8'), int(args.nbest))

print("skipped", skipped, "of the", total, "total lines", (skipped / total))