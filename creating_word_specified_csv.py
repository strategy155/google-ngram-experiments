import ngram_tools
import sys


def _checking_if_all_modules_installed():
    ngram_tools.install_or_upgrade_module('pymorphy2')
    ngram_tools.install_pip_stuff('pymorphy2-dicts-ru')


_checking_if_all_modules_installed()


import pymorphy2
import csv


def _get_word_from_parameters():
    try:
        return str(sys.argv[1])
    except IndexError:
        print('You didnt provide parameters')
        sys.exit()


def _get_ngram_url(word_input):
    ngram_url = ngram_tools.choose_right_ngram_url(word_input)
    return ngram_url


def _open_source_tsv(ngram_url):
    source_ngram_tsv = ngram_tools.download_and_open_gzip(ngram_url)
    return source_ngram_tsv


def _creating_csv_writer(ngram_url):
    csv_ngram = open(ngram_url.split('/')[-1][:-3]+'.csv', 'w+',newline='')
    csv_writer = csv.writer(csv_ngram, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
    return csv_writer


def _creating_specified_csv(word_input, csv_writer, source_ngram_tsv):
    counter_tsv = 0
    counter_csv = 0
    morph = pymorphy2.MorphAnalyzer()
    for line in source_ngram_tsv:
        counter_tsv += 1
        line = line.rstrip()
        line = line.replace('\t',' ')
        line = line.split(' ')
        first_word_without_tag = line[0].split('_')[0]
        first_word_normal_form = morph.parse(first_word_without_tag)[0].normal_form
        if word_input == first_word_normal_form:
            csv_writer.writerows([line])
            counter_csv += 1
        ngram_tools.updating_output_row("Creating file process: " + str(counter_tsv) + " lines of tsv file checked and "
                                        + str(counter_csv) + " lines were written in csv file." )




if __name__ == '__main__':
    _creating_specified_csv(_get_word_from_parameters(),
                            _creating_csv_writer(_get_ngram_url(_get_word_from_parameters()))
                            ,_open_source_tsv(_get_ngram_url(_get_word_from_parameters())))