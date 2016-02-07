import UsefulFunctions


try:
    import pymorphy2
except ImportError:
    UsefulFunctions.install_and_import('pymorphy2')
try:
    import transliterate
except ImportError:
    UsefulFunctions.install_and_import('transliterate')
wordNeeded = 'кидать'
firstTwoLettersFromWordGiven = transliterate.translit(wordNeeded,'ru',reversed=True)[:2]
ngramURL = 'http://storage.googleapis.com/books/ngrams/books/googlebooks-rus-all-2gram-20120701-'+firstTwoLettersFromWordGiven +'.gz'
file = UsefulFunctions.download_and_open_gzip(ngramURL)
processedFile = open(ngramURL.split('/')[-1][:-3], 'a+')
morph = pymorphy2.MorphAnalyzer()
counter = 0
for line in file:
    counter +=1
    line = line.rstrip('\n')
    ngramFields = line.split('\t')
    ngramFields[0] = ngramFields[0].split(' ') # splitted words
    ngramFields[0][0]= ngramFields[0][0].split('_')[0] # removed tag
    ngramFields[0][1]= ngramFields[0][1].split('_')[0] # removed tag
    firstParsedWord = morph.parse(ngramFields[0][0])[0]
    if wordNeeded == firstParsedWord.normal_form:
        processedFile.write(ngramFields[0][0] + ' ' + ngramFields[0][1] + ' ' + ngramFields[2] + '\n')
file.close()
processedFile.close()