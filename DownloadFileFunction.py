import urllib.request

def downloadFile(fileName=None , fileURL = None):
    urllib.request.urlretrieve(fileURL, fileName)
    print('File downloaded succesfully, cause i have no idea how to process exceptions')