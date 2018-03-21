import os
import pprint
import argparse

pp = pprint.PrettyPrinter()
parser = argparse.ArgumentParser()

parser.add_argument('--wikideppaths', type=str, required=True)
parser.add_argument('--relevantdeppaths', type=str, required=True)
parser.add_argument('--outputfile', type=str, required=True)


def extractHyperHypoExtractions(wikideppaths, relevantPaths):
    '''Each line in wikideppaths contains 3 columns
        col1: word1
        col2: word2
        col3: deppath


        Step 1: Check if the path is in relevantPaths
        Step 2: If the path is in relevantPaths, check the type of path
        Step 3: Depending on path type, store (hyponym, hypernym) as word1,word2 or word2,word1
    '''

    depPathExtractions = set()
    with open(wikideppaths, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            w1, w2, deppath = line.split("\t")
            if deppath in relevantPaths:
                if relevantPaths[deppath] == "forward":
                    depPathExtractions.add((w1, w2))
                elif relevantPaths[deppath] == "reverse":
                    depPathExtractions.add((w2, w1))

    # Should finally contain a list of (hyponym, hypernym) tuples

    '''
        IMPLEMENT
    '''
    # print(depPathExtractions)
    return depPathExtractions


def readPaths(relevantdeppaths):

    deppaths2type = {}

    with open(relevantdeppaths) as rdp:
        inputdata = rdp.read().strip()

        inputdata = inputdata.split("\n")

        for line in inputdata:
            data = line.split("\t")
            path = data[0]
            path_type = data[1]
            deppaths2type.update({path: path_type})

    '''
    IMPLEMENTED ABOVE
        READ THE RELEVANT DEPENDENCY PATHS HERE
    '''
    # print(deppaths2type)
    return deppaths2type


def writeHypoHyperPairsToFile(hypo_hyper_pairs, outputfile):
    directory = os.path.dirname(outputfile)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(outputfile, 'w') as f:
        for (hypo, hyper) in hypo_hyper_pairs:
            f.write(hypo + "\t" + hyper + '\n')


def main(args):
    # print(args.wikideppaths)

    relevantPaths = readPaths(args.relevantdeppaths)

    hypo_hyper_pairs = extractHyperHypoExtractions(args.wikideppaths,
                                                   relevantPaths)

    writeHypoHyperPairsToFile(hypo_hyper_pairs, args.outputfile)


if __name__ == '__main__':
    args = parser.parse_args()
    pp.pprint(args)
    main(args)
