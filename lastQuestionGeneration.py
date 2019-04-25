# -*- coding: utf-8 -*-
import sys
import nltk
from textblob import TextBlob
import spacy
from spacy import displacy
from collections import Counter
import copy
import re
import random
PRONOUND_LIST = ["he", "she", "they", "his", "her", "their", "you", "your", "yours", "theirs", "hers", "it", "its",'these','those','this','that']


def preprocess(inputFile):
    inFile = open(inputFile, 'r', encoding='UTF-8')
    fileContent = inFile.read()
    linesList = fileContent.split('\n')
    processedFileContent = ""
    # get rid of sub title
    for i in range(len(linesList)):
        if linesList[i] == "See also" or linesList[i] == "Bibliography" or linesList[i] == "References" \
                and linesList[i] == "External links":
            break
        if (not (len(linesList[i].split(" ")) <= 7 and (not linesList[i].__contains__(".")))):
            processedFileContent += linesList[i] + " "
    fileContent = processedFileContent
    fileContent = re.sub("[\(\[].*?[\)\]]", "", fileContent)
    sentences_split = nltk.sent_tokenize(fileContent)

    tokens = []
    for eachLine in sentences_split:
        tokens.append(nltk.word_tokenize(eachLine))
    tokens_w_tags = []
    for each in tokens:
        tokens_w_tags.append(nltk.pos_tag(each))
    tags = [None] * len(tokens_w_tags)
    for i in range(len(tokens_w_tags)):
        for each in tokens_w_tags[i]:
            if tags[i] == None:
                tags[i] = [each[1]]
            else:
                tags[i].append(each[1])
    return fileContent, sentences_split, tokens, tokens_w_tags, tags

def getCompound(subject, compound):
    if subject.n_lefts > 0:
        for each_left_child in subject.lefts:
            compound = getCompound(each_left_child, compound)
    if compound is not None:
        compound = " ".join([compound, subject.orth_])
    else:
        compound = subject.orth_
    if subject.n_rights > 0:
        for each_right_child in subject.rights:
            compound = getCompound(each_right_child, compound)
    return compound

