__author__ = 'rim'
import argparse
import random
import re

host_name = "http://kinopoisk.ru/"
number_of_random_urls = 2000


def parse_args():
    parser = argparse.ArgumentParser(description='parse two file names')
    parser.add_argument(dest='general_filename', help='general urls')
    parser.add_argument(dest='examined_filename', help='examined urls')
    parser.add_argument(dest='regex_filename', help='filename for output regexs')
    return parser.parse_args()


def purity(regexs, examined_urls, general_urls):
    p = 0.
    n = 0
    examined_counts = [0] * len(regexs)
    general_counts = [0] * len(regexs)
    for j, u in enumerate(examined_urls):
        for i, r in enumerate(regexs):
            if re.match(r, u):
                examined_counts[i] += 1
                n += 1
    for u in general_urls:
        for i, r in enumerate(regexs):
            if re.match(r, u):
                general_counts[i] += 1
                n += 1
    result_counts = list(zip(examined_counts, general_counts))
    p += sum([max([a, b]) for (a, b) in result_counts]) / n
    result_counts = [a + b for (a, b) in result_counts]
    return p, result_counts


def main():
    args = parse_args()

    with open(args.regex_filename, 'r') as regex_filename, open(args.examined_filename, 'r') as examined_filename, \
            open(args.general_filename, 'r') as general_filename:
        regexs = sorted(regex_filename.read().rstrip('\n').split('\n'))
        examined_urls = examined_filename.read().rstrip('\n').split('\n')
        general_urls = general_filename.read().rstrip('\n').split('\n')

        purity_final = 0.
        m = 50
        regexs_counts = [0] * len(regexs)
        for i in range(m):
            print('BOOTSTRAPPING.', int(i/m*100), '% completed...\n')
            p, counts = purity(regexs, random.sample(examined_urls, number_of_random_urls // 2), random.sample(general_urls, number_of_random_urls // 2))
            purity_final += p
            regexs_counts = [a + b for (a, b) in zip(regexs_counts, counts)]
        print('100 % completed!\n')
        purity_final /= m
        n = sum(regexs_counts)
        print('Total matches =', n, end='\n\n')
        regexs_counts = [100*count / n for count in regexs_counts]
        regexs = [(a, b) for (a, b) in zip(regexs_counts, regexs)]
        regexs = sorted(regexs, key=lambda r: -r[0])
        for r in regexs:
            print(r[0], '% for ', r[1])
        print('\nPurity is', purity_final)

if __name__ == '__main__':
    main()