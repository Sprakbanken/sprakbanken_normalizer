import pyparsing as pp
from pyparsing import (
    oneOf,
    Suppress,
)
from .year_grammar import yearpattern
from .number_grammar import wstart, wend

# change Pyparsing's default whitespace handling
pp.ParserElement.setDefaultWhitespaceChars("\t\n")

ordinaldictlow = {
    "første": "1.",
    "fyrste": "1.",
    "andre": "2.",
    "tredje": "3.",
    "fjerde": "4.",
    "femte": "5.",
    "sjette": "6.",
    "sjuende": "7.",
    "syvende": "7.",
    "sjuande": "7.",
    "åttende": "8.",
    "åttande": "8.",
    "niende": "9.",
    "niande": "9.",
    "tiende": "10.",
    "tiande": "10.",
    "ellevte": "11.",
    "tolvte": "12.",
}

ordinaldicthigh = {
    "trettende": "13.",
    "trettande": "13.",
    "fjortende": "14.",
    "fjortande": "14.",
    "femtende": "15.",
    "femtande": "15.",
    "sekstende": "16.",
    "sekstande": "16.",
    "syttende": "17.",
    "syttande": "17.",
    "attende": "18.",
    "attande": "18.",
    "nittende": "19.",
    "nittande": "19.",
    "tjuende": "20.",
    "tyvende": "20.",
    "tjuande": "20.",
    "tjueførste": "21.",
    "tjuefyrste": "21.",
    "tjueandre": "22.",
    "tjuetredje": "23.",
    "tjuefjerde": "24.",
    "tjuefemte": "25.",
    "tjuesjette": "26.",
    "tjuesjuende": "27.",
    "tjuesyvende": "27.",
    "tjuesjuande": "27.",
    "tjueåttende": "28.",
    "tjueåttande": "28.",
    "tjueniende": "29.",
    "tjueniande": "29.",
    "trettiende": "30.",
    "trettiande": "30.",
    "trettiførste": "31.",
    "trettifyrste": "31.",
}

months = [
    "januar",
    "februar",
    "mars",
    "april",
    "mai",
    "juni",
    "juli",
    "august",
    "september",
    "oktober",
    "november",
    "desember",
]

monthdict = {x: x for x in months}

ordinalsall = {**ordinaldictlow, **ordinaldicthigh}

# Rules for ordinals and month names
loword = oneOf(ordinaldictlow.keys()).setParseAction(
    lambda t: (t[0], ordinaldictlow[t[0]])
)  # første - tolvte
ord = oneOf(ordinalsall.keys()).setParseAction(
    lambda t: (t[0], ordinalsall[t[0]])
)  # første - trettiførste
month = oneOf(monthdict.keys()).setParseAction(
    lambda t: (t[0], monthdict[t[0]])
)  # januar - desember

# Lambda functions which give appropriate return values for date expressions (a pair where the first element is
# the search date string and the second is the return (normalized) date string)
normalfunc = lambda t: (t[0][0] + " " + t[1][0], t[0][1] + " " + t[1][1])
infunc = lambda t: (t[0][0] + " " + "i" + " " + t[1][0], t[0][1] + " " + t[1][1])
denfunc = lambda t: ("den" + " " + t[0][0], t[0][1])
strconcat = lambda t: (t[0][0] + " " + t[1][0], str(t[0][1]) + " " + str(t[1][1]))

# Patterns for "i", whitespace and non-obligatory "den" before date expressions
IN = Suppress(" ") + Suppress("i") + Suppress(" ")
WS = Suppress(" ")
DEF = Suppress("den")

# Rules for composing date expressions
pattern1 = (ord + WS + month).setParseAction(normalfunc)  # tredje juni
pattern2 = (ord + IN + loword).setParseAction(infunc)  # tredje i sjette
pattern3 = (DEF + WS + (pattern1 | pattern2)).setParseAction(
    denfunc
)  # den tredje i sjette / den tredje juni
pattern4 = ((pattern3 ^ pattern1 ^ pattern2) + WS + yearpattern).setParseAction(
    strconcat
)

# Complete grammar
dategrammar = (
    wstart
    + (pattern4 ^ pattern3 ^ pattern1 ^ pattern2)
    + wend.setParseAction(lambda s, l, t: l)
)

if __name__ == "__main__":

    # tests
    print(
        dategrammar.searchString(
            "av den årsak er det viktig å behandle denne loven i dag slik at de også etter den første oktober har en lov til å forho forholde oss til i tilknytning til den her saken"
        )
    )
    print(
        dategrammar.searchString("Vi går igang med dette tredje i sjette tjueseksten")
    )
    print(dategrammar.parseString("den tredje juni"))
    print(dategrammar.parseString("tredje i sjette"))
    print(dategrammar.parseString("den tjueåttende september"))
    print(dategrammar.parseString("niende i tredje"))
    print(
        dategrammar.searchString(
            "blant annet satt hun i Statoils sitt styre store deler av nittenåtti"
        )
    )
