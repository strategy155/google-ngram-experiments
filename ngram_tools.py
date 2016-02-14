import sys
import gzip
import urllib.error
import urllib.request


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
