def install_and_import(package):
    import sys
    try:
        import pip
    except ImportError:
        print("You have no pip module installed")
        sys.exit()
    import importlib
    import site
    try:
        importlib.import_module(package)
    except ImportError:
        pip.main(['install','--upgrade', package])
    finally:
        globals()[package] = importlib.import_module(package)
        importlib.reload(site)


def choose_right_ngram_url(word_given):
    try:
        import transliterate
    except ImportError:
        install_and_import('transliterate')
    first_two_letters_transliterated = transliterate.translit(word_given, 'ru', reversed=True)[:2]
    return 'http://storage.googleapis.com/books/ngrams/books/googlebooks-rus-all-2gram-20120701-' + first_two_letters_transliterated + '.gz'


def download_and_open_gzip(file_url):
    import gzip
    import sys
    file_name = file_url.split('/')[-1]
    try:
        return gzip.open(file_name, 'rt+', encoding='utf-8')
    except IOError:
        try:
            import urllib.error
            import urllib.request
        except ImportError:
            install_and_import('urlib')
            import urllib.request
            import urllib.error
        try:
            urllib.request.urlretrieve(file_url,file_name,_reporthook)
        except urllib.error.URLError:
            print("Internet connection is down, try later")
            sys.exit()
        return gzip.open(file_name, 'rt+', encoding='utf-8')


def updating_output_row(your_message):
    import sys
    sys.stdout.write('\r')
    sys.stdout.write(your_message)
    sys.stdout.flush()


def _reporthook(block_num, block_size, total_size):
    import sys
    read_so_far = block_num * block_size
    if total_size > 0:
        percent = read_so_far * 1e2 / total_size
        mes = "\r%5.1f%% %*d / %d" % (percent, len(str(total_size)), read_so_far, total_size) + " downloaded"
        sys.stderr.write(mes)
        if read_so_far >= total_size:
            sys.stderr.write("\n")
    else:
        sys.stderr.write("read %d\n" % (read_so_far,))

