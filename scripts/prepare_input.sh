#!/usr/bin/env bash

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

set -e

if [ $# -ne 1 ]
then
    echo "Usage: $0 inputFile"
    echo " inputFile: with one line per transliteration (with "
    echo "   source and target tab separated)"
    exit 1
fi

inputFile=$1

./normalize_text.py "${inputFile}" "${inputFile}.normalized"
# we pass nbest '1' so that the train dataset would have a single target for each source word 
./align_tokens.py "${inputFile}.normalized" "${inputFile}.normalized.aligned" 1
./split_pronunciation.py "${inputFile}.normalized.aligned" "${inputFile}.normalized.aligned.tokens"

./cross_validation_split.sh "${inputFile}.normalized.aligned.tokens" 
mv "${inputFile}.normalized.aligned.tokens.test" "${inputFile}_20"
mv "${inputFile}.normalized.aligned.tokens.train" "${inputFile}_80"

./cross_validation_split.sh "${inputFile}_80" 
mv "${inputFile}_80.train" "${inputFile}_64"
mv "${inputFile}_80.test" "${inputFile}_16"

