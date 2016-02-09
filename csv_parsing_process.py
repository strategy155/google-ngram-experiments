import ngram_tools


def _checking_if_all_modules_installed():
    ngram_tools.try_install_module('json')
    ngram_tools.try_install_module('pymorphy2')
    ngram_tools.try_install_module('os')
    ngram_tools.install_pip_stuff('pymorphy2-dicts-ru')
    ngram_tools.try_install_module('csv')

_checking_if_all_modules_installed()


import json
import pymorphy2
import os
import csv


def _get_word():
    custom_word = 'кидать'
    return custom_word


def _creating_csv_reader(custom_word = 'кидать'):
    ngram_url = ngram_tools.choose_right_ngram_url(custom_word)
    try:
        source_csv = open(ngram_url.split('/')[-1][:-3]+'.csv', 'r+',newline='')
    except IOError:
        os.system("creating_word_specified_csv.py " + custom_word)
        source_csv = open(ngram_url.split('/')[-1][:-3]+'.csv', 'w+',newline='')
    return csv.reader(source_csv, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)


def creating_frequency_dict(csv_reader):
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
    dict_of_objects = creating_frequency_dict(just_csv_reader)
    dict_of_objects = sorted(dict_of_objects.items(), key=lambda sample_dict: (sample_dict[1],sample_dict[0]), reverse=True)
    return dict_of_objects


def main():
    with open(_get_word() + '_object_list.json','w+') as file:
        json.dump(_dict_creation_and_sorting(), file, ensure_ascii=False )


if __name__ == '__main__':
    main()