def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install','--upgrade', package])
    finally:
        globals()[package] = importlib.import_module(package)

def download_and_open_gzip(file_url):
    import gzip
    file_name =file_url.split('/')[-1]
    try:
        return gzip.open(file_name, 'rt', encoding='utf-8')
    except IOError:
        import urllib.request
        import urllib.error
        try:
            urllib.request.urlretrieve(file_url, file_name)
            return gzip.open(file_name, 'rt', encoding='utf-8')
        except urllib.error.URLError:
            print("Internet connection is down, try later")
            exit()
