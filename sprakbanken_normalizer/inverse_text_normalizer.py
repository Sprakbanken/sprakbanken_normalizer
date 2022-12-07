from .inverse_text_normalization.number_grammar import numbergrammar_abovethirteen
from .inverse_text_normalization.year_grammar import yeargrammar
from .inverse_text_normalization.date_grammar import dategrammar
from .inverse_text_normalization.abbrev_grammar import abbrevgrammar
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
    teststrings = [
        "dagens dato er tjuende juni tjuetjueto",
        "dette er for eksempel en forkortelse",
        "renta er på to komma fire prosent",
        "dette tallet er tre hundre tusen fire hundre og tjueto",
        "denne setninga skal ikke normaliseres og inneholder æøå-",
        "blant annet satt hun i Statoils sitt styre store deler av nittenåtti-tallet",
        "tjuesekstiåtte",
        "totusenogén",
        "nittenhundreogfire",
        "ni og et halvt tusen",
        "av den årsak er det viktig å behandle denne loven i dag slik at de også etter den første oktober har en lov til å forho forholde oss til i tilknytning til den her saken",
        "os <ee> Kartverkets tinglysning <INAUDIBLE> så tinglyses omkring én komma seks millioner dokumenter i året",
    ]
    for test in teststrings:
        print("BEFORE: " + test)
        print("AFTER: " + inv_normalize(test))
        print()