def yesNo_question(inputFile, numQuestions):
    '''
    be:
    am VBP/are VBP/is VBZ
    were VBD / was VBD
    verb:
    '''
    generatedNum = 0
    nlp = spacy.load("en_core_web_sm")
    fileContent, sentences_split, tokens, tokens_w_tags, tags = preprocess(inputFile)
    grammar_be_p_and_ver_p = 'VBP'
    grammar_be_is_and_ver_3 = 'VBZ'
    grammar_be_d_and_ver_d = 'VBD'
    grammar_md = 'MD'
    # print(tags)
    # print(tokens)
    # print(tokens_w_tags)

    for i in range(len(tags)):

        if generatedNum == numQuestions:
            return numQuestions
        # be
        checkedFlg = False
        nlp_sent = nlp(sentences_split[i])

        if grammar_be_p_and_ver_p in tags[i]:
            if grammar_be_p_and_ver_p==list(nlp_sent.sents)[0].root.tag_:
                curr = tags[i].index(list(nlp_sent.sents)[0].root.tag_)
                if tokens[i][curr].lower() == 'am' or tokens[i][curr].lower() == 'are':
                    for X in nlp_sent:

                        if X.dep_.__contains__('nsubj') and X.head.dep_== "ROOT":
                            if X.text.lower() in PRONOUND_LIST:
                                break
                        if X.dep_ == 'ROOT':
                            notRandomGeneration((tokens[i][curr] + " " + " ".join(tokens[i][:curr]) + " " + " ".join(
                                tokens[i][curr + 1:-1]) + "?").capitalize())
                            checkedFlg = True
                            generatedNum+=1
                            break
        if checkedFlg:
            continue

        if grammar_be_d_and_ver_d in tags[i]:
            if grammar_be_d_and_ver_d==list(nlp_sent.sents)[0].root.tag_:
                curr = tags[i].index(list(nlp_sent.sents)[0].root.tag_)
                if tokens[i][curr].lower() == 'was' or tokens[i][curr].lower() == 'were':
                    for X in nlp_sent:

                        if X.dep_.__contains__('nsubj') and X.head.dep_ == "ROOT":
                            if X.text.lower() in PRONOUND_LIST:
                                break
                        if X.dep_ == 'ROOT':
                            notRandomGeneration((tokens[i][curr] + " " + " ".join(tokens[i][:curr]) + " " + " ".join(
                                tokens[i][curr + 1:-1]) + "?").capitalize())
                            checkedFlg = True
                            generatedNum += 1
                            break
        if checkedFlg:
            continue

        if grammar_be_is_and_ver_3 in tags[i]:
            if grammar_be_is_and_ver_3==list(nlp_sent.sents)[0].root.tag_:
                curr = tags[i].index(list(nlp_sent.sents)[0].root.tag_)
                if tokens[i][curr].lower() == 'is':
                    for X in nlp_sent:
                        if X.dep_.__contains__('nsubj') and X.head.dep_ == "ROOT":
                            if X.text.lower() in PRONOUND_LIST:
                                break
                        if X.dep_ == 'ROOT':
                            notRandomGeneration((tokens[i][curr] + " " + " ".join(tokens[i][:curr]) + " " + " ".join(
                                tokens[i][curr + 1:-1]) + "?").capitalize())
                            generatedNum += 1
                            checkedFlg = True
                            break
        if checkedFlg:
            continue

        # modal: should
        if grammar_md in tags[i]:
            if grammar_md==list(nlp_sent.sents)[0].root.tag_:
                curr = tags[i].index(list(nlp_sent.sents)[0].root.tag_)
                for X in nlp_sent:
                    if X.dep_.__contains__('nsubj') and X.head.dep_ == "ROOT":
                        if X.text.lower() in PRONOUND_LIST:
                            break
                    if X.dep_ == 'ROOT':
                        notRandomGeneration((tokens[i][curr] + " " + " ".join(tokens[i][:curr]) + " " + " ".join(
                            tokens[i][curr + 1:-1]) + "?").capitalize() )
                        checkedFlg = True
                        generatedNum += 1
                        break

        if checkedFlg:
            continue

        # verb
        if grammar_be_p_and_ver_p in tags[i]:
            if grammar_be_p_and_ver_p==list(nlp_sent.sents)[0].root.tag_:
                curr = tags[i].index(list(nlp_sent.sents)[0].root.tag_)
                if tokens[i][curr].lower() != 'am' and tokens[i][curr].lower() != 'are':
                    for X in nlp_sent:
                        if X.dep_.__contains__('nsubj') and X.head.dep_ == "ROOT":
                            if X.text.lower() in PRONOUND_LIST:
                                break
                        if X.dep_ == 'ROOT':
                            notRandomGeneration(("Do " + " ".join(tokens[i][:curr]) + " " + X.lemma_ + " " + " ".join(
                                tokens[i][curr + 1:-1]) + "?").capitalize() )
                            checkedFlg = True
                            generatedNum += 1
                            break
        if checkedFlg:
            continue
        if grammar_be_d_and_ver_d in tags[i]:
            if grammar_be_d_and_ver_d==list(nlp_sent.sents)[0].root.tag_:
                curr = tags[i].index(list(nlp_sent.sents)[0].root.tag_)
                if tokens[i][curr].lower() != 'was' and tokens[i][curr].lower() != 'were':
                    for X in nlp_sent:
                        if X.dep_.__contains__('nsubj') and X.head.dep_ == "ROOT":
                            if X.text.lower() in PRONOUND_LIST:
                                break
                        if X.dep_ == 'ROOT':
                            notRandomGeneration(("Did " + " ".join(tokens[i][:curr]) + " " + X.lemma_ + " " + " ".join(
                                tokens[i][curr + 1:-1]) + "?").capitalize() )
                            checkedFlg = True
                            generatedNum += 1
                            break
        if checkedFlg:
            continue

        if grammar_be_is_and_ver_3 in tags[i]:
            if grammar_be_is_and_ver_3==list(nlp_sent.sents)[0].root.tag_:
                curr = tags[i].index(list(nlp_sent.sents)[0].root.tag_)
                if tokens[i][curr].lower() != 'is':
                    for X in nlp_sent:
                        if X.dep_.__contains__('nsubj') and X.head.dep_ == "ROOT":
                            if X.text.lower() in PRONOUND_LIST:
                                break
                        if X.dep_ == 'ROOT':
                            notRandomGeneration(("Does " + " ".join(tokens[i][:curr]) + " " + X.lemma_ + " " + " ".join(
                                tokens[i][curr + 1:-1]) + "?").capitalize() )
                            checkedFlg = True
                            generatedNum += 1
                            break
        if checkedFlg:
            continue

    return generatedNum

