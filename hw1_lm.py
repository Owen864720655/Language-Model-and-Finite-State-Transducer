########################################
## CS447 Natural Language Processing  ##
##           Homework 1               ##
##       Julia Hockenmaier            ##
##       juliahmr@illnois.edu         ##
########################################
##
## Part 1:
## Develop a smoothed n-gram language model and evaluate it on a corpus
##
import os
import random
import sys

from collections import defaultdict
from math import log, exp

#----------------------------------------
#  Data input 
#----------------------------------------

# Read a text file into a corpus (list of sentences (which in turn are lists of words))
def readFileToCorpus(f):
    if os.path.isfile(f):
        file = open(f, "r") # open the input file in read-only mode
        i = 0 # this is just a counter to keep track of the sentence numbers
        corpus = [] # this will become a list of sentences
        print("Reading file", f)
        for line in file:
            i += 1
            sentence = line.split() # split the line into a list of words
            # append this lis as an element to the list of sentences
            corpus.append(sentence)
            if i % 1000 == 0:
    	        # print a status message
                sys.stderr.write("Reading sentence " + str(i) + "\n")
        return corpus
    else:
    # ideally we would throw an exception here, but this will suffice
        print("Error: corpus file ", f, " does not exist")
        sys.exit() # exit the script


# Preprocess the corpus to help avoid sparsity
def preprocess(corpus):
    # find all the rare words
    freqDict = defaultdict(int)
    for sen in corpus:
	    for word in sen:
	       freqDict[word] += 1

    # replace rare words with unk
    for sen in corpus:
        for i in range(0, len(sen)):
            word = sen[i]
            if freqDict[word] < 2:
                sen[i] = UNK

    # bookend the sentences with start and end tokens
    for sen in corpus:
        sen.insert(0, start)
        sen.append(end)
    
    return corpus


def preprocessTest(vocab, corpus):
    # replace test words that were unseen in the training with unk
    for sen in corpus:
        for i in range(0, len(sen)):
            word = sen[i]
            if word not in vocab:
                sen[i] = UNK
    
    # bookend the sentences with start and end tokens
    for sen in corpus:
        sen.insert(0, start)
        sen.append(end)

    return corpus


# Constants 
UNK = "UNK"     # Unknown word token
start = "<s>"   # Start-of-sentence token
end = "</s>"    # End-of-sentence token


#--------------------------------------------------------------
# Language models and data structures
#--------------------------------------------------------------

# Parent class for the three language models you need to implement
class LanguageModel:
    # Initialize and train the model (ie, estimate the model's underlying probability
    # distribution from the training corpus)
    def __init__(self, corpus):
        pass

    # Generate a sentence by drawing words according to the 
    # model's probability distribution
    def generateSentence(self):
        print("Implement the generateSentence method in each subclass")
        return "mary had a little lamb ."

    # Given a sentence (sen), return the probability of 
    # that sentence under the model
    def getSentenceProbability(self, sen):
        print("Implement the getSentenceProbability method in each subclass")
        return 0.0

    # Given a corpus, calculate and return its perplexity 
    # (normalized inverse log probability)
    def getCorpusPerplexity(self, corpus):
        print("Implement the getCorpusPerplexity method")
        return 0.0

    # Given a file (filename) and the number of sentences, generate a list
    # of sentences and write each to file along with its model probability.
    def generateSentencesToFile(self, numberOfSentences, filename):
        filePointer = open(filename, 'w+')
        for i in range(0, numberOfSentences):
            sen = self.generateSentence()
            prob = self.getSentenceProbability(sen)
            stringGenerated = str(prob) + " " + " ".join(sen) 
            

# Unigram language model
class UnigramModel(LanguageModel):
    def __init__(self, corpus):
        self.counts = defaultdict(float)
        self.total = 0.0
        self.vocab = set()
        
        for sen in corpus:
            for i in range(1, len(sen)): # ignore start symbol for unigram counts
                self.counts[(sen[i])] += 1.0 # unigram counts
                self.total += 1.0
                self.vocab.add(sen[i])

        self.vocab_size = len(self.vocab)

    # Returns the probability of word in the distribution
    def prob(self, word):
        return self.counts[(word)]/self.total
    
    # Generate a single random word according to the distribution
    def draw(self):
        rand = random.random()
        for word in self.counts.keys():
            rand -= self.prob(word)
            if rand <= 0.0:
                return word
    
    def generateSentence(self):
        sen = [start]
        while True:
            next_word = self.draw()
            sen.append(next_word)
            if next_word == end:
                break

        return sen

    def getSentenceProbability(self, sen):
        log_prob_sum = 0.0
        for i in range(1, len(sen)):
            if self.prob(sen[i]) == 0.0:
                return 0.0
            log_prob_sum += log(self.prob(sen[i]))

        return exp(log_prob_sum)

    def getCorpusPerplexity(self, corpus):
        log_prob_sum = 0.0
        corpus_total = 0.0
        for sen in corpus:
            for i in range(1, len(sen)):
                corpus_total += 1.0
                if self.prob(sen[i]) == 0.0:
                    print('Unknown unigram in corpus')
                    sys.exit()
                log_prob_sum += log(self.prob(sen[i]))

        return exp(-log_prob_sum/corpus_total)


