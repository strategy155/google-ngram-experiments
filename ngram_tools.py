import importlib
import sys


def cool_import(module_name):
    importlib.import_module(module_name)


def install_pip_stuff(package):
    try:
        import pip
    except ImportError:
        print("You have no pip module installed")
        sys.exit('How you are living w/out pip???????')
    pip.main(['install', '--upgrade', package])


def install_or_upgrade_module(package):
    install_pip_stuff(package)


def _checking_if_all_modules_installed():
    install_or_upgrade_module('transliterate')


_checking_if_all_modules_installed()


import transliterate
import gzip
import urllib.error
import urllib.request


def choose_right_ngram_url(word_given):
    first_two_letters_transliterated = transliterate.translit(word_given, 'ru', reversed=True)[:2]
    return 'http://storage.googleapis.com/books/ngrams/books/googlebooks-rus-all-2gram-20120701-' + first_two_letters_transliterated + '.gz'


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


def _reporthook(block_num, block_size, total_size):
    read_so_far = block_num * block_size
    if total_size > 0:
        percent = read_so_far * 1e2 / total_size
        mes = "\r%5.1f%% %*d / %d" % (percent, len(str(total_size)), read_so_far, total_size) + " downloaded"
        sys.stderr.write(mes)
        if read_so_far >= total_size:
            sys.stderr.write("\n")
    else:
        sys.stderr.write("read %d\n" % (read_so_far,))


if __name__ == '__main__':
    print('Sorry. This script contains useful functions.')