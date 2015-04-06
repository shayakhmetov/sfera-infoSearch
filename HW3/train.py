from __future__ import print_function
# -*- coding: utf-8 -*-
__author__ = 'rim'

from lxml import etree
import sys
import codecs
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
from sklearn import metrics
import numpy as np
from sklearn.externals import joblib
import random

potentional_delimeters = ".!?;:-,)_>=({[*%}]\\/|\"+^$#"
best_delimeters = ".!?"


def get_sentences(xml_filename):
    with codecs.open(xml_filename, 'r', encoding='utf-8') as xml_file:
        tree = etree.parse(xml_file)
        root = tree.getroot()
        texts = root.findall("text")
        for text in texts:
            paragraphs = text.find("paragraphs")
            ps = paragraphs.findall("paragraph")
            for p in ps:
                sentences = p.findall("sentence")
                for sentence in sentences:
                    source = sentence.find("source")
                    yield source.text


def get_code_char(char):
    if char in best_delimeters:
        return potentional_delimeters.index(char)
    elif char in potentional_delimeters:
        return potentional_delimeters.index(char)
    elif char.isalpha() and char.islower():
        return len(potentional_delimeters) + 1
    elif char.isalpha() and char.isupper():
        return len(potentional_delimeters) + 2
    elif char.isdigit():
        return len(potentional_delimeters) + 3
    elif char.isspace():
        return len(potentional_delimeters) + 4
    else:
        return len(potentional_delimeters) + 5


def get_features(line, index):
    features = []
    words = line[:index].split()
    next_words = [word.strip() for word in line[index+1:].strip().split()]

    features.append(get_code_char(line[index]))
    features.append(get_code_char(line[index+1]))
    features.append(get_code_char(line[index-1]))

    if next_words[0][0].isupper():
        features.append(0)
    else:
        features.append(1)

    if words[-1][0].isupper():
        features.append(0)
    else:
        features.append(1)

    features.append(len(words))
    features.append(len(next_words))
    features.append(len(words[-1]))
    features.append(len(next_words[0]))
    return features


def construct_examples(sentence, next_sentence):
    sentence = sentence.rstrip()
    next_sentence = next_sentence.rstrip()
    line = sentence + ' ' + next_sentence
    assert len(line) >= 3
    if len(sentence) > 1 and len(next_sentence) > 1:
        features = get_features(line, len(sentence)-1)
        yield {'tag': 0, 'features': features}

    # if len(sentence) >= 50:
    #     rand_index = random.randint(1, len(sentence) - 2)
    #     features = get_features(line, rand_index)
    #     yield {'tag': 1, 'features': features}

    for i, c in enumerate(line):
        if i != 0 and i != len(sentence)-1 and i != len(line)-1:
            if c in potentional_delimeters:
                features = get_features(line, i)
                yield {'tag': 1, 'features': features}




def construct_data_set(sentences):
    data_set = []
    for i, sentence in enumerate(sentences):
        if i != len(sentences) - 1:
            for example in construct_examples(sentence, sentences[i+1]):
                data_set.append(example)
    return data_set


def main():
    xml_filename = 'sentences.xml'
    print("Parsing opencorpora...")
    sentences = [l.encode('utf-8') for l in list(get_sentences(xml_filename)) if l.strip() != '']

    print("Constructing features...")
    data_set = construct_data_set(sentences)
    targets = np.array([d['tag'] for d in data_set])
    data_set = np.array([d['features'] for d in data_set])

    print("Running cross validation...")
    clf = RandomForestClassifier()

    predicted = cross_validation.cross_val_predict(clf, data_set, targets, cv=3)
    target_names = ['конец предложения', 'не конец предложения']
    print(metrics.classification_report(targets, predicted))

    print("Training on the whole data set...")
    clf.fit(data_set, targets)

    print("Feature importances is ", *["%.5f" % f for f in  clf.feature_importances_])
    print("Saving the model...")
    model_filename = 'saved/saved_model'
    joblib.dump(clf, model_filename)

    print("Train completed. Model saved.")

if __name__ == '__main__':
    main()