# Language-Model-and-Finite-State-Transducer
Assignment 1 for CS447 NLP Fall 2019 @ UIUC

## Part 1:
Implementation of 3 Language Models (Unigram, Unigram with Add One Smoothing, Bigram) in ***hw1_lm.py***.<br>
***hw1_lm_test.py*** tests the working of the 3 Language Models on a small toy dataset.

## Part 2:
Implementation of a Non Deterministic Finite State Transducer to convert an infinite word to its **-ing** form.<br>
**Examples:**<br>
```
ride   --> riding
see    --> seeing
stop   --> stopping
gather --> gathering
die    --> dying
```
***fst.py*** defines the working of a Finite State Transducer.<br>
***hw1_fst.py*** contains the states and transitions between states to convert input word to its **-ing** form.
