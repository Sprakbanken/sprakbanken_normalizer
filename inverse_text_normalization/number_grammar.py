#!/usr/bin/env python
# coding=utf-8

import pyparsing as pp
from pyparsing import Combine, Word, Keyword, Literal, oneOf, Suppress, Group, StringStart, StringEnd, WordEnd, WordStart, alphanums, printables, FollowedBy

# change Pyparsing's default whitespace handling
pp.ParserElement.setDefaultWhitespaceChars('\t\n')

# Pyparsing grammar that converts identifies Norwegian number words/phrases in the range 1-999999 and 
# converts them to digits

# Number dicts
oneninedict = {"én": 1, "éin": 1, "éi": 1, "eitt": 1, "ett": 1, "to": 2, "tre": 3, \
               "fire": 4, "fem": 5, "seks": 6, "syv": 7, "sju": 7, "åtte": 8, \
              "ni": 9}
teensdict = {"elleve": 11, "tolv": 12, "tretten": 13, "fjorten": 14, "femten": 15, "seksten": 16, \
                "sytten": 17, "atten": 18, "nitten": 19}
abovetwelve = {k: v for k, v in teensdict.items() if v > 12}
tensdict = {"tjue": 20, "tyve": 20, "tretti": 30, "tredve": 30, "førti": 40, "femti": 50, \
                "seksti": 60, "sytti": 70, "åtti": 80, "nitti": 90}

# Patterns for conjunction and whitespace etc.
CONJ = Suppress(" ") + Suppress("og") + Suppress(" ")
WS = Suppress(" ")
extraprintables = "éæøåÆØÅ–" # Characters to be added to Pyparsing's printables
wstart = WordStart(printables + extraprintables) # Start of word
wend = WordEnd(printables + extraprintables) # end of word


# Lambda functions which give appropriate return values for complex number rules (a pair where the first element is 
# the number phrase and the second the calculation of the number phrase)
multfunc = lambda t: (t[0][0]+" "+t[1][0], t[0][1] * t[1][1])
addfunc = lambda t: (t[0][0]+" "+"og"+" "+t[1][0], t[0][1] + t[1][1])
addfuncnows = lambda t: (t[0][0]+t[1][0], t[0][1]+t[1][1])
addfuncnoconj = lambda t: (t[0][0]+" "+t[1][0], t[0][1] + t[1][1])
halfkfunc = lambda t: (t[0][0] + " " + t[1][0] + " " + t[2][0], (t[0][1] * t[2][1]) + t[1][1])

# Rules for number words
lownum = oneOf(oneninedict.keys()).setParseAction(lambda t: (t[0], oneninedict[t[0]]))
ten = Literal("ti").setParseAction(lambda t: (t[0], 10))
teens = oneOf(teensdict.keys()).setParseAction(lambda t: (t[0], teensdict[t[0]]))
thirteentonineteen = oneOf(abovetwelve.keys()).setParseAction(lambda t: (t[0], teensdict[t[0]]))
tens = oneOf(tensdict.keys()).setParseAction(lambda t: (t[0], tensdict[t[0]]))
hundred = Literal("hundre").setParseAction(lambda t: (t[0], 100))
thousand = Literal("tusen").setParseAction(lambda t: (t[0], 1000))
zero = Literal("null").setParseAction(lambda t: (t[0], 0))
halfthousand = Literal("og et halvt").setParseAction(lambda t: (t[0], 500))

thousand_single = thousand + ~FollowedBy(Literal(" takk"))

lownumwten = lownum | ten
compnum = (tens + lownum).setParseAction(addfuncnows)
belowhundred = compnum ^ lownumwten ^ teens ^ tens
numword = compnum | belowhundred | hundred | thousand_single
belowhundred_above_twelve = compnum ^ thirteentonineteen ^ tens
numword_above_twelve = compnum | belowhundred_above_twelve | hundred | thousand_single

# Rules for number phrases
H1 = (lownum + WS + hundred).setParseAction(multfunc) # tre hundre
H2 = (teens + WS + hundred).setParseAction(multfunc) # fjorten hundre
H3 = ((H1 | hundred) + CONJ + belowhundred).setParseAction(addfunc) # hundre og sekstiåtte
H4 = (H2 + CONJ + belowhundred).setParseAction(addfunc) # fjorten hundre og sekstiåtte
T1 = (belowhundred + WS + thousand).setParseAction(multfunc) # sekstiåtte tusen
T2 = ((H3 | H1 | hundred) + WS + thousand).setParseAction(multfunc) # tre hundre og sekstiåtte tusen
T3 = ((T2 | T1 | thousand) + CONJ + belowhundred).setParseAction(addfunc) # femti tusen og sekstiåtte
T4 = ((T2 | T1) + WS + (H3 | H1)).setParseAction(addfuncnoconj) # tre hundre og femtiåtte tusen ni hundre
T5 = (lownum + WS + halfthousand + WS + thousand).setParseAction((halfkfunc))

numpatterns = H1 ^ H2 ^ H3 ^ H4 ^ T1 ^ T2 ^ T3 ^ T4 ^ T5 ^ numword
numpatternszero = numpatterns | zero

# Full grammars
numbergrammar = WordStart() + (numpatterns) + WordEnd().setParseAction(lambda s, l, t: l)
numbergrammar_abovethirteen = wstart + (T5 ^ H1 ^ H2 ^ H3 ^ H4 ^ T1 ^ T2 ^ T3 ^ T4 ^ numword_above_twelve) + wend.setParseAction(lambda s, l, t: l)


if __name__ == "__main__":

    #tests
    print(numbergrammar.searchString("vi har jo bare gjort dette cirka to og et halvt tusen ganger"))
    print(numbergrammar_abovethirteen.searchString("vi har tjue biler"))
    print(numbergrammar.parseString("ni og et halvt tusen"))
    print(numbergrammar.searchString("tusen takk for det president"))

