import ngram_tools
import sys

try:
    word_input = str(sys.argv[1])
except IndexError:
    print('You didnt provide parameters')
    sys.exit()
ngram_tools.try_install_module('pymorphy2')
ngram_tools.install_pip_stuff('pymorphy2-dicts-ru')
ngram_tools.try_install_module('csv')
ngram_url = ngram_tools.choose_right_ngram_url(word_input)
source_ngram_tsv = ngram_tools.download_and_open_gzip(ngram_url)
csv_ngram = open(ngram_url.split('/')[-1][:-3]+'.csv', 'w+',newline='')
counter_tsv = 0
counter_csv = 0
morph = pymorphy2.MorphAnalyzer()
csv_writer = csv.writer(csv_ngram, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)

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

source_ngram_tsv.close()
csv_ngram.close()

if __name__ == '__main__':
