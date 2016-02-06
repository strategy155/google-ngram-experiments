import UsefulFunctions
import sys


try:
        import pymorphy2
except ImportError:
    UsefulFunctions.install('pymorphy2')
    UsefulFunctions.install('pymorphy2-dicts-ru')
    import pymorphy2


file = UsefulFunctions.download_and_open_gzip(
    'http://storage.googleapis.com/books/ngrams/books/googlebooks-rus-all-2gram-20120701-ki.gz')
file2 = UsefulFunctions.download_and_open_gzip(
    'http://storage.googleapis.com/books/ngrams/books/googlebooks-rus-all-2gram-20120701-br.gz')

morph = pymorphy2.MorphAnalyzer()
dictionaryOfObjects = {}
dictionaryOfObjects1 = {}
counter = 0
counter1 = 0
for line in file:
    counter +=1
    line = line.rstrip('\n')
    ngramFields = line.split('\t')
    ngramFields[0] = ngramFields[0].split(' ') # splitted words
    ngramFields[0][0]= ngramFields[0][0].split('_')[0] # removed tag
    ngramFields[0][1]= ngramFields[0][1].split('_')[0] # removed tag
    firstParsedWord = morph.parse(ngramFields[0][0])[0]
    secondParsedWord = morph.parse(ngramFields[0][1])[0]
    if 'кидать' == firstParsedWord.normal_form and ({'NOUN', 'accs'} in secondParsedWord.tag or {'NOUN', 'nomn'} in secondParsedWord.tag or
                     {'NPRO', 'accs'} in secondParsedWord.tag or {'NOUN','ablt'} in secondParsedWord.tag):  # проверка на винительный падеж(прямой объект)
        # print(ngramFields)
        # print(ngramFields[0][1])
        counter1 +=1
        try:
            dictionaryOfObjects[ngramFields[0][1]] += int(ngramFields[2])
        except KeyError:
            dictionaryOfObjects[ngramFields[0][1]] = int(ngramFields[2])
    sys.stdout.write('\r')
    sys.stdout.write("Parsing progress: " + str(counter) + "  lines parsed |" + "Analysis progress: " + str(counter1) + " count of  'кидать' " )
    sys.stdout.flush()
print('\n')
counter = 0
counter1 = 0
for line in file2:
    counter +=1
    line = line.rstrip('\n')
    ngramFields = line.split('\t')
    ngramFields[0] = ngramFields[0].split(' ') # splitted words
    ngramFields[0][0]= ngramFields[0][0].split('_')[0] # removed tag
    ngramFields[0][1]= ngramFields[0][1].split('_')[0] # removed tag
    firstParsedWord = morph.parse(ngramFields[0][0])[0]
    secondParsedWord = morph.parse(ngramFields[0][1])[0]
    if 'бросать' == firstParsedWord.normal_form and ({'NOUN', 'accs'} in secondParsedWord.tag or {'NOUN', 'nomn'} in secondParsedWord.tag or
                     {'NPRO', 'accs'} in secondParsedWord.tag or {'NOUN','ablt'} in secondParsedWord.tag):  # проверка на винительный падеж(прямой объект)
        # print(ngramFields)
        # print(ngramFields[0][1])
        counter1 +=1
        try:
            dictionaryOfObjects1[ngramFields[0][1]] += int(ngramFields[2])
        except KeyError:
            dictionaryOfObjects1[ngramFields[0][1]] = int(ngramFields[2])
    sys.stdout.write('\r')
    sys.stdout.write("Parsing progress: " + str(counter) + "  lines parsed |" + "Analysis progress: " + str(counter1) + " count of  'бросать' " )
    sys.stdout.flush()

print(dictionaryOfObjects)
print(dictionaryOfObjects1)
file.close()
file2.close()