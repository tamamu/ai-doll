import CaboCha

parser = CaboCha.Parser()

sentence = "すもももももももものうち"

print(parser.parseToString(sentence))

tree = parser.parse(sentence)

print(tree.toString(CaboCha.FORMAT_LATTICE))
