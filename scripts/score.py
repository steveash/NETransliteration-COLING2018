#! /usr/bin/env python3
#
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

#
# Script to compute transliteration word-level accuracy. 
#
#   $ ./score.py truth response words
#   matches:
#    1best: 987 (98.11%)
#    2best: 18 (1.79%)
#    3best: 1 (0.10%)
#   accuracy:
#    1best: 0.98
#    2best: 1.00
#    3best: 1.00
#
# Truth and response file formats: word <tab> pronunciation
#
# Example:
#
#   $ cut -f1,2 truth
#   george                ジョージ
#   washington            ワシントン 
#
# The response file has the exact same format. The difference is
# that the response can have multiple pronunciation per word while
# the truth must contain a single pronunciation per word. 
 
import argparse
from collections import defaultdict
 
def read_words(f):
    words_list = []
    words_set = set()
    for line in f:
        line = line.rstrip()
        fields = line.split('\t')
        if not fields[0] in words_set:
            words_set.add(fields[0])
            words_list.append(fields[0])
    return words_list
 

def read_truth_or_response(f, uniq=False):
    source_to_target = defaultdict(list)
    for line in f:
        line = line.rstrip()
        fields = line.split('\t')
        if (len(fields) < 2):
            print("expected 2+ fields, got", line)
            continue
        
        source, target = fields[0], fields[1]
        if uniq and source_to_target[source]:
            raise ValueError("Duplicate words in truth are not allowed: " + line)
        source_to_target[source].append(target)
    return source_to_target


def get_match_index(source_to_target, source, target):
    if source_to_target.get(source):
        for idx, val in enumerate(source_to_target.get(source)):
            if target == val:
                return idx
    return -1

def get_percentage(freq, total):
    return 100 * float(freq)/float(total)
    
    
 
# main
parser = argparse.ArgumentParser()
parser.add_argument('truth')
parser.add_argument('response')
parser.add_argument('words')
args = parser.parse_args() 

truth = read_truth_or_response(open(args.truth, encoding='utf8'), uniq=False)
response = read_truth_or_response(open(args.response, encoding='utf8'))
words = read_words(open(args.words, encoding='utf8'))
matches = dict([(-1, 0), (0, 0), (1, 0), (2, 0)])

for word in words:
    truth_targets = truth.get(word)
    found_hit = False
    found_idx = 100000
    for truth_target in truth_targets:
        match_idx = get_match_index(response, word, truth_target)
        if (match_idx >= 0):
            found_idx = min(found_idx, match_idx)
            found_hit = True

    if (found_hit):        
        matches[found_idx] += 1
    else:
        matches[-1] += 1

total_matches = int(matches[0]) + int(matches[1]) + int(matches[2])
print("total tested: %d" % len(words))
print('matches:\n 1best: %d (%2.2f%%)\n 2best: %d (%2.2f%%)\n 3best: %d (%2.2f%%)' % (
    matches[0], get_percentage(matches[0], total_matches),
    matches[1], get_percentage(matches[1], total_matches),
    matches[2], get_percentage(matches[2], total_matches)))

print('accuracy:\n 1best: %2.2f\n 2best: %2.2f\n 3best: %2.2f' % (
    matches[0] / len(words),
    (matches[0] + matches[1]) / len(words),
    total_matches / len(words)))
