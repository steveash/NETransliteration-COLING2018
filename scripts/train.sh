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
    echo "Usage: $0 inputPrefix modelDir method"
    echo " inputPrefix: path to the wd_dataset file; its assumed there are "
    echo "   wd_dataset_64 and wd_dataset_16 files (and others from prepare_input.sh) present"
    echo " method: either s2s or t2t for TensorFlow seq2seq approach or "
    echo "   tensor2tensor approach "
    exit 1
fi

inputPrefix=$1
modelDir=$2
tfmethod=$3
num_units=128
numLayers=2
mkdir -p $modelDir

export PYTHONPATH=$(readlink -f ../):$PYTHONPATH
# run TF training
case "$tfmethod" in
	s2s) echo "Training with seq-2-seq" 
		./split_for_nmt.py "${inputPrefix}_64" 
		./split_for_nmt.py "${inputPrefix}_16"
		./split_for_nmt.py "${inputPrefix}_20"
		./vocab_for_nmt.py "${inputPrefix}.normalized.aligned.tokens" "${inputPrefix}_vocab"

		python -m xlit_s2s_nmt.nmt \
    		--src=en --tgt=tg \
    		--vocab_prefix="${inputPrefix}_vocab"  \
    		--train_prefix="${inputPrefix}_64" \
    		--dev_prefix="${inputPrefix}_16"  \
    		--test_prefix="${inputPrefix}_20" \
    		--out_dir="${modelDir}" \
    		--num_train_steps=1000000 \
    		--steps_per_stats=400 \
		    --num_layers=$numLayers \
		    --num_units=$num_units \
		    --dropout=0.2 \
		    --metrics=accuracy \
		    --beam_width=6 \
    		--num_translations_per_input=3
		;;
	t2t) echo "Training with tensor2tensor"
		paste <(cut -f1,2 "${inputPrefix}_64") > "${inputPrefix}_64.f12"
		paste <(cut -f1,2 "${inputPrefix}_16") > "${inputPrefix}_16.f12"
		echo $PYTHONPATH
		python "../xlit_t2t/app.py" \
			--train "${inputPrefix}_64.f12" \
			--valid "${inputPrefix}_16.f12" \
			--model_dir "${modelDir}" \
			--size $num_units \
			--max_epochs 10 \
			--num_layers $numLayers
		;;
	ps) echo "Training with phonetisaurus"
		paste <(cut -f1,2 "${inputPrefix}_64") > "${inputPrefix}_64.f12"
		phonetisaurus-train --lexicon "${inputPrefix}_64.f12" --dir_prefix "${modelDir}" --seq2_del
		;;
	none) echo "Skipping training"
		;;
	*)	echo "Dont know TensorFlow method $tfmethod, should be s2s or t2t"
		exit 1
		;;
esac