# Smoothed unigram language model (use laplace for smoothing)
class SmoothedUnigramModel(UnigramModel):
    def __init__(self, corpus):
        super(SmoothedUnigramModel, self).__init__(corpus)
    
    # override UnigramModel prob method
    def prob(self, word):
        return (self.counts[word]+1)/(self.total+self.vocab_size)


# Unsmoothed bigram language model
class BigramModel(LanguageModel):
    def __init__(self, corpus):
        self.counts = defaultdict(float)
        
        for sen in corpus:
            self.counts[(sen[0])] += 1.0
            for i in range(1, len(sen)): # ignore start symbol for unigram counts
                self.counts[(sen[i])] += 1.0 # unigram counts
                self.counts[(sen[i-1], sen[i])] += 1.0 # bigram counts

    # Returns the probability of word in the distribution
    def prob(self, word, prev_word):
        if self.counts[(prev_word, word)] == 0.0:
            return 0.0
        return self.counts[(prev_word, word)]/self.counts[(prev_word)]
    
    # Generate a single random word according to the distribution given a prev_word
    def draw(self, prev_word):
        rand = random.random()
        potential_next_words = [ngrams[1] for ngrams in self.counts.keys() if len(ngrams) == 2 and ngrams[0] == prev_word]
        for word in potential_next_words:
            rand -= self.prob(word, prev_word)
            if rand <= 0.0:
                return word
    
    def generateSentence(self):
        sen = [start]
        while True:
            next_word = self.draw(sen[-1])
            sen.append(next_word)
            if next_word == end:
                break

        return sen

    def getSentenceProbability(self, sen):
        log_prob_sum = 0.0
        for i in range(1, len(sen)):
            if self.prob(sen[i], sen[i-1]) == 0.0:
                return 0.0
            log_prob_sum += log(self.prob(sen[i], sen[i-1]))

        return exp(log_prob_sum)

    def getCorpusPerplexity(self, corpus):
        log_prob_sum = 0.0
        corpus_total = 0.0
        for sen in corpus:
            for i in range(1, len(sen)):
                corpus_total += 1.0
                if self.prob(sen[i], sen[i-1]) == 0.0:
                    print('Unknown bigram in corpus')
                    sys.exit()
                log_prob_sum += log(self.prob(sen[i], sen[i-1]))

        return exp(-log_prob_sum/corpus_total)


#-------------------------------------------
# The main routine
#-------------------------------------------
if __name__ == "__main__":
    # read your corpora
    trainCorpus = readFileToCorpus('train.txt')
    trainCorpus = preprocess(trainCorpus)
    
    posTestCorpus = readFileToCorpus('pos_test.txt')
    negTestCorpus = readFileToCorpus('neg_test.txt')
    
    vocab = set()
    for sen in trainCorpus:
        for word in sen:
            vocab.add(word)

    posTestCorpus = preprocessTest(vocab, posTestCorpus)
    negTestCorpus = preprocessTest(vocab, negTestCorpus)

    # Run sample unigram dist code
    unigram_model = UnigramModel(trainCorpus)
    print("\nUnigramModel output:")
    print("Probability of \"course\":", unigram_model.prob("course"))
    print("Probability of \""+UNK+"\":", unigram_model.prob(UNK))
    print("Random draw:", unigram_model.draw())
    print("posTestCorpus Perplexity:", unigram_model.getCorpusPerplexity(posTestCorpus))
    print("negTestCorpus Perplexity:", unigram_model.getCorpusPerplexity(negTestCorpus))

    smoothed_unigram_model = SmoothedUnigramModel(trainCorpus)
    print("\nSmoothedUnigramModel output:")
    print("Probability of \"course\":", smoothed_unigram_model.prob("course"))
    print("Probability of \""+UNK+"\":", smoothed_unigram_model.prob(UNK))
    print("Random draw:", smoothed_unigram_model.draw())
    print("posTestCorpus Perplexity:", smoothed_unigram_model.getCorpusPerplexity(posTestCorpus))
    print("negTestCorpus Perplexity:", smoothed_unigram_model.getCorpusPerplexity(negTestCorpus))

    bigram_model = BigramModel(trainCorpus)
    print("\nBigramModel output:")
    print("Probability of \"course\" given previous word \"of\":", bigram_model.prob("of", "course"))
    print("Probability of \"i "+UNK+"\":", bigram_model.prob("i", UNK))
    print("Random draw given previous word \"of\":", bigram_model.draw("of"))
    print("posTestCorpus Perplexity:", bigram_model.getCorpusPerplexity(posTestCorpus))
    print("negTestCorpus Perplexity:", bigram_model.getCorpusPerplexity(negTestCorpus))
