# NETransliteration-COLING2018

This is a repository containing the tensorflow code, datasets, and scripts to reproduce the results for the paper:

```
Merhav, Yuval and Ash, Stephen. "Design Challenges in Named Entity Transliteration" Proceedings of COLING 2018, the 27th International Conference on Computational Linguistics. 2018.
```

This paper evaluates Named Entity Transliteration using two neural methods (Seq2Seq Encoder Decoder and Tensor2Tensor Transformer) against the WFST method (using Phonetisaurus).

## Abstract
We analyze some of the fundamental design challenges that impact the development of a multilingual state-of-the-art named entity transliteration system, including curating bi-lingual named entity datasets and evaluation of multiple transliteration methods. We empirically evaluate the transliteration task using the traditional weighted finite state transducer (WFST) approach against two neural approaches: the encoder-decoder recurrent neural network method and the recent, non-sequential Transformer method. In order to improve availability of bi-lingual named entity transliteration datasets, we release personal name bilingual dictionaries mined from Wikidata for English to Russian, Hebrew, Arabic, and Japanese Katakana.

Authors: Yuval Merhav (merhavy@amazon.com) and Stephen Ash (ashstep@amazon.com)

The repo is setup with folders:

- `scripts` - bash scripts and python scripts to prepare data, run training, and testing
- `data` - all datasets used in the paper including our new wikidata sets
- `xlit_s2s_nmt` - adaptation of the Tensorflow Seq2Seq NMT tutorial scripts to work for the task of named entity transliteration
- `xlit_t2t` - adaptation of Tensor2Tensor to work for the task of named entity transliteration

# Replicating Tensorflow experimental results

## First time setup

1. Launch an AWS Deep Learning AMI for Ubuntu v3.0 
    * Deep Learning AMI (Ubuntu) Version 3.0
    * We used a p3.2xlarge instance.
    * This bundles CUDA 9 and TensorFlow 1.4.1 

2. Copy the source code repository in `~/repo` (i.e. afterwards this README.md should be at ~/repo/README.md). You can name the folder whatever you want, but in the rest of this guide it assumes it is in `~/repo`
3. Craete an empty `~/models` folder where TF will store checkpoints of models during training

The data files are all named as: `wd_<script>[_<slice>]` where _script_ is the targets script (i.e. English -> Script) and the optional _slice_ is either 80, 20, 16, or 64 which are all different slices for train, development, and test sets. In the notes below a file _prefix_ is only `wd_script` and does not include the slice. The scripts _assume_ that the slice files exist.

4. Active the Python3 TF environment with `source activate tensorflow_p36`
5. Install the right version of tensor2tensor `pip install 'tensor2tensor==1.2.9'`

## Training and Testing
1. Active the Python3 TF environment with `source activate tensorflow_p36`
2. `cd ~/repo/scripts`
3. Run training for a particular file. 
    - The first argument is the path of the input data file _without_ the slice. So if you want to run training for arabic, which has cross validation slices `wd_arabic_64`, `wd_arabic_16`, and `wd_arabic_20` then pass `../data/wd_arabic` as the first argument.
    - The second argument is the path where the model checkpoints should be written. We will write all of the models into subfolders of the `~/models` folder that we previously created.
    - The third argument is either `t2t` for tensor2tensor mode or `s2s` for seq2seq mode.
```
./train.sh ../data/wd_arabic ../../models/arabic_t2t_1 t2t
```
4. Run testing for the held out validation set after training completes. Note that you can also kill training at any time as checkpoints are saved periodically. When you run testing it picks the last checkpoint.
    - The arguments are the same as for train _except_ the data file argument **is** the actual slice file (not just the prefix without the slice). So if you want to evaluate `wd_arabic_20` then pass `../data/wd_arabic_20`
```
./test.sh ../data/wd_arabic_20 ../../models/arabic_t2t_1 t2t
```

This produces result summary with the 1best, 2best, 3best like:
```
total tested: 32927
matches:
 1best: 19642 (79.19%)
 2best: 3753 (15.13%)
 3best: 1410 (5.68%)
accuracy:
 1best: 0.60
 2best: 0.71
 3best: 0.75
```

Matches 1best, 2best, etc. is the count of words correctly predicted that appeared in this position in the top-k results from the decoder. The percentages in the parenthesis indicate the % of total tested words that appeared in that spot.

Accuracy is the % of words that appeared anywhere in the top-k results. Thus the 2best score includes correct words predicted that showed up in either the top spot or second spot in the results. The accuracy here is 1.0 - WER (Word Error Rate).

# Replicating Phonetisaurus experimental results

This process is similar to replicating the Tensorflow results as described above. Read those instructions first as there are some duplicate details omitted from the below description.

## First time setup
1. Install Phonetisaurus as described here: https://github.com/AdolfVonKleist/Phonetisaurus
2. Copy the source code repository in `~/repo` (i.e. afterwards this README.md should be at ~/repo/README.md). You can name the folder whatever you want, but in the rest of this guide it assumes it is in `~/repo`
3. Craete an empty `~/models` folder where TF will store checkpoints of models during training

## Training and Testing
1. `cd ~/repo/scripts`
2. Run training for a particular file. 
    - The first argument is the path of the input data file _without_ the slice. So if you want to run training for arabic, which has cross validation slices `wd_arabic_64`, `wd_arabic_16`, and `wd_arabic_20` then pass `../data/wd_arabic` as the first argument.
    - The third argument is `ps` for Phonetisaurus
```
./train.sh ../data/wd_arabic ../../models/arabic_ps_1 ps
```
3. Run testing for the held out validation set after training completes.
    - The arguments are the same as for train _except_ the data file argument **is** the actual slice file (not just the prefix without the slice). So if you want to evaluate `wd_arabic_20` then pass `../data/wd_arabic_20`
```
./test.sh ../data/wd_arabic_20 ../../models/arabic_ps_1 ps
```

The produces the same scoring output as described in the above section.

# Re-creating the data

In the `data` subfolder we already have the original, raw data from wikidata (e.g. `wd_arabic`), the normalized and aligned data (e.g. `wd_arabic.normalized.aligned.tokens`), and the cross-validation splits that we used in the paper (e.g. `wd_arabic_64`, `wd_arabic_16`, `wd_arabic_20`). However, if you want to re-create new splits or tweak the normalization or alignment, then you can follow these instructions.

Each of the data files mined from wikidata are named `wd_<script>` (e.g. wd_arabic) and include name phrases like:
`Douglas Adams	دوغلاس آدمز`

This is the raw record extracted from wikidata. As described in the paper, we choose to evaluate at the word level. To process the files to normalize, align, and create splits, run the `prepare_input.sh` script:

```bash
cd ~/repo/scripts
./prepare_input.sh ../data/wd_arabic
```

This script calls our to other scripts included in the repo that does normalization and alignment. Refer to `prepare_input.sh` for details.

# Licenses
The code in `xlit_s2s_nmt` and `xlit_t2t` are adapted from other tensorflow repositories and is licensed under the original Apache 2 licenses.

The `data` is adapted from Wikidata and retains its license, Creative Commons CC0 1.0 Universal (see `data/LICENSE`)

The `scripts` folder contains data preparation and train/test scripts licensed under the MIT License.