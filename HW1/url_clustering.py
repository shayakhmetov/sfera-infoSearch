__author__ = 'rim'
import argparse
import random
import re
from sklearn.cluster import DBSCAN
from itertools import groupby
import numpy as np

host_name = "http://kinopoisk.ru/"
number_of_random_urls = 4000
selected_alpha = 0.04
dbscan_eps = 0.2
dbscan_min_samples = 3

def parse_args():
    parser = argparse.ArgumentParser(description='parse two file names')
    parser.add_argument(dest='general_filename', help='general urls')
    parser.add_argument(dest='examined_filename', help='examined urls')
    parser.add_argument('-o', dest='regex_filename', help='filename for output regexs', default='regexs')
    return parser.parse_args()


def get_extension(s):
    result = s.split('.')
    if len(result) > 1 and 2 <= len(result[-1]) <= 5:
        result = result[-1]
        return result
    else:
        return None


def try_to_regex(s):
    s = re.escape(s)
    s = re.sub(r'[^/]+\.flv', '[^/]+\\.flv', s)
    s = re.sub(r'[^/]*%[^/]*', '[^/]*%[^/]*', s)
    s = re.sub(r'[0-9]{4}\-[0-9]{2}\-[0-9]{2}', '[0-9]{4}-[0-9]{2}-[0-9]{2}', s)
    s = re.sub(r'[0-9]+', '[0-9]+', s)
    return s


def divide_and_normalize(urls, qlink=False):
    for every_url in urls:
        url_as_dictionary = {'qlink': qlink, 'url': every_url}

        url = every_url[len(host_name):].split('?')

        if every_url[len(host_name)] == '?':
            url_as_dictionary['segments'] = []
        else:
            url_as_dictionary['segments'] = [try_to_regex(s) for s in url[0].rstrip('/').split('/')]

        if len(url) == 1:
            url_as_dictionary['parameters'] = []
        else:
            url_as_dictionary['parameters'] = [try_to_regex(p) for p in url[-1].split('&')]
        yield url_as_dictionary


def construct_url(u):
    url_string = host_name
    for segment in u['segments']:
        url_string += (segment + '/')
    if u['parameters'] is not []:
        url_string = url_string[:-1] + '?'
        for parameter in u['parameters']:
            url_string += (parameter + '&')
        url_string = url_string[:-1]
    return url_string


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

        if len(url['segments']) > 0:
            extension = get_extension(url['segments'][-1])
            if extension:
                yield {'type': '5', 'value': extension, 'freq': 0} # file extension


def count_freq_features(features, urls):
    for f, feature in enumerate(features):
        for url in urls:
            if feature['type'] == '1':
                if feature['value'] == len(url['segments']):
                    features[f]['freq'] += 1
            elif feature['type'] == '2':
                if feature['value'] == len(url['parameters']):
                    features[f]['freq'] += 1
            elif feature['type'] == '3':
                if len(url['parameters']) > feature['value']['i'] and feature['value']['parameter'] == url['parameters'][feature['value']['i']]:
                    features[f]['freq'] += 1
            elif feature['type'] == '4':
                if len(url['segments']) > feature['value']['i'] and feature['value']['segment'] == url['segments'][feature['value']['i']]:
                    features[f]['freq'] += 1
            elif feature['type'] == '5':
                if len(url['segments']) > 0 and feature['value'] == get_extension(url['segments'][-1]):
                    features[f]['freq'] += 1
    return features


def select_features(features, urls, alpha=selected_alpha):
    features = list(count_freq_features(features, urls))
    features = sorted(features, key=lambda f: -f['freq'])
    n = int(number_of_random_urls*alpha)
    if n >= len(features):
        n = len(features)
    print(n, 'features of', len(features), 'selected.')
    return features[:n]


def assign_features(features, urls):
    urls_with_vectors = urls
    for i, url in enumerate(urls):
        urls_with_vectors[i]['vector'] = [0] * len(features)
        for f, feature in enumerate(features):
            if feature['type'] == '1':
                if feature['value'] == len(url['segments']):
                    urls_with_vectors[i]['vector'][f] = 1
            elif feature['type'] == '2':
                if feature['value'] == len(url['parameters']):
                    urls_with_vectors[i]['vector'][f] = 1
            elif feature['type'] == '3':
                if len(url['parameters']) > feature['value']['i'] and feature['value']['parameter'] == url['parameters'][feature['value']['i']]:
                    urls_with_vectors[i]['vector'][f] = 1
            elif feature['type'] == '4':
                if len(url['segments']) > feature['value']['i'] and feature['value']['segment'] == url['segments'][feature['value']['i']]:
                    urls_with_vectors[i]['vector'][f] = 1
            elif feature['type'] == '5':
                if len(url['segments']) > 0 and feature['value'] == get_extension(url['segments'][-1]):
                    urls_with_vectors[i]['vector'][f] += 1

    return urls_with_vectors


