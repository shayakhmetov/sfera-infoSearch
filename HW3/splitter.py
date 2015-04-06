from __future__ import print_function
__author__ = 'rim'
# -*- coding: utf-8 -*-
from sklearn.externals import joblib
import sys
import numpy as np
from train import get_features, potentional_delimeters


def main():
    model_filename = 'saved/saved_model'
    clf = joblib.load(model_filename)
    for line in sys.stdin:
        line = line.decode('utf-8').strip()
        index = 0
        for i, c in enumerate(line):
            if 0 < i < len(line)-1 and i - index > 1 and line[i] in potentional_delimeters:
                features = np.array(get_features(line[index:], i-index))
                y = clf.predict(features)[0]
                if y == 0:
                    print(line[index:i+1].strip())
                    index = i + 1
        print(line[index:].strip())


if __name__ == '__main__':
    main()
