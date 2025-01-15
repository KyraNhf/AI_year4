import nltk
import sys

nltk.download('punkt_tab')


def main():
    slist = [None for x in range(10)]
    slist[0] = "Jip roept moeder."
    slist[1] = "Jip en Janneke spelen in de slaapkamer."
    slist[2] = "Jip is nu heel voorzichtig."
    slist[3] = "Bijna valt Takkie overboord."
    slist[4] = "Takkie loopt weg, met zijn staart tussen zijn pootjes."
    slist[5] = "Er komt een grote rode brandweerauto voorbij."
    slist[6] = "Janneke komt terug met de keukentrap."
    slist[7] = "Hij heeft een slee gezien met twee jongetjes erop en twee hondjes ervoor."
    slist[8] = "De volgende morgen kijkt Jip uit het raam."
    slist[9] = "En als ze klaar zijn, wil Jip direct weer met de trein gaan spelen."

    TERMINALS = """
    N -> "jip" | "moeder" | "janneke" | "slaapkamer" | "takkie" | "staart" | "pootjes" | "brandweerauto" | "keukentrap" | "hij" | "slee" | "jongetjes" | "hondjes" | "raam" | "morgen" | "ze" | "trein"
    V -> "roept" | "spelen" | "is" | "valt" | "loopt" | "komt" | "gezien" | "heeft" | "kijkt" | "zijn" | "wil" | "gaan" | "spelen"
    Det -> "de" | "zijn" | "een" | "twee" | "het" | "weer"
    P -> "in" | "met" | "tussen" | "uit"
    Con -> "en" | "als"
    Adv -> "nu" | "heel" | "bijna" | "overboord" |"weg" | "er" | "voorbij" | "terug" | "erop" | "ervoor" | "klaar" | "direct"
    Adj -> "voorzichtig" | "grote" | "rode" | "volgende"
    """

    NONTERMINALS = """
    S -> NP VP | PP VP | NP PP
    VP -> V | VP NP |VP PP 
    NP -> N | NP NP | Con NP | Det NP | NP PP | Adj NP | N VP | NP V
    PP -> Adv | P NP | Adv PP | Adv Adj | Con PP | Con NP | Adv VP
    """

    # parse CFG from strings
    grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
    parser = nltk.ChartParser(grammar)

    # nltk.ChartParser(grammar, trace=2) # debug
    # to show rules:
    # for p in grammar.productions():
    #    print(p).

    for i, s in enumerate(slist):
        print(s)

        s = preprocess(s)

        try:
            trees = list(parser.parse(s))
        except ValueError as e:
            print(e)
            return
        if not trees:
            print("Could not parse sentence.")
            return

        # print each tree with noun phrase chunks
        for tree in trees:
            tree.pretty_print()

            print("Noun Phrase Chunks")
            for np in np_chunk(tree):
                print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words = nltk.word_tokenize(sentence.lower())

    return [w for w in words if any(c.isalpha() for c in w)]


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    def subtrees_filter(tree: nltk.tree.Tree):
        return tree.label() == "NP" and not any(st.label() == "NP" for st in tree)

    return [st for st in tree.subtrees(subtrees_filter)]


if __name__ == '__main__':
    main()