def make_clusters(urls_with_vectors):
    model = DBSCAN(eps=dbscan_eps, min_samples=dbscan_min_samples, metric='jaccard')
    labels = model.fit_predict(np.array([u['vector'] for u in urls_with_vectors]))
    for i, l in enumerate(labels):
        urls_with_vectors[i]['cluster'] = l

    urls_with_vectors = sorted(urls_with_vectors, key=lambda u: u['cluster'])
    clusters = []
    for k, us in groupby(urls_with_vectors, key=lambda u: u['cluster']):
        clusters.append(list(us))

    return clusters


def get_segment_regex(segments):
    uniq_segments = []
    for s in segments:
        if s not in uniq_segments:
            uniq_segments.append(s)

    find = False
    for u in uniq_segments:
        if re.search(r'%', u):
            find = True
            break
    if find:
        return '[^/]+'

    if len(uniq_segments) == 1:
        return uniq_segments[0]
    else:
        if len(uniq_segments) > 8:
            return '[^/]+'
        else:
            return '(' + '|'.join(uniq_segments) + ')'


def get_parameters_regex(parameters):
    uniq_parameters = []
    for p in parameters:
        if p not in uniq_parameters:
            uniq_parameters.append(p)

    find = False
    for u in uniq_parameters:
        if re.search(r'%', u):
            find = True
            break
    if find:
        return '.+'
    elif len(uniq_parameters) == 1:
        return uniq_parameters[0]
    else:
        if len(uniq_parameters) >= 3:
            return '.+'
        else:
            return '(' + '|'.join(uniq_parameters) + ')'+'{' + '0,' + str(len(uniq_parameters)) + '}'


def shorten_regex(regex):
    pattern = re.compile('(\(\[\^/\]\+\)\?/\?)+')
    return pattern.sub('.+', regex)


def get_regex_cluster(cluster):
    if len(cluster) == 1:
        regex = construct_url(cluster[0])
        if cluster[0]['parameters'] == 0 and regex[-1] != '/':
            regex += '/?'
        elif regex[-1] == '/':
            regex += '?'
        return regex + '$'
    else:
        # min_segments = zip(*[u['segments'] for u in cluster])
        # min_segments = [list(segments) for segments in min_segments]

        l = min(cluster, key=lambda url: len(url['segments']))
        l = len(l['segments'])
        m = max(cluster, key=lambda url: len(url['segments']))
        m = len(m['segments'])
        regex = host_name
        if l != 0:
            for i in range(l):
                regex += (get_segment_regex([u['segments'][i] for u in cluster]) + '/')
            regex += '?'
        if m > l:
            if l != 0:
                regex = regex[:-1]
            for i in range(l, m):
                if i > 10:
                    regex += '.+'
                    break
                else:
                    regex_segments = get_segment_regex([u['segments'][i] for u in cluster if len(u['segments']) > i])
                    if regex_segments[0] == '(':
                        regex += (regex_segments + '?/?')
                    else:
                        regex += ('(' + regex_segments + ')?/?')
        l = min(cluster, key=lambda url: len(url['parameters']))
        l = len(l['parameters'])
        m = max(cluster, key=lambda url: len(url['parameters']))
        m = len(m['parameters'])
        if m != 0:
            regex = regex[:-2]
            parameters = []

            for u in cluster:
                for p in u['parameters']:
                    parameters.append(p)

            regex += ('\\?' + get_parameters_regex(parameters))
        elif m == 0 and regex[-2:] != '/?':
            regex += '/?'
        return shorten_regex(regex) + '$'


def get_regular_expressions(clusters):
    clusters_with_unique = []
    for c in clusters:
        unique_cluster_strings = []
        unique_cluster = []
        qlink = 0
        for u in c:
            if u['qlink']:
                    qlink += 1
            url_string = construct_url(u)
            if url_string not in unique_cluster_strings:
                unique_cluster_strings.append(url_string)
                unique_cluster.append(u)
        clusters_with_unique.append({'url_strings': unique_cluster_strings, 'cluster': unique_cluster,
                                     'quality': qlink/len(c), 'regex': get_regex_cluster(unique_cluster)})

    return sorted(clusters_with_unique, key=lambda cluster: -cluster['quality'])


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

        features = select_features(generated_features, urls)
        # for f in features:
        #     print(f)
        # print('...\n')

        print('Assigning features to all urls...')
        urls_with_vectors = assign_features(features, urls)
        # urls_with_vectors = assign_features(features, examined_urls + general_urls)

        print('Clustering...')
        clusters = list(make_clusters(urls_with_vectors))

        print('Getting regex for every cluster...')
        result_clusters = get_regular_expressions(clusters)

        print('Printing results...')
        with open(args.regex_filename, 'w') as file_regexs:
            regs_to_write = []
            for i, c in enumerate(result_clusters):
                print('\n#######', i+1, ' CLUSTER of', len(result_clusters), '#######')
                print('QUALITY =', c['quality'], 'REGEX =', c['regex'], end='\n\n')
                regs_to_write.append(c['regex'])
                for url_string in c['url_strings']:
                    print(url_string)
            regs_to_write = sorted(regs_to_write)
            for reg in regs_to_write:
                file_regexs.write(reg + '\n')


if __name__ == '__main__':
    main()