def notRandomGeneration(question):
    flg=random.randint(0, 1)
    # if flg=1, add not
    if flg==1:
        if (not question.__contains__("not")):
            word = question.split()
            word.insert(1, "not")
            print(' '.join(word))
    else:
        print(question)


def wh_question(inputFile, numQuestions):
    generatedNum = 0
    nlp = spacy.load("en_core_web_sm")
    fileContent, sentences_split, tokens, tokens_w_tags, tags = preprocess(inputFile)
    nlp_sent = nlp(fileContent)
    # print(nlp_sent.sents)
    # print(tokens_w_tags)
    # print(nlp_sent)
    # print([(X.text, X.label_) for X in nlp_sent.ents])
    grammar1_who = ['NNP', 'VB', 'MD']
    grammar2_who = ['NN', 'MD']
    check_duplicate_what = set()
    for i in range(len(tags)):
        # print([(X.text, X.label_) for X in nlp_sent.ents])
        if grammar1_who[0] in tags[i]:
            curr = tags[i].index(grammar1_who[0])
            if curr == 0:
                if grammar1_who[1] in tags[i][curr + 1] or grammar1_who[2] in tags[i][curr + 1]:
                    if (tokens[i][curr], 'PERSON') in [(X.text, X.label_) for X in nlp_sent.ents]:
                        if generatedNum == numQuestions:
                            return numQuestions
                        print("Who " + " ".join(tokens[i][curr + 1:-1]) + "?")
                        generatedNum += 1
            else:
                nlp_sent = nlp(sentences_split[i])
                root_token = list(nlp_sent.sents)[0].root
                if 'PERSON' in [X.label_ for X in nlp_sent.ents]:
                    if root_token.orth_.lower() in ['is', 'are', 'was', 'were']:
                        if 'NNP' in [tmp.tag_ for tmp in root_token.rights]:
                            if 'VB' not in [tmp.tag_ for tmp in root_token.rights] and 'VBZ' not in [tmp.tag_ for tmp in
                                                                                                     root_token.rights]\
                                    and 'VBP' not in [tmp.tag_ for tmp in root_token.rights] and 'VBN' not in\
                                    [tmp.tag_ for tmp in root_token.rights] and 'VBD' not in [tmp.tag_ for tmp in root_token.rights]:
                                for j, X in enumerate(nlp_sent):
                                    # print(j, X, X.dep_, X.pos_, X.tag_, X.ent_iob_, X.ent_type_)
                                    if X.dep_ == 'nsubj' and X.head.dep_ == 'ROOT':
                                        if X.text.lower() in PRONOUND_LIST:
                                            break
                                        subject = X.text
                                        if X.n_lefts + X.n_rights > 0:
                                            compound = None
                                            subject = getCompound(X, compound)
                                if subject is not None:
                                    if not (subject.lower().split().__contains__(
                                            "another") or subject.lower().__contains__("example")\
                                            or subject.lower().split()[0] in PRONOUND_LIST):
                                        question_to_print = "Who " + root_token.orth_ + " " + subject.lower()
                                        if generatedNum == numQuestions:
                                            return numQuestions
                                        question_to_print = question_to_print.split()
                                        print(" ".join(question_to_print) + "?")
                                        generatedNum += 1

        if grammar2_who[0] in tags[i]:
            curr = tags[i].index(grammar2_who[0])
            if curr == 0:
                if grammar2_who[1] in tags[i][curr + 1]:
                    if (tokens[i][curr], 'PERSON') in [(X.text, X.label_) for X in nlp_sent.ents]:
                        if generatedNum == numQuestions:
                            return numQuestions
                        print("Who " + " ".join(tokens[i][curr + 1:-1]) + "?")
                        generatedNum += 1
                        # continue;

        # print(tags[i])
    for i in range(len(tags)):
        nlp_sent = nlp(sentences_split[i])
        root_token = list(nlp_sent.sents)[0].root
        if root_token.orth_.lower() in ['is', 'are', 'was', 'were']:
            if 'NN' in [tmp.tag_ for tmp in root_token.rights]:
                if 'VB' not in [tmp.tag_ for tmp in root_token.rights] and 'VBZ' not in [tmp.tag_ for tmp in root_token.rights]\
                    and 'VBP' not in [tmp.tag_ for tmp in root_token.rights] and 'VBN' not in [tmp.tag_ for tmp in root_token.rights]\
                        and 'VBD' not in [tmp.tag_ for tmp in root_token.rights]:
                    for j, X in enumerate(nlp_sent):
                        # print(j, X, X.dep_, X.pos_, X.tag_, X.ent_iob_, X.ent_type_)
                        if X.dep_ == 'nsubj' and X.head.dep_ == 'ROOT':
                            if X.text.lower() in PRONOUND_LIST:
                                break
                            subject = X.text
                            if X.n_lefts + X.n_rights > 0:
                                compound = None
                                subject = getCompound(X, compound)
                    if subject is not None:
                        if not subject.lower().split()[0] in PRONOUND_LIST:
                            if subject.lower().split()[-1].__contains__('date'):
                                question_to_print = "When " + root_token.orth_ + " " + subject.lower()
                            else:
                                question_to_print = "What " + root_token.orth_ + " "+ subject.lower()
                            if generatedNum == numQuestions:
                                return numQuestions
                            if question_to_print not in check_duplicate_what:
                                check_duplicate_what.add(question_to_print)
                                question_to_print = question_to_print.split()
                                print(" ".join(question_to_print) + "?")
                                generatedNum+=1
                                continue
        elif root_token.tag_ == 'VBD':
            root_index = -1
            # if 'NN' in [tmp.tag_ for tmp in root_token.rights]:
            #     if 'VB' not in [tmp.tag_ for tmp in root_token.rights] and 'VBZ' not in [tmp.tag_ for tmp in root_token.rights]\
            #         and 'VBP' not in [tmp.tag_ for tmp in root_token.rights] and 'VBN' not in [tmp.tag_ for tmp in root_token.rights]\
            #             and 'VBD' not in [tmp.tag_ for tmp in root_token.rights]:
            for j, X in enumerate(nlp_sent):
                # print(j, X, X.dep_, X.pos_, X.tag_, X.ent_iob_, X.ent_type_)
                if X.dep_ == 'nsubj' and X.head.dep_ == 'ROOT':
                    if X.text.lower() in PRONOUND_LIST:
                        break
                    subject = X.text
                    if X.n_lefts + X.n_rights > 0:
                        compound = None
                        subject = getCompound(X, compound)
                elif X.dep_ == 'ROOT' and X.orth_ == root_token.orth_:
                    root_index = j
            if subject is not None:
                if not subject.lower().split()[0] in PRONOUND_LIST and root_index != -1:
                    nlp_text = [tmp.text for tmp in nlp_sent[root_index:-1]]
                    question_to_print = "What " +  " ".join(nlp_text)
                    if generatedNum == numQuestions:
                        return numQuestions
                    if question_to_print not in check_duplicate_what and len(question_to_print.split()) > 8:
                        check_duplicate_what.add(question_to_print)
                        question_to_print = question_to_print.split()
                        print(" ".join(question_to_print) + "?")
                        generatedNum+=1

        if 'DATE' in [(X.label_) for X in nlp_sent.ents]:
            # print("here")
            # print(sentences_split[i])
            # print(tokens[i])
            tmp_sent = copy.copy(tokens[i])
            verb = None
            subject = None
            ask_tense = None
            for j, X in enumerate(nlp_sent):
                # print(j, X, X.dep_, X.pos_, X.tag_, X.ent_iob_, X.ent_type_)
                if X.dep_ == 'nsubj' and X.head.dep_ == 'ROOT':
                    if X.text.lower() in PRONOUND_LIST:
                        break
                    subject = X.text
                    if X.n_lefts + X.n_rights > 0:
                        compound = None
                        subject = getCompound(X, compound)
                        # subject = (" ".join([compound, subject])).lower()
                if X.dep_ == 'ROOT' and 'VB' in X.tag_:
                    # print("here", X.text)
                    verb_index = j
                    if X.tag_ == 'VBD':
                        # past tense
                        ask_tense = 'did '
                        verb = X.lemma_
                    elif X.tag_ == 'VB' or X.tag_ == 'VBP':
                        # future tense or present
                        if nlp_sent[j - 1].tag_ == 'MD':
                            ask_tense = nlp_sent[j - 1].text + " "
                            verb = X.lemma_
                        else:
                            ask_tense = 'do '
                            verb = X.text
                    elif X.tag_ == 'VBZ':
                        # present tense
                        ask_tense = 'does '
                        verb = X.lemma_
                    elif X.tag_ == 'VBN':
                        if nlp_sent[j - 1].text in ['have', 'has']:
                            ask_tense = nlp_sent[j - 1].text + " "
                            verb = X.text
                        elif nlp_sent[j - 1].text in ['was', 'were']:
                            ask_tense = 'did '
                            verb = 'be ' + X.text
                        elif nlp_sent[j - 1].text == 'been':
                            ask_tense = nlp_sent[j - 2].text + " "
                            verb = 'been ' + X.text
                        verb = X.lemma_
                    if verb in ['is', 'are', 'am', 'be']:
                        # print(verb)
                        verb = None
                        ask_tense = X.text + " "
                if X.pos_ == 'ADP' and nlp_sent[j + 1].ent_type_ == 'DATE' and X.head.dep_ == "ROOT":
                    if subject is None or ask_tense is None:
                        continue
                    if X.text == 'for':
                        continue
                    curr = j
                    if verb is not None:
                        # print("Original:",sentences_split[i])
                        if generatedNum == numQuestions:
                            return numQuestions
                        nlp_text = [tmp.text for tmp in nlp_sent[verb_index + 1:curr]]
                        question_to_print = "When " + ask_tense + subject + " " + verb + " " + " ".join(
                            nlp_text)
                        question_to_print = question_to_print.split()
                        print(" ".join(question_to_print) + "?")
                        # print("###################################")
                        # print(tokens[i])
                        # print("###################################")
                        generatedNum += 1
                    else:
                        # print("Original:",sentences_split[i])
                        if not (subject.lower().split()[0] in PRONOUND_LIST):
                            if generatedNum == numQuestions:
                                return numQuestions
                            nlp_text = [tmp.text for tmp in nlp_sent[verb_index + 1:curr]]
                            question_to_print = ("When " + ask_tense + subject + " " + " ".join(
                                nlp_text))
                            question_to_print = question_to_print.split()
                            print(" ".join(question_to_print)+"?")
                            generatedNum += 1
                    # print("")
                    break

        if 'GPE' in [(X.label_) for X in nlp_sent.ents]:
            # print("here")
            # print(sentences_split[i])
            # print(tokens[i])
            tmp_sent = copy.copy(tokens[i])
            verb = None
            subject = None
            ask_tense = None
            for j, X in enumerate(nlp_sent):
                # print(j, X, X.dep_, X.pos_, X.tag_, X.ent_iob_, X.ent_type_)
                if X.dep_ == 'nsubj' and X.head.dep_ == 'ROOT':
                    if X.text.lower() in PRONOUND_LIST:
                        break
                    subject = X.text
                    if X.n_lefts + X.n_rights > 0:
                        compound = None
                        subject = getCompound(X, compound)

                        # subject = (" ".join([compound, subject])).lower()
                if X.dep_ == 'ROOT' and 'VB' in X.tag_:
                    # print("here", X.text)
                    verb_index = j
                    if X.tag_ == 'VBD':
                        # past tense
                        ask_tense = 'did '
                        verb = X.lemma_
                    elif X.tag_ == 'VB' or X.tag_ == 'VBP':
                        # future tense or present
                        if nlp_sent[j - 1].tag_ == 'MD':
                            ask_tense = nlp_sent[j - 1].text + " "
                            verb = X.lemma_
                        else:
                            ask_tense = 'do '
                            verb = X.text
                    elif X.tag_ == 'VBZ':
                        # present tense
                        ask_tense = 'does '
                        verb = X.lemma_
                    elif X.tag_ == 'VBN':
                        if nlp_sent[j - 1].text in ['have', 'has']:
                            ask_tense = nlp_sent[j - 1].text + " "
                            verb = X.text
                        elif nlp_sent[j - 1].text in ['was', 'were']:
                            ask_tense = 'did '
                            verb = 'be ' + X.text
                        elif nlp_sent[j - 1].text == 'been':
                            ask_tense = nlp_sent[j - 2].text + " "
                            verb = 'been ' + X.text
                        verb = X.lemma_
                    if verb in ['is', 'are', 'am', 'be']:
                        # print(verb)
                        verb = None
                        ask_tense = X.text + " "
                if X.pos_ == 'ADP' and nlp_sent[j + 1].ent_type_ == 'GPE' and X.head.dep_ == "ROOT":
                    if subject is None or ask_tense is None:
                        continue
                    if X.text == 'for':
                        continue
                    curr = j
                    if verb is not None:
                        # print("Original:",sentences_split[i])
                        if not (subject.lower().split()[0] in PRONOUND_LIST):
                            if generatedNum == numQuestions:
                                return numQuestions
                            nlp_text = [tmp.text for tmp in nlp_sent[verb_index + 1:curr+1]]
                            question_to_print = ("Where " + ask_tense + subject + " " + verb + " " + " ".join(
                                nlp_text))
                            question_to_print = question_to_print.split()
                            print(" ".join(question_to_print) + "?")
                            generatedNum += 1
                    else:
                        # print("Original:",sentences_split[i])
                        if not (subject.lower().split()[0] in PRONOUND_LIST):
                            if generatedNum == numQuestions:
                                return numQuestions
                            nlp_text = [tmp.text for tmp in nlp_sent[verb_index + 1:curr+1]]
                            question_to_print = ("Where " + ask_tense + subject + " " + " ".join(
                                nlp_text))
                            question_to_print = question_to_print.split()
                            print(" ".join(question_to_print) + "?")
                            generatedNum += 1
                    # print("")
                    break
        if 'because' in [X.orth_.lower() for X in nlp_sent]:
            start_index = -1
            stop_index = -1
            for (k, X) in enumerate(nlp_sent):
                if X.dep_ == 'nsubj' and X.head.dep_ == 'ROOT' and X in list(nlp_sent.sents)[0].root.lefts:
                    if X.text.lower() in PRONOUND_LIST:
                        break
                    subject = X.text
                    if X.n_lefts + X.n_rights > 0:
                        compound = None
                        subject = getCompound(X, compound)
                    start_index = k
                elif X.text == 'because':
                    # print(X.text, k, nlp_sent[k+1].orth_)
                    stop_index = k
            if subject is None or start_index == -1 or stop_index == -1:
                # print(subject)
                continue
            if stop_index < 8:
                continue
            question_to_print = (
                        "Why " + subject + " " + " ".join([tmp.orth_ for tmp in nlp_sent[start_index + 1 :stop_index]]))
            question_to_print = question_to_print.split()
            if generatedNum == numQuestions:
                return numQuestions
            if question_to_print[-1] == ',' :
                print(" ".join(question_to_print[:-1]) + "?")
            else:
                print(" ".join(question_to_print) + "?")
            generatedNum += 1

    return generatedNum


if __name__ == '__main__':
    # sys.argv[1] = input file name
    # sys.argv[2] = number of questions
    # test(sys.argv[1])
    generatedNum=wh_question(sys.argv[1],int(sys.argv[2]))
    generatedNum2=yesNo_question(sys.argv[1],int(sys.argv[2])-generatedNum)

    for i in range(int(sys.argv[2])-generatedNum-generatedNum2):
        print("null")

