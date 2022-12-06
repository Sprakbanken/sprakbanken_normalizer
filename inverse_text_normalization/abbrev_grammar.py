#!/usr/bin/env python
# coding=utf-8

import pyparsing as pp
from pyparsing import Combine, Word, Keyword, Literal, oneOf, Suppress, Group, StringStart, StringEnd, WordEnd, WordStart, alphanums, printables
from .number_grammar import numpatternszero, WS, wstart, wend

# change Pyparsing's default whitespace handling
pp.ParserElement.setDefaultWhitespaceChars('\t\n')

# Adaptation of the abbreviation table used at Stortinget, although some abbreviations are left out as they were impractical, e.g. currency abbreviations,
# where the spoken word order and the written word order do not match ("hundre kroner" vs. "kr 100"). Some common abbreviations actually used in
#  the Stortinget proceedings, but not present in the table, were added. Also, "prosent" is abbreviated to "%", not "pst." 
abbrevdict = {
                "blant annet": "bl.a.",
                "blant anna": "bl.a.",
                "cirka": "ca.",
                "sirka": "ca.",
                "centimeter": "cm",
                "det vil si": "dvs.",
                "et cetera": "etc.",
                "for eksempel": "f.eks.",
                "fylkesvei": "fv.",
                "kilobyte": "kB",
                "kilometer i timen": "km/t",
                "kilowattimer": "kWh",
                "mellom anna": "m.a.",
                "megabyte": "MB",
                "millimeter": "mm",
                "og liknende": "o.l.",
                "parts per million": "p.p.m",
                "riksvei": "rv.",
                "til dømes": "t.d.",
                "terrawattimer": "TWh",
                "jamfør": "jf.",
                "det vil seie": "dvs.",
                "fylkesveg": "fv.",
                "jevnfør": "jf.",
                "kilowattimar": "kWh",
                "og lignende": "o.l.",
                "og liknande": "o.l.",
                "riksveg": "rv.",
                "terrawattimar": "TWh",
                "terawattimar": "TWh",
                "terawattimer": "TWh",
                "dekar": "daa",
                "desibel": "dB",
                "desiliter": "dl",
                "desimeter": "dm",
                "eller liknende": "e.l.",
                "eller lignende": "e.l.",
                "eller liknande": "e.l.",
                "fra og med": "f.o.m.",
                "gigabyte": "GB",
                "gigawatt": "GW",
                "kilobit": "kb",
                "kilo": "kg",
                "kilogram": "kg",
                "kilometer": "km",
                "kilovolt": "kV",
                "kvadratmeter": "kvm",
                "kilowatt": "kW",
                "megabit": "Mb",
                "milliliter": "ml",
                "millivolt": "mV",
                "megavolt": "MV",
                "milliwatt": "mW",
                "megawatt": "MW",
                "og så bortetter": "osb.",
                "og så vidare": "osv.",
                "og så videre": "osv.",
                "på grunn av": "pga.",
                "petabyte": "PB",
                "petawatt": "PW",
                "terabyte": "TB",
                "terrabyte": "TB",
                "til og med": "t.o.m.",
                "terawatt": "TW",
                "terrawatt": "TW",
                "til eksempel": "t.eks."
            }

# Rules for percent and comma
pst = Literal("prosent").setParseAction(lambda t: (t[0], '%'))
comma =  Literal("komma").setParseAction(lambda t: (t[0], ','))
andhalf = Literal("og en halv").setParseAction(lambda t: (t[0], ',5'))

# Rule compositions
simpleabbrev = oneOf(abbrevdict.keys()).setParseAction(lambda t: (t[0], abbrevdict[t[0]])) # Return abbreviations from abbrevdict
numpst = (numpatternszero + WS + pst).setParseAction(lambda t: (t[0][0] + " " + t[1][0], str(t[0][1]) + t[1][1])) # Convert "seksti prosent" to "60%" (note that correct orthography is "60 %")
numcomma = (numpatternszero + WS + comma + WS + numpatternszero).setParseAction(lambda t: (t[0][0]+" "+t[1][0]+" "+t[2][0], str(t[0][1]) + t[1][1] + str(t[2][1]))) # Convert "seks komma fire" to "6,4"
numcommapst = (numcomma + WS + pst).setParseAction(lambda t: (t[0][0] + " " + t[1][0], t[0][1] + t[1][1])) # Convert "seks komma fire prosent" to "6,4%"
numandhalf = (numpatternszero + WS + andhalf).setParseAction(lambda t: (t[0][0] + " " + t[1][0], str(t[0][1]) + t[1][1])) # Convert "to og en halv" to "2,5"

# Complete grammar
abbrevgrammar = wstart + (numandhalf ^numcommapst ^ numpst ^ numcomma ^ simpleabbrev) + wend.setParseAction(lambda s, l, t: l)


if __name__ == "__main__":

    #tests
    print(abbrevgrammar.parseString("til dømes"))
    print(abbrevgrammar.searchString("blant annet satt hun i Statoils sitt styre og liknende store deler av én prosent"))
    print(abbrevgrammar.searchString("blant annet satt hun i Statoils sitt styre og liknende store deler av nittini prosent av tida"))
    print(abbrevgrammar.searchString("os <ee> Kartverkets tinglysning <INAUDIBLE> så tinglyses omkring én komma seks millioner dokumenter i året"))
