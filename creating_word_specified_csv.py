import csv
import sys
import pymorphy2
import ngram_tools


_BIGRAM_SOURCE = "http://storage.googleapis.com/books/ngrams/books/googlebooks-rus-all-2gram-20120701-"
_NGRAM_TYPE = ".gz"


def _get_word_from_parameters():
    """
    :return: string, first parameter provided to this py script
    """
    try:
        return str(sys.argv[1])
    except IndexError:
        print('You didnt provide parameters')
        sys.exit()


def _open_source_tsv(ngram_url):
    return ngram_tools.download_and_open_gzip(ngram_url)


def _creating_csv_writer(ngram_url):
    csv_ngram = open(ngram_url.split('/')[-1][:-3]+'.csv', 'w+',newline='')
    csv_writer = csv.writer(csv_ngram, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
    return csv_writer


def _creating_specified_csv(word_input, source_ngram_tsv, csv_writer):
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


def main():
    _creating_specified_csv(_get_word_from_parameters(),
                            _open_source_tsv(
                                    ngram_tools.choose_right_ngram_url(_get_word_from_parameters())),
                            _creating_csv_writer(
                                    ngram_tools.choose_right_ngram_url(_get_word_from_parameters())))


if __name__ == '__main__':
    main()
