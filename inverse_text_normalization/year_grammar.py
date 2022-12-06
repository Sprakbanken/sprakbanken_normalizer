#!/usr/bin/env python
# coding=utf-8

import pyparsing as pp
from pyparsing import Combine, Word, Keyword, Literal, oneOf, Suppress, Group, StringStart, StringEnd, WordStart, WordEnd, alphanums, printables
from .number_grammar import teens, belowhundred, hundred, ten, tens, compnum, zero, lownum, wstart, wend

# change Pyparsing's default whitespace handling
pp.ParserElement.setDefaultWhitespaceChars('\t\n')

# Whitespace and conjunction
WS = Suppress(" ")
CONJ_NO_WS = Suppress("og")

# Return values for year words
multfunc_no_ws = lambda t: (t[0][0]+t[1][0], t[0][1] * t[1][1])
addfunc_no_ws = lambda t: (t[0][0]+"og"+t[1][0], t[0][1] + t[1][1])

# Elements of year words not definded in number_grammar
twenty = Literal("tjue").setParseAction(lambda t: (t[0], 20))
twothousand = Literal("totusen").setParseAction(lambda t: (t[0], 2000))
belowhundred_abovenine = compnum ^ ten ^ teens ^ tens

# Rules for composing year words
Y1 = (teens + hundred).setParseAction(multfunc_no_ws) # nittenhundre
Y2 = (Y1 + CONJ_NO_WS + belowhundred).setParseAction(addfunc_no_ws) # nittenhundreogsekstiåtte
Y3 = (twothousand + CONJ_NO_WS + belowhundred).setParseAction(addfunc_no_ws) # totusenogfire
Y4 = (teens + belowhundred).setParseAction(lambda t: (t[0][0]+t[1][0], (t[0][1]*100) + t[1][1])) #nittensekstiåtte
Y5 = (twenty + belowhundred_abovenine).setParseAction(lambda t: (t[0][0]+t[1][0], (t[0][1]*100) + t[1][1])) #tjuetolv
Y6 = ((teens ^twenty)+Suppress(zero)+lownum).setParseAction(lambda t: (t[0][0]+"null"+t[1][0], (t[0][1]*100) + t[1][1])) # nittennullni
yearpattern = Y1 ^ Y2 ^ Y3 ^ Y4 ^ Y5 ^ Y6 | twothousand

# Full grammar
#yeargrammar = (StringStart() | WS) + (yearpattern) + (StringEnd() | WS).setParseAction(lambda s, l, t: l)
yeargrammar = wstart + yearpattern + wend.setParseAction(lambda s, l, t: l)

if __name__ == "__main__":

    #tests
    print(yeargrammar.parseString("attentretti"))
    print(yeargrammar.parseString("nittenfire"))
    print(yeargrammar.parseString("nittenhundreogfire"))
    print(yeargrammar.parseString("totusen"))
    print(yeargrammar.parseString("totusenogén"))
    print(yeargrammar.parseString("tjueti"))
    print(yeargrammar.parseString("tjuesekstiåtte"))
    #print(yeargrammar.parseString("nittenåtti-tallet"))
    print(yeargrammar.searchString("blant annet satt hun i Statoils sitt styre store deler av nittenåtti-tallet"))
