import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1        # nr of files used for the answer
SENTENCE_MATCHES = 1    # nr of sentences used for the answer

def main():

    files = load_files("corpus")
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }

    # calculate IDF values across files
    file_idfs = compute_idfs(file_words)

    # prompt user for query, ex. Query: blussen ladder
    query = set(tokenize(input("Query: ")))

    # determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # extract sentences from n top file(s)
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):

    # given a directory name, return a dictionary with key=filename and value=contents

    file_dict = dict()

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, mode="r", encoding="utf8") as file:
                file_string = file.read()
                file_dict[filename] = file_string

    return file_dict

def tokenize(document):

    # given a string return a list of all of the words
    # convert to lowercase and remove punctuation or stopwords

    cleaned_tokens = []

    tokens = nltk.tokenize.word_tokenize(document.lower())

    # ensure all tokens are lowercase, non-stopwords, non-punctuation
    for token in tokens:
        if token in nltk.corpus.stopwords.words('dutch'): # replace with 'english'?
            continue
        else:
            all_punct = True
            for char in token:
                if char not in string.punctuation:
                    all_punct = False
                    break

            if not all_punct:
                cleaned_tokens.append(token)

    return cleaned_tokens

def compute_idfs(documents):

    # documents = dictionary where key=filename or sentence and value=list of words/tokens
    #   ex1: {'jip.txt': ['jip', 'en', 'janneke', 'lopen', 'samen', 'naar', 'school']}
    #   ex2: {'Jip en Janneke lopen samen naar school.': ['jip', 'en', 'janneke', 'lopen', 'samen', 'naar', 'school']}

    # returns a dictionary that maps words to their IDF-value
    #   ex1: suppose corpus has 2 docs and 1 doc contains the word 'jip' then word_idfs["school"] = ln(1/2) = 0.693
    #   ex2: suppose corpus has 6 docs and 2 docs contain the word 'keuken' then word_idfs["keuken"] = ln(6/2) = 1.0986

    # number of documents
    num_docs = len(documents)
    # dictionary to count number of docs containing each word
    count_docs_have_word = dict()
    for values in documents.values():
        unique_words = set(values)
        for word in unique_words:
            if word in count_docs_have_word.keys():
                count_docs_have_word[word] = count_docs_have_word[word] + 1
            else:
                count_docs_have_word[word] = 1

    ### your code
    word_idfs = {}
    for word, doc_count in count_docs_have_word.items():
        word_idfs[word] = math.log(num_docs / doc_count)

    return word_idfs

def top_files(query, files, idfs, n):

    # query = a set of words
    # files = a dict key=filename and value=list of words (tokens)
    # idfs = a dictionary that maps words to their IDF-value
    # n = number 0 < n <= nr of files
    # returns a list of n filenames that match the query, ranked according to tf-idf

    if n < 1: n = 1

    # dictionary to hold scores for files
    file_scores = {filename:0 for filename in files}
    # print(file_scores)

    sorted_files = None
    query_words = query.copy()
    for word in query:
        if word not in idfs.keys():
            query_words.remove(word)

    for file, words in files.items():
        file_words = set(words)
        for word in file_words:
            if word in query_words:
                file_scores[file] = file_scores[file] + idfs[word]

    # return best n files
    sorted_files = sorted([file for file in files], key= lambda x: (file_scores[x]), reverse=True)
    return sorted_files[:n]


def top_sentences(query, sentences, idfs, n):

    # query = a set of words
    # sentences = dictionary where key=sentence and value=list of words/tokens
    #   ex: {'Jip en Janneke lopen samen naar school.': ['jip', 'en', 'janneke', 'lopen', 'samen', 'naar', 'school']}
    # idfs = a dictionary that maps words to their IDF-value
    # n = nr of files used for the answer
    # returns a list of the n top sentences that match

    # dict to score sentences:
    sentence_score = {sentence:{'idf_score': 0, 'length':0, 'query_words':0, 'qtd_score':0} for sentence in sentences}

    ### your code
    for key, values in sentences.items():
        sentence = set(values)
        sentence_score[key]['length'] = len(sentence)
        for word in sentence:
            if word in query:
                word_idf = idfs[word]
                sentence_score[key]['idf_score'] = sentence_score[key]['idf_score']+word_idf
                sentence_score[key]['query_words'] = sentence_score[key]['query_words'] + 1
        sentence_score[key]['qtd_score'] = round(sentence_score[key]['query_words'] / sentence_score[key]['length'], 3)

    # example: Query: jip
    # sentence_score:
    # {'Jip en Janneke lopen samen naar school.': {'idf_score': 0.693, 'length': 8, 'query_words': 1, 'qtd_score': 0.125}, 
    #  'Takkie mag ook mee.': {'idf_score': 0, 'length': 5, 'query_words': 0, 'qtd_score': 0.0}}

    # rank sentences by score and return n sentence
    sorted_sentences = sorted([sentence for sentence in sentences], key= lambda x: (sentence_score[x]['idf_score'], sentence_score[x]['qtd_score']), reverse=True)
    print(sentence_score[sorted_sentences[0]])
    return sorted_sentences[:n]

if __name__ == '__main__':
    main()