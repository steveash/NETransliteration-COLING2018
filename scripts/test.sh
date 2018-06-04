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

if [ $# -ne 3 ]
then
    echo "Usage: $0 testInput modelDir method"
    echo " testInput: the input test file (the wd_dataset_20 file, not .words)"
    exit 1
fi

testInput=$1
modelDir=$2
tfmethod=$3

paste <(cut -f1 "${testInput}") > "${testInput}.words"
# add the root of the repo to the python path
export PYTHONPATH=$(readlink -f ../):$PYTHONPATH
# run the appropriate scoring
case "$tfmethod" in
	s2s) echo "Scoring with seq-2-seq" 
		python -m xlit_s2s_nmt.nmt \
    		--inference_input_file="${testInput}.en" \
    		--inference_output_file="${testInput}.decoded" \
    		--out_dir="${modelDir}"

		;;
	t2t) echo "Scoring with tensor2tensor"
		echo $PYTHONPATH
		python "../xlit_t2t/app.py" \
			--decode "$testInput" \
			--return_beams \
			--beam_size 3 \
			--model_dir "${modelDir}" \
			--output "${testInput}.decoded"
		;;
	ps) echo "Testing with phonetisaurus"
		paste <(cut -f1 "${testInput}") > "${testInput}.f1"
		phonetisaurus-apply --model "${modelDir}/model.fst" --word_list "${testInput}.f1" --nbest 3 --probs --pmass 1.0 > "${testInput}.decoded"
		;;
	*)	echo "Dont know TensorFlow method $tfmethod, should be s2s or t2t or ps"
		exit 1
		;;
esac

./score.py "$testInput" "${testInput}.decoded" "${testInput}.words"