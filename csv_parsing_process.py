import ngram_tools
import json
import csv
import subprocess
import pymorphy2
import sys


def _get_word():
    custom_word = 'кидать'
    return custom_word


def _creating_csv_reader(custom_word = 'кидать'):
    ngram_url = ngram_tools.choose_right_ngram_url(custom_word)
    try:
        source_csv = open(ngram_url.split('/')[-1][:-3]+'.csv', 'r+',newline='')
    except IOError:
        try:
            p = subprocess.Popen([sys.executable,"creating_word_specified_csv.py",custom_word])
            p.communicate()
            source_csv = open(ngram_url.split('/')[-1][:-3]+'.csv', 'r+',newline='')
        except FileNotFoundError:
            sys.exit("script failed to create")
    return csv.reader(source_csv, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)


def _creating_frequency_dict(csv_reader):
    morph = pymorphy2.MorphAnalyzer()
    counter = 0
    counter_of_objects = 0
    dict_of_objects = {}
    for line in csv_reader:
        counter += 1
        count_of_words = line[3]
        second_word_without_tag = line[1].split('_')[0]
        second_word_parsed = morph.parse(second_word_without_tag)[0]
        if {'NOUN', 'accs'} in second_word_parsed.tag or {'NOUN', 'ablt'} in second_word_parsed.tag \
                or {'NOUN', 'nomn'} in second_word_parsed.tag or {'NPRO', 'accs'} in second_word_parsed.tag \
                or {'NPRO', 'ablt'} in second_word_parsed.tag or {'NPRO', 'nomn'} in second_word_parsed.tag:
            try:
                dict_of_objects[second_word_without_tag] += int(count_of_words)
            except KeyError:
                dict_of_objects[second_word_without_tag] = 1
                counter_of_objects += 1
        ngram_tools.updating_output_row('Dictionary creation process: ' + str(counter) + ' lines parsed and ' +
                                        str(counter_of_objects) + ' objects were specified' )
    return dict_of_objects


def _dict_creation_and_sorting():
    just_csv_reader = _creating_csv_reader(_get_word())
    dict_of_objects = _creating_frequency_dict(just_csv_reader)
    dict_of_objects = sorted(dict_of_objects.items(), key=lambda sample_dict: (sample_dict[1],sample_dict[0]), reverse=True)
    return dict_of_objects


def _final_information_write():
    with open(_get_word() + '_object_list.json','w+') as file:
        json.dump(_dict_creation_and_sorting(), file, ensure_ascii=False )


def main():
    _final_information_write()


if __name__ == '__main__':
    main()