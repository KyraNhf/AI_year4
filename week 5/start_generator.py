from pprint import pprint
import json
import markovify

# read text from file
f = open('Nescio-de-Uitvreter.txt', 'r')
text = f.read()

# train and print model for n=2
text_model = markovify.Text(text, state_size=2)
d = text_model.chain.model
# pprint(d)

state = ('Gare', 'du')

if state in d:
    next_words = d[state]
    pprint(next_words)
    total_freq = sum(next_words.values())
    prob = {word: freq/total_freq for word, freq in next_words.items()}
    print(prob)
# generate some sentences

# train and print model for n=3

# generate sentences n=3

