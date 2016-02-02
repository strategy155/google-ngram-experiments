import RussianSnowballStemmer
import urllib.request
import io
import gzip


def download_and_save_file_locally(file_url, counter=1):
    file_name = "ngram" + str(counter)
    try:
        return gzip.open(file_name, 'rt', encoding='utf-8')
    except IOError:
        urllib.request.urlretrieve(file_url, file_name)
        return gzip.open(file_name, 'rt', encoding='utf-8')

file = download_and_save_file_locally(
    'http://storage.googleapis.com/books/ngrams/books/googlebooks-rus-all-2gram-20120701-ki.gz', 1)
file2 = download_and_save_file_locally(
    'http://storage.googleapis.com/books/ngrams/books/googlebooks-rus-all-2gram-20120701-br.gz', 2)

stemmer = RussianSnowballStemmer.Stemmer() #just to ease codewriting


for line in file:
    line = line.rstrip('\n')
    fields = line.split('\t')
    fields[0] = fields[0].split(' ') #splitted words
    fields[0][0]= fields[0][0].split('_')[0] #removed _VERB tag
    if "кида" == stemmer.stem(fields[0][0]) and "_NOUN" in fields[0][1]: #checking if second word is NOUN
        print(fields)
        fields[0][1]= fields[0][1].split('_')[0] #removed _NOUN tag