__author__ = 'rim'
import argparse
import random
import re

host_name = "http://kinopoisk.ru/"
number_of_random_urls = 1000


def parse_args():
    parser = argparse.ArgumentParser(description='parse two file names')
    parser.add_argument(dest='examined_filename', help='examined urls')
    parser.add_argument(dest='general_filename', help='general urls')
    return parser.parse_args()


def try_to_regex(s):
    s = re.sub(r'(%[0-9A-Za-z]{2,3}(\.|,|\+|\-){0,3})+[0-9]*', '[params]', s)
    s = re.sub(r'[0-9]{4}\-[0-9]{2}\-[0-9]{2}', '[date]', s)
    s = re.sub(r'[0-9]+', '[0-9]+', s)
    return s


def divide_and_normalize(urls, qlink=False):
    for every_url in urls:
        url_as_dictionary = {'qlink': qlink, 'url': every_url}

        url = every_url[len(host_name):].split('?')

        if every_url[len(host_name)] == '?':
            url_as_dictionary['segments'] = []
        else:
            if url[0][-1] != '/':
                url[0] += '/'
            url_as_dictionary['segments'] = [try_to_regex(s) for s in url[0].split('/')[:-1]]

        if len(url) == 1:
            url_as_dictionary['parameters'] = []
        else:
            url_as_dictionary['parameters'] = [try_to_regex(p) for p in url[1].split('&')]

        yield url_as_dictionary


def get_random_urls(examined_urls, general_urls):
    first_indices = random.sample(range(len(examined_urls)), number_of_random_urls // 2)
    second_indices = random.sample(range(len(general_urls)), number_of_random_urls // 2)

    urls = [examined_urls[i] for i in first_indices] + [general_urls[i] for i in second_indices]
    random.shuffle(urls)
    return urls


def generate_features(urls):
    for url in urls:
        yield {'type': '1', 'value': len(url['segments']), 'freq': 0}    # number of segments
        yield {'type': '2', 'value': len(url['parameters']), 'freq': 0}  # number of parameters

        for i, parameter in enumerate(url['parameters']):
            yield {'type': '3', 'value': {'i': i, 'parameter': parameter}, 'freq': 0}   # position, parameter=value

        for i, segment in enumerate(url['segments']):
            yield {'type': '4', 'value': {'i': i, 'segment': segment}, 'freq': 0}  # position, segment


def count_freq_features(features, urls):
    freq_features = features.copy()
    for f, feature in enumerate(features):
        for url in urls:
            if feature['type'] == '1':
                if feature['value'] == len(url['segments']):
                    freq_features[f]['freq'] += 1
            elif feature['type'] == '2':
                if feature['value'] == len(url['parameters']):
                    freq_features[f]['freq'] += 1
            elif feature['type'] == '3':
                if len(url['parameters']) > feature['value']['i'] and feature['value']['parameter'] == url['parameters'][feature['value']['i']]:
                    freq_features[f]['freq'] += 1
            elif feature['type'] == '4':
                if len(url['segments']) > feature['value']['i'] and feature['value']['segment'] == url['segments'][feature['value']['i']]:
                    freq_features[f]['freq'] += 1
    return freq_features


def select_features(features, urls, alpha=0.05):
    features = list(count_freq_features(features, urls))
    features = sorted(features, key=lambda f: -f['freq'])
    n = int(number_of_random_urls*alpha)
    if n >= len(features):
        n = len(features)
    print(n, 'features of', len(features), 'selected.')
    return features[:n]


def assign_features(features, urls):
    urls_with_vectors = urls.copy()

    for i, url in enumerate(urls):
        urls_with_vectors[i]['vector'] = [0] * len(features)
        for feature in features:
            if feature['type'] == '1':
                if feature['value'] == len(url['segments']):
                    urls_with_vectors[i]['vector'] = 1
            elif feature['type'] == '2':
                if feature['value'] == len(url['parameters']):
                    urls_with_vectors[i]['vector'] = 1
            elif feature['type'] == '3':
                if len(url['parameters']) > feature['value']['i'] and feature['value']['parameter'] == url['parameters'][feature['value']['i']]:
                    urls_with_vectors[i]['vector'] = 1
            elif feature['type'] == '4':
                if len(url['segments']) > feature['value']['i'] and feature['value']['segment'] == url['segments'][feature['value']['i']]:
                    urls_with_vectors[i]['vector'] = 1

    return urls_with_vectors


def make_clusters(urls_with_vectors):
    pass


def get_regular_expressions(clusters):
    pass


def main():
    args = parse_args()

    with open(args.examined_filename, 'r') as examined_file, open(args.general_filename, 'r') as general_file:

        examined_urls = list(divide_and_normalize(examined_file.read().split('\n')[:-1], qlink=True))
        general_urls = list(divide_and_normalize(general_file.read().split('\n')[:-1], qlink=False))

        urls = get_random_urls(examined_urls, general_urls)
        print(len(urls), ' urls sampled.')

        all_generated_features = list(generate_features(urls))
        generated_features = []
        for f in all_generated_features:
            if f not in generated_features:
                generated_features.append(f)
        print(len(generated_features), 'features generated.')

        features = select_features(generated_features, urls, alpha=0.1)
        for f in features[:7]:
            print(f)
        print('...')

        urls_with_vectors = assign_features(features, examined_urls + general_urls)

        clusters = make_clusters(urls_with_vectors)

        result = get_regular_expressions(clusters)




if __name__ == '__main__':
    main()