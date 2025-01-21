# https://radimrehurek.com/gensim/models/word2vec.html
# https://radimrehurek.com/gensim/auto_examples/
# https://radimrehurek.com/gensim/auto_examples/tutorials/run_word2vec.htm

# pip install gensim
# pip install nltk

from gensim.models import Word2Vec
from gensim.models import utils
from nltk.corpus import stopwords 
from collections import Counter
import time

f = open('Nescio-de-Uitvreter.txt', 'r')
doc = f.read()

# convert into a list of lowercase tokens, ignoring tokens that are too short or too long
# returns list of strings
list_w_1 = utils.simple_preprocess(doc, deacc=False, min_len=2, max_len=15)

list_w_2 = []
stop_words = set(stopwords.words('dutch'))
stop_words.add('den')
for word in list_w_1:
    if word not in stop_words:
        list_w_2.append(word)

print('** first 30 words:')
print(list_w_2[0:30])
print('** most frequent words (top 10):')
# Count word frequencies
Counter = Counter(list_w_2)
print(Counter.most_common(10))

# init the model, sentence has to be a list of words
# min_count=5 means words that appear less than 5 times are skipped

start_time = time.time()
model = Word2Vec(sentences=[list_w_2], vector_size=60, window=5, min_count=5, workers=4, sg=0)
end_time = time.time()

print("duration : {:06.3f}".format(end_time-start_time))
print()

# get some words from the model
print('** some words from the model:')
for index, word in enumerate(model.wv.index_to_key):
    if index == 10:
        break
    print(f"word #{index}/{len(model.wv.index_to_key)}: {word}")

# Store just the words + their trained embeddings.
#model.wv.save("word2vec.wordvectors")

print('** vector \'japi\': ')
print(model.wv["japi"])
print('** words most siliar to \'japi\':')
print(model.wv.most_similar("japi", topn=10))

print('** cosine japi, bavink:', model.wv.similarity(w1="japi", w2="bavink"))
print('** cosine japi, koekebakker:', model.wv.similarity(w1="japi", w2="koekebakker"))
print('** cosine jenever, bier:', model.wv.similarity(w1="jenever", w2="bier"))
print('** cosine jenever, kerel:', model.wv.similarity(w1="jenever", w2="kerel"))

