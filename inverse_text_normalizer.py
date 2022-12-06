from inverse_text_normalization.number_grammar import numbergrammar_abovethirteen
from inverse_text_normalization.year_grammar import yeargrammar
from inverse_text_normalization.date_grammar import dategrammar
from inverse_text_normalization.abbrev_grammar import abbrevgrammar
from pyparsing import Word, printables, alphas8bit

wordgrammar = Word(printables + alphas8bit)

grammar = (
    abbrevgrammar
    ^ dategrammar
    ^ yeargrammar
    ^ numbergrammar_abovethirteen
    ^ wordgrammar
)


def inv_normalize(mystring):
    returnstring = ""
    parsed = grammar.searchString(mystring)
    for x in parsed:
        if len(x) == 2:
            returnstring += str(x[0][1]) + " "
        else:
            returnstring += str(x[0]) + " "
    return returnstring[:-1]


if __name__ == "__main__":
    print(inv_normalize("dagens dato er tjuende june tjuetjueto"))
    print(inv_normalize("dette er for eksempel en forkortelse"))
    print(inv_normalize("renta er på to komma fire prosent"))
    print(inv_normalize("dette tallet er tre hundre tusen fire hundre og tjueto"))
    print(inv_normalize("denne setninga skal ikke normaliseres og inneholder æøå-"))
