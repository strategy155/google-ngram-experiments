import ngram_tools
import sys
import json
import os

try:
    import csv
except ImportError:
    ngram_tools.install_and_import('csv')
try:
    import pymorphy2
except ImportError:
    ngram_tools.install_and_import('pymorphy2')
    import pip
    pip.main(['install','--upgrade','pymorphy2-dicts-ru'])
custom_word = 'кидать'
ngram_url = ngram_tools.choose_right_ngram_url(custom_word)
morph = pymorphy2.MorphAnalyzer()
dict_of_objects = {}
try:
    source_csv = open(ngram_url.split('/')[-1][:-3]+'.csv', 'r+',newline='')
except IOError:
    os.system("creating_word_specified_csv.py " + custom_word)
    source_csv = open(ngram_url.split('/')[-1][:-3]+'.csv', 'w+',newline='')
just_csv_reader = csv.reader(source_csv ,delimiter=',',quotechar='"')
for line in just_csv_reader:
    count_of_words = line[3]
    second_word_without_tag = line[1].split('_')[0]
    second_word_parsed = morph.parse(second_word_without_tag)[0]
    if {'NOUN','accs'} in second_word_parsed.tag or {'NOUN','ablt'} in second_word_parsed.tag \
            or {'NOUN','nomn'} in second_word_parsed.tag or {'NPRO','accs'} in second_word_parsed.tag \
            or {'NPRO','ablt'} in second_word_parsed.tag or {'NPRO','nomn'} in second_word_parsed.tag  :
        try:
            dict_of_objects[second_word_without_tag]+= int(count_of_words)
        except KeyError:
            dict_of_objects[second_word_without_tag] = 1
sorted(dict_of_objects.items(), key=lambda sample_dict: (sample_dict[1],sample_dict[0]), reverse=True)
with open(custom_word + '_object_list.json','wb') as file:
    json.dump(dict_of_objects,file)