# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 2019

11-611 NLP Homework-3 Language Modeling

@author: Jennifer Li

Andrew ID: jiatong2
"""
import sys
import math
import operator

def trainingPrepare(wordsInFile):
    wordDictionary = {}
    totalWordsCount = 0
    vocabulary = 0
    for eachWord in wordsInFile:
        totalWordsCount+=1
        if eachWord in wordDictionary:
            wordDictionary[eachWord] += 1
        else:
            wordDictionary[eachWord] = 1
    # print(totalWordsCount)
    unknownCount = 0
    wordDictionaryWithUnknown = {}
    for word, count in wordDictionary.items():
        if count < 5:
            unknownCount += count
            for i in range(0, len(wordsInFile)):
                if wordsInFile[i] == word:
                    wordsInFile[i] = "UNKNOWNWORD"            
        else:
            vocabulary += 1
            wordDictionaryWithUnknown[word] = count
    wordDictionaryWithUnknown["UNKNOWNWORD"] = unknownCount
    vocabulary += 1
    # print(unknownCount)
    print("Vocab =", vocabulary)
    return wordDictionary, totalWordsCount, vocabulary, wordDictionaryWithUnknown, unknownCount

def bigramModeling(wordsInFile, wordDictionary, vocabulary):
    bigramTable = {}
    for i in range(1, len(wordsInFile)):
        if (wordsInFile[i-1], wordsInFile[i]) in bigramTable.keys():
            bigramTable[(wordsInFile[i-1], wordsInFile[i])] += 1
        else:
            bigramTable[(wordsInFile[i-1], wordsInFile[i])] = 1
    print(len(bigramTable))
    bigramProbTable = {}
    for eachPair, count in bigramTable.items():
        bigramProbTable[eachPair] = count/(wordDictionary[eachPair[0]])
    print("Bigram types =", len(bigramProbTable))
    return bigramTable, bigramProbTable


def trigramModeling(wordsInFile, wordDictionary, bigramTable, vocabulary):
    trigramTable = {}
    for i in range(2, len(wordsInFile)):
        if (wordsInFile[i-2], wordsInFile[i-1], wordsInFile[i]) in trigramTable.keys():
            trigramTable[(wordsInFile[i-2],wordsInFile[i-1], wordsInFile[i])] += 1
        else:
            trigramTable[(wordsInFile[i-2],wordsInFile[i-1], wordsInFile[i])] = 1
    print(len(trigramTable))
    trigramProbTable = {}
    for eachPair, count in trigramTable.items():
        trigramProbTable[eachPair] = count/(bigramTable[(eachPair[0], eachPair[1])])
    print("Trigram types =", len(trigramProbTable))
    return trigramTable, trigramProbTable


def languageModeling(lambda0, lambda1, lambda2, lambda3, testfile,
                     trainingfile):
    trainFile = open(trainingfile, "r")
    trainContent = trainFile.readlines()
    wordsInFile = []
    print("Length of training file: ", len(trainContent))
    for index in range(0, len(trainContent)):
        wordsInLine = trainContent[index].split(" ")
        wordsInFile += wordsInLine
    wordDictionary, totalWordsCount, vocabulary, wordDictionaryWithUnknown, unknownCount = trainingPrepare(wordsInFile)
    uniformProb = 1/vocabulary
    wordUnigramProb = {}
    # print(wordsInFile)
    for word, count in wordDictionaryWithUnknown.items():
        wordUnigramProb[word] = count / totalWordsCount
    print("Unigram types =", len(wordUnigramProb.keys()))
    # print(vocabulary)
    # print(len(wordsInFile))
    # print(totalWordsCount)
    bigramTable, bigramProb = bigramModeling(wordsInFile, wordDictionaryWithUnknown, vocabulary)
    trigramTable, trigramProb = trigramModeling(wordsInFile, wordDictionaryWithUnknown, bigramTable, vocabulary)
    trainFile.close()
    testFile = open(testfile, "r")
    testContent = testFile.readlines()
    wordsInTest = []
    print("Length of test file: ", len(testContent))
    for index in range(0, len(testContent)):
        wordsInLine = testContent[index].split(" ")
        wordsInTest += wordsInLine
    wordsInTestWithUnknown = []
    for eachWord in wordsInTest:
        if eachWord not in wordUnigramProb.keys():
            wordsInTestWithUnknown.append("UNKNOWNWORD")
        else:
            wordsInTestWithUnknown.append(eachWord)
    # print(wordsInTestWithUnknown)
    testProbUnigram = 0
    testProbBigram = 0
    testProbTrigram = 0
    perplexityBase = 0
    for i in range(0, len(wordsInTestWithUnknown)):
        testProbUnigram = 0
        testProbBigram = 0
        testProbTrigram = 0
        testProbUnigram = wordUnigramProb[wordsInTestWithUnknown[i]]
        if i > 0:
            if (wordsInTestWithUnknown[i-1], wordsInTestWithUnknown[i]) in bigramProb.keys():
                testProbBigram = bigramProb[(wordsInTestWithUnknown[i-1], wordsInTestWithUnknown[i])]
            else:
                # if wordsInTestWithUnknown[i-1] in wordDictionary.keys():
                #     testProbBigram = 1/(wordDictionary[wordsInTestWithUnknown[i-1]] + vocabulary)
                # else:
                #     testProbBigram = 1/vocabulary
                testProbBigram = 0
        if i > 1:
            if (wordsInTestWithUnknown[i-2], wordsInTestWithUnknown[i-1], wordsInTestWithUnknown[i]) in trigramProb.keys():
                testProbTrigram = trigramProb[(wordsInTestWithUnknown[i-2], wordsInTestWithUnknown[i-1], wordsInTestWithUnknown[i])]
            else:
                # if (wordsInTestWithUnknown[i-2], wordsInTestWithUnknown[i -1]) in bigramTable.keys():
                #    testProbTrigram = 1/(bigramTable[(wordsInTestWithUnknown[i-2], wordsInTestWithUnknown[i -1])] + vocabulary)
                # else:
                #    testProbTrigram = 1/vocabulary
                testProbTrigram = 0
        combinedProb = 0 * uniformProb + 0 * testProbUnigram + 0.5 * testProbBigram + 0.5 * testProbTrigram
        if combinedProb != 0:
            perplexityBase += math.log(combinedProb, 2)
    perplexity = math.pow(2, -perplexityBase/(len(wordsInTest)))
    testFile.close()
    # outputResult = open("result.txt", "w")
    # outputResult.write(str(perplexity))
    print(perplexity)
    # outputResult.close()
    


if __name__ == '__main__':
    # sys.argv[1] = lambda0 - coefficient for the uniform model
    # sys.argv[2] = lambda1 - coefficient for the unigram model
    # sys.argv[3] = lambda2 - coefficient for the bigram model
    # sys.argv[4] = lambda3 - coefficient for the trigram model
    # sys.argv[5] = testfile - file to calculate perplexity on
    # sys.argv[6] = trainingfile - file to train the four language models
    languageModeling(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
                  sys.argv[5], sys.argv[6])