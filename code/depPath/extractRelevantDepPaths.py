import pprint
import argparse
from collections import Counter
import numpy as np
import re

pp = pprint.PrettyPrinter()
parser = argparse.ArgumentParser()
parser.add_argument('--wikideppaths', type=str, required=True)
parser.add_argument('--trfile', type=str, required=True)

parser.add_argument('--outputfile', type=str, required=True)


def extractRelevantPaths(wikideppaths, wordpairs_labels, outputfile):
    '''Each line in wikideppaths contains 3 columns
        col1: word1
        col2: word2
        col3: deppath


        Step 1: Get all "True" pairs in training data
        Step 2: Each time a pair is found in deppaths, record the path (also check if the reversal of the pair exists)
        Step 3: Record the TYPE of the path alongside path
        Step 4: Apply some statistical function to the deppath counts such that overfitting is avoided
        Step 5: Write the paths to the outputfile, as well as the TYPE

    '''

    # Step 1
    true_pairs = set()
    for w1, w2 in wordpairs_labels:
        label = wordpairs_labels[(w1, w2)]
        if label:
            true_pairs.add((w1, w2))


    # Step 2
    lines_read = 0

    relevantDepPaths2counts = dict()
    blacklist = set()
    deppaths2type = {}
    with open(wikideppaths, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            lines_read += 1
            hypo, hyper, deppath = line.split("\t")

            # Step 3
            # checks if pair exists in true training data pairs, and then the type of deppath

            matches = re.match("(\w|\/|\<|\>)*X\/(\w+)\/\w+\<Y\/\w+\/conj", deppath)
            if not matches:
                if (hypo, hyper) in true_pairs and deppath:
                    if deppath not in relevantDepPaths2counts:
                        relevantDepPaths2counts.update({deppath: 0})
                    relevantDepPaths2counts.update({deppath: relevantDepPaths2counts[deppath] + 1})
                    deppaths2type.update({deppath: 'forward'})
                elif (hyper, hypo) in true_pairs and deppath:
                    if deppath not in relevantDepPaths2counts:
                        relevantDepPaths2counts.update({deppath: 0})
                    relevantDepPaths2counts.update({deppath: relevantDepPaths2counts[deppath] + 1})
                    deppaths2type.update({deppath: 'reverse'})
                else:
                    if deppath not in relevantDepPaths2counts:
                        relevantDepPaths2counts.update({deppath: 0})

                    else:
                        count = relevantDepPaths2counts[deppath]
                        relevantDepPaths2counts.update({deppath: 0})

            '''
            IMPLEMENTED ABOVE 
            
                IMPLEMENT METHOD TO EXTRACT RELEVANT DEPEDENCY PATHS HERE

                Make sure to be clear about X being a hypernym/hyponym.

                Dependency Paths can be extracted in multiple different categories, such as
                1. Forward Paths: X is hyponym, Y is hypernym
                2. Reverse Paths: X is hypernym, Y is hyponym
                3. Negative Paths: If this path exists, definitely not a hyper/hyponym relations
                4. etc......
            '''
    # filter out all that are less than or equal to 0
    relevantDepPaths2counts = {key: relevantDepPaths2counts[key] for key in relevantDepPaths2counts
                               if relevantDepPaths2counts[key] > 0}

    # Step 4
    # for now, our statistical filter uses mean and standard deviation
    path_counts = list(relevantDepPaths2counts.values())
    # print(path_counts)
    mean = np.mean(path_counts)
    std = np.std(path_counts)
    print("Mean = " + str(mean))
    print("STD = +" + str(std))
    final_paths = [(deppath, deppaths2type[deppath]) for deppath in relevantDepPaths2counts
                   if relevantDepPaths2counts[deppath] >= 1]

    # Step 5
    with open(outputfile, 'w') as f:
        for dep_path, path_type in final_paths:
                f.write(dep_path + "\t" + path_type)
                f.write('\n')


def readVocab(vocabfile):
    vocab = set()
    with open(vocabfile, 'r') as f:
        for w in f:
            if w.strip() == '':
                continue
            vocab.add(w.strip())
    return vocab


def readWordPairsLabels(datafile):
    wordpairs = {}
    with open(datafile, 'r') as f:
        inputdata = f.read().strip()

    inputdata = inputdata.split("\n")
    for line in inputdata:
        word1, word2, label = line.strip().split('\t')
        word1 = word1.strip()
        word2 = word2.strip()
        wordpairs[(word1, word2)] = label
    return wordpairs


def main(args):
    print(args.wikideppaths)

    wordpairs_labels = readWordPairsLabels(args.trfile)

    print("Total Number of Word Pairs: {}".format(len(wordpairs_labels)))

    extractRelevantPaths(args.wikideppaths, wordpairs_labels, args.outputfile)


if __name__ == '__main__':
    args = parser.parse_args()
    pp.pprint(args)
    main(args)
