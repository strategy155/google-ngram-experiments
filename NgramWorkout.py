import RussianSnowballStemmer
import urllib.request
import urllib.error
import gzip
import pip

pip.main(['install','--upgrade','pymorphy2'])


def download_and_save_file_locally(file_url):
    file_name =file_url.split('/')[-1]
    try:
        return gzip.open(file_name, 'rt', encoding='utf-8')
    except IOError:
        try:
            urllib.request.urlretrieve(file_url, file_name)
            return gzip.open(file_name, 'rt', encoding='utf-8')
        except urllib.error.URLError:
            print("Internet connection is down, try later")
            exit()

file = download_and_save_file_locally(
    'http://storage.googleapis.com/books/ngrams/books/googlebooks-rus-all-2gram-20120701-ki.gz')
file2 = download_and_save_file_locally(
    'http://storage.googleapis.com/books/ngrams/books/googlebooks-rus-all-2gram-20120701-br.gz')

stemmer = RussianSnowballStemmer.Stemmer() # just to ease coding

dictionaryOfObjects = {}


for line in file:
    line = line.rstrip('\n')
    ngramFields = line.split('\t')
    ngramFields[0] = ngramFields[0].split(' ') # splitted words
    ngramFields[0][0]= ngramFields[0][0].split('_')[0] # removed _VERB tag
    if "кида" == stemmer.stem(ngramFields[0][0]) and "_NOUN" in ngramFields[0][1]: # checking if second word is NOUN
        # print(ngramFields)
        ngramFields[0][1]= ngramFields[0][1].split('_')[0] # removed _NOUN tag
        # print(ngramFields[0][1])
        try:
            dictionaryOfObjects[ngramFields[0][1]] += ngramFields[2]
        except KeyError:
            dictionaryOfObjects[ngramFields[0][1]] = ngramFields[2]
print(dictionaryOfObjects)