import MeCab

_WAKATI = MeCab.Tagger('-Owakati')
_CHASEN = MeCab.Tagger('-Ochasen')

def punctuate(text):
    result = _WAKATI.parse(text)
    return result

def parseToParts(text):
    node = _CHASEN.parseToNode(text).next
    surfaces = []
    parts = []
    while node:
        surfaces.append(node.surface)
        parts.append(node.feature.split(",")[0])
        node = node.next
    return (surfaces, parts)

def makeDictionary(data):
    dictionary = {}
    index = []
    idict = {}
    for line in data:
        s, p = parseToParts(line)
        for i in range(len(s)):
            if s[i] not in dictionary:
                dictionary[s[i]] = p[i]
                idict[len(index)] = s[i]
                index.append(s[i])
    return (dictionary, index, idict)

def convertToVector(data, index):
    result = []
    for line in data:
        svec = []
        s = parseToParts(line)[0]
        for word in s:
            svec.append(index.index(word))
        result.append(svec)
    return result


if __name__ == '__main__':

    # Open serif dataset
    f = open("../rem1.txt", "r")
    data = f.read().split("\n")
    f.close()

    # Make dictionary and index
    dictionary, index, idict = makeDictionary(data)

    # Serifs convert to list of vector
    svecs = convertToVector(data, index)

    # Show sample vector of serif
    print(svecs[0])
    for i in svecs[0]:
        print(idict[i], end='')
