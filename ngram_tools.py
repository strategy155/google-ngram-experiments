import sys
import gzip
import urllib.error
import urllib.request

import transliterate

from creating_word_specified_csv import _BIGRAM_SOURCE, _NGRAM_TYPE

_BYTES_IN_MEGABYTES = 1024 * 1024


def download_and_open_gzip(file_url):
    file_name = file_url.split('/')[-1]
    try:
        return gzip.open(file_name, 'rt+', encoding='utf-8')
    except IOError:
        try:
            urllib.request.urlretrieve(file_url, file_name, _reporthook)
        except urllib.error.URLError:
            print("Internet connection is down, try later")
            sys.exit()
        return gzip.open(file_name, 'rt+', encoding='utf-8')


def updating_output_row(your_message):
    sys.stdout.write('\r')
    sys.stdout.write(your_message)
    sys.stdout.flush()
    return None


def _reporthook(_block_num, _block_size, _total_size):
    _read_so_far = _block_num * _block_size
    if _total_size > 0:
        _percent_so_far = _read_so_far / _total_size
        _mes = "\r{:.2%} {:.1f} / {:.1f}".format(_percent_so_far, _read_so_far/_BYTES_IN_MEGABYTES,
                                                 _total_size/_BYTES_IN_MEGABYTES) + " megabytes downloaded"
        updating_output_row(_mes)
        if _read_so_far >= _total_size:
            updating_output_row("\n")
    else:
        updating_output_row("read {d}\n".format(_read_so_far))
    return None


def choose_right_ngram_url(word_given):
    """
    :param word_given: string, of the keyword in ngram
    :return:string, url adress which can be used to download ngram, bigram specifically
    """
    _first_two_letters_transliterated = transliterate.translit(word_given, "ru", reversed=True)[:2]
    return _BIGRAM_SOURCE + _first_two_letters_transliterated + _NGRAM_TYPE