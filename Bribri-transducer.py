#==============================================================
# Dartmouth College, LING48, Spring 2020
# Julian Grunauer (juliang222@gmail.com)
# Modified from code provided by Rolando Coto-Solano 
# (Rolando.A.Coto.Solano@dartmouth.edu)
# 
# Exercise 2: Finite State Transductors
#
# This program uses the openfst and graphviz packages:
# http://www.openfst.org/twiki/bin/view/FST/PythonExtension
# https://graphviz.readthedocs.io/en/stable/manual.html
#
# The Bribri language is spoken by approximately 3000  
# people in southern Costa Rica. It is part of  the Chibchan 
# language family, a family with languages in Costa Rica, 
# Panama and Colombia. In this small example, you will see 
# a transductor that reads BriBri words and decomposes them 
# morphologically and denotes the meaning of each morpheme.
# 
# For example:
#     aleH   -> al-eH & cook-IPFV
#     ali'   -> al-i' & cook-THEME.PFV.IMPROSP
#     alìne -> al-iHn-ex & cook-THEME.MID-PFV.IMPROSP
#
# This program has four parts:
#
# (1) First, we have the fstSymbols. This is the
#     list of all of the elements you are going
#     to have in the FST. 
#
# (2) Second, we have a list of compiler instructions.
#     This is the list of all the transitions and final
#     states in the FST.
#
# (3) Third, we have the spellout function. This
#     function has the string as its input, and 
#     then goes character by character, calculating
#     the path through the FST and its corresponding
#     transformations.
#
# (4) Finally, we have a function that prints the 
#     FST into a PDF so you can see the transitions
#     graphically. (You do not need to modify this)
#
#==============================================================

import openfst_python as fst
from graphviz import render

#====================================================
# The following four functions (linear_fst, 
# apply_fst, accepted, spellout) carry out
# the FST processing. 
#====================================================

def linear_fst(elements, automata_op, keep_isymbols=True, **kwargs):
    """Produce a linear automata."""
    compiler = fst.Compiler(isymbols=automata_op.input_symbols().copy(), 
                            acceptor=keep_isymbols,
                            keep_isymbols=keep_isymbols, 
                            **kwargs)

    for i, el in enumerate(elements):
        print("{} {} {}".format(i, i+1, el),file=compiler)
    print(str(i+1),file=compiler)

    return compiler.compile()

def apply_fst(elements, automata_op, is_project=True, **kwargs):
    """Compose a linear automata generated from `elements` with `automata_op`.

    Args:
        elements (list): ordered list of edge symbols for a linear automata.
        automata_op (Fst): automata that will be applied.
        is_project (bool, optional): whether to keep only the output labels.
        kwargs:
            Additional arguments to the compiler of the linear automata .
    """
    linear_automata = linear_fst(elements, automata_op, **kwargs)
    out = fst.compose(linear_automata, automata_op)
    if is_project:
        out.project(project_output=True)
    return out

def accepted(output_apply):
    """Given the output of `apply_fst` for acceptor, return True is sting was accepted."""
    return output_apply.num_states() != 0
	

def spellout(inputString, inSymbols, inFST):
	output=""
	currentFST = apply_fst(list(inputString), inFST)
	for state in currentFST.states():
		for arc in currentFST.arcs(state):
			if (inSymbols.find(arc.olabel) != "<eps>"):
				output += inSymbols.find(arc.olabel)
	return output
	
	
#================================================
# List of symbols
#================================================

fstSymbols = fst.SymbolTable()
fstSymbols.add_symbol("<eps>", 0)
fstSymbols.add_symbol("a", 1)
fstSymbols.add_symbol("c", 2)
fstSymbols.add_symbol("d", 3)
fstSymbols.add_symbol("e", 4)
fstSymbols.add_symbol("F", 5)
fstSymbols.add_symbol("h", 6)
fstSymbols.add_symbol("H", 7)
fstSymbols.add_symbol("i", 8)
fstSymbols.add_symbol("k", 9)
fstSymbols.add_symbol("l", 10)
fstSymbols.add_symbol("m", 11)
fstSymbols.add_symbol("n", 12)
fstSymbols.add_symbol("o", 13)
fstSymbols.add_symbol("p", 14)
fstSymbols.add_symbol("q", 15)
fstSymbols.add_symbol("r", 16)
fstSymbols.add_symbol("s", 17)
fstSymbols.add_symbol("t", 18)
fstSymbols.add_symbol("u", 19)
fstSymbols.add_symbol("x", 20)
fstSymbols.add_symbol("^", 21)
fstSymbols.add_symbol("'", 22)
fstSymbols.add_symbol("l-", 23)
fstSymbols.add_symbol("-k", 24)
fstSymbols.add_symbol("-p", 25)
fstSymbols.add_symbol("-d", 26)
fstSymbols.add_symbol("-u", 27)
fstSymbols.add_symbol("-a", 28)
fstSymbols.add_symbol("-m", 29)
fstSymbols.add_symbol("-e", 30)
fstSymbols.add_symbol("-o", 31)
fstSymbols.add_symbol("-THEME.PFV.IMPROSP", 32)
fstSymbols.add_symbol("-INF", 33)
fstSymbols.add_symbol("cook", 34)
fstSymbols.add_symbol("-IPFV", 35)
fstSymbols.add_symbol("-HABIT", 36)
fstSymbols.add_symbol(".NEG", 37)
fstSymbols.add_symbol("-PFV.PROSP", 38)
fstSymbols.add_symbol("-POT", 39)
fstSymbols.add_symbol("-FUT", 40)
fstSymbols.add_symbol("-FUT.NEG", 41)
fstSymbols.add_symbol("-ADVERSATIVE", 42)
fstSymbols.add_symbol("-DESIDERATIVE", 43)
fstSymbols.add_symbol("-IMP.NEG", 44)
fstSymbols.add_symbol("-IMP", 45)
fstSymbols.add_symbol("-INF", 46)
fstSymbols.add_symbol("-PURPOSIVE", 47)
fstSymbols.add_symbol("-THEME.MID", 48)
fstSymbols.add_symbol("-THEME.PFV-IMPROSP", 49)
fstSymbols.add_symbol("-ANTERIOR", 50)
fstSymbols.add_symbol(".MID", 51)
fstSymbols.add_symbol(".IPFV", 52)
fstSymbols.add_symbol("-PFV.PROSP", 53)
fstSymbols.add_symbol("-PFV.IMPROSP", 54)
fstSymbols.add_symbol("-PURPOSE", 55)

#================================================
# Build the transitions of the FSTs
#================================================
# Morpheme Meanings
compiler = fst.Compiler(isymbols=fstSymbols, osymbols=fstSymbols, keep_isymbols=True, keep_osymbols=True)
print("0 1 a <eps>",file=compiler)           # Transition from the start (state 0) to state 1. You get a 'c' and return a 'c'
print("1 2 l cook",file=compiler)          
print("2 3 e <eps>",file=compiler) 
print("3 4 H -IPFV",file=compiler) 
print("4 64 <eps> <eps>",file=compiler) 
print("64",file=compiler) 
print("4 6 k -HABIT",file=compiler)   
print("6 7 e <eps>",file=compiler)   
print("7 8 x <eps>",file=compiler)   
print("8",file=compiler)                 # State 8 is an end state. The FST finished recognizing the word "Al-eH-kex"
print("6 9 u .NEG",file=compiler)
print("9 10 x <eps>",file=compiler)
print("10",file=compiler)                 
print("3 5 F -PFV.PROSP",file=compiler)
print("5",file=compiler)                 
print("4 11 m -POT",file=compiler)
print("11 12 i <eps>",file=compiler)
print("12 13 x <eps>",file=compiler)
print("13",file=compiler)
print("4 14 d -FUT",file=compiler)
print("14 15 a <eps>",file=compiler)
print("15 16 ^ <eps>",file=compiler)
print("16",file=compiler)    
print("4 17 p -FUT.NEG",file=compiler)  
print("17 18 a <eps>",file=compiler) 
print("18",file=compiler)   
print("2 19 a <eps>",file=compiler)
print("19 20 ' <eps>",file=compiler)
print("20 65 <eps> -ADVERSATIVE",file=compiler)
print("65",file=compiler) 
print("20 21 k <eps>",file=compiler)
print("21 61 u -DESIDERATIVE",file=compiler)
print("61 62 x <eps>",file=compiler)
print("62",file=compiler)
print("19 22 r -IMP.NEG",file=compiler)
print("22",file=compiler)
print("2 23 o <eps>",file=compiler)
print("23 24 q <eps>",file=compiler)
print("24 25 F <eps>",file=compiler)
print("25 63 <eps> -IMP",file=compiler)
print("63",file=compiler)
print("25 26 k -INF",file=compiler)
print("26",file=compiler)
print("23 27 F -PURPOSIVE",file=compiler)
print("27",file=compiler)
print("2 28 i <eps>",file=compiler)
print("28 29 ' -THEME.PFV-IMPROSP",file=compiler)
print("29",file=compiler)
print("28 30 F -ANTERIOR",file=compiler)
print("30 31 r <eps>",file=compiler)
print("31 32 u <eps>",file=compiler)
print("32 33 l <eps>",file=compiler)
print("33 34 e <eps>",file=compiler)
print("34",file=compiler)
print("28 35 H -THEME.MID",file=compiler)
print("35 36 r .IPFV",file=compiler)
print("36",file=compiler)
print("36 37 k -HABIT",file=compiler)
print("37 40 u .NEG",file=compiler)
print("40 41 x <eps>",file=compiler)
print("41",file=compiler)
print("37 38 e <eps>",file=compiler)
print("38 39 x <eps>",file=compiler)
print("39",file=compiler)
print("36 42 m -POT",file=compiler)
print("42 43 i <eps>",file=compiler)
print("43 44 x <eps>",file=compiler)
print("44",file=compiler)
print("36 45 d -FUT",file=compiler)
print("45 46 a <eps>",file=compiler)
print("46 47 ^ <eps>",file=compiler)
print("47",file=compiler)
print("36 48 p -FUT.NEG",file=compiler)
print("48 49 a <eps>",file=compiler)
print("49",file=compiler)
print("35 50 n <eps>",file=compiler)
print("50 51 u -INF",file=compiler)
print("51 52 x <eps>",file=compiler)
print("52 53 k <eps>",file=compiler)
print("53",file=compiler)
print("50 54 a -PFV.PROSP",file=compiler)
print("54 55 x <eps>",file=compiler)
print("55",file=compiler)
print("50 56 e -PFV.IMPROSP",file=compiler)
print("56 57 x <eps>",file=compiler)
print("57",file=compiler)
print("50 58 o -PURPOSE",file=compiler)
print("58 59 F <eps>",file=compiler)
print("59 60 x <eps>",file=compiler)
print("60",file=compiler)

# Extra Credit
print("0 64 i i",file=compiler)
print("64 65 c c",file=compiler)
print("65 66 h h",file=compiler)
print("66 67 a a",file=compiler)
print("67 68 k -k",file=compiler)
print("68 69 i i",file=compiler)
print("69 70 ' '",file=compiler)
print("70",file=compiler)
print("68 71 o o",file=compiler)
print("71 72 k k",file=compiler)
print("72",file=compiler)
print("0 73 t t",file=compiler)
print("73 74 s s",file=compiler)
print("74 75 a a",file=compiler)
print("75 76 k -k",file=compiler)
print("76 77 i i",file=compiler)
print("77 78 ' '",file=compiler)
print("78",file=compiler)
print("76 79 o o",file=compiler)
print("79 80 k k",file=compiler)
print("80",file=compiler)


 
morphMeaningFST = compiler.compile()

# Morpheme Boundaries
compiler = fst.Compiler(isymbols=fstSymbols, osymbols=fstSymbols, keep_isymbols=True, keep_osymbols=True)
print("0 1 a a",file=compiler)           # Transition from the start (state 0) to state 1. You get a 'c' and return a 'c'
print("1 2 l l-",file=compiler)          
print("2 3 e e",file=compiler) 
print("3 4 H H",file=compiler)
print("4 64 <eps> <eps>",file=compiler) 
print("64",file=compiler)  
print("4 6 k -k",file=compiler)   
print("6 7 e e",file=compiler)   
print("7 8 x x",file=compiler)   
print("8",file=compiler)                 # State 8 is an end state. The FST finished recognizing the word "Al-eH-kex"
print("6 9 u u",file=compiler)
print("9 10 x x",file=compiler)
print("10",file=compiler)                 
print("3 5 F F",file=compiler)
print("5",file=compiler)                 
print("4 11 m -m",file=compiler)
print("11 12 i i",file=compiler)
print("12 13 x x",file=compiler)
print("13",file=compiler)
print("4 14 d -d",file=compiler)
print("14 15 a a",file=compiler)
print("15 16 ^ ^",file=compiler)
print("16",file=compiler)    
print("4 17 p -p",file=compiler)  
print("17 18 a a",file=compiler) 
print("18",file=compiler)   
print("2 19 a a",file=compiler)
print("19 20 ' '",file=compiler)
print("20 65 <eps> <eps>",file=compiler)
print("65",file=compiler) 
print("20 21 k k",file=compiler)
print("21 61 u u",file=compiler)
print("61 62 x x",file=compiler)
print("62",file=compiler)
print("19 22 r r",file=compiler)
print("22",file=compiler)
print("2 23 o o",file=compiler)
print("23 24 q q",file=compiler)
print("24 25 F F",file=compiler)
print("25",file=compiler)
print("25 26 k k",file=compiler)
print("26",file=compiler)
print("23 27 F F",file=compiler)
print("27",file=compiler)
print("2 28 i i",file=compiler)
print("28 29 ' '",file=compiler)
print("29",file=compiler)
print("28 30 F F",file=compiler)
print("30 31 r r",file=compiler)
print("31 32 u u",file=compiler)
print("32 33 l l",file=compiler)
print("33 34 e e",file=compiler)
print("34",file=compiler)
print("28 35 H H",file=compiler)
print("35 36 r r",file=compiler)
print("36",file=compiler)
print("36 37 k -k",file=compiler)
print("37 40 u u",file=compiler)
print("40 41 x x",file=compiler)
print("41",file=compiler)
print("37 38 e e",file=compiler)
print("38 39 x x",file=compiler)
print("39",file=compiler)
print("36 42 m -m",file=compiler)
print("42 43 i i",file=compiler)
print("43 44 x x",file=compiler)
print("44",file=compiler)
print("36 45 d -d",file=compiler)
print("45 46 a a",file=compiler)
print("46 47 ^ ^",file=compiler)
print("47",file=compiler)
print("36 48 p -p",file=compiler)
print("48 49 a a",file=compiler)
print("49",file=compiler)
print("35 50 n n",file=compiler)
print("50 51 u -u",file=compiler)
print("51 52 x x",file=compiler)
print("52 53 k k",file=compiler)
print("53",file=compiler)
print("50 54 a -a",file=compiler)
print("54 55 x x",file=compiler)
print("55",file=compiler)
print("50 56 e -e",file=compiler)
print("56 57 x x",file=compiler)
print("57",file=compiler)
print("50 58 o -o",file=compiler)
print("58 59 F F",file=compiler)
print("59 60 x x",file=compiler)
print("60",file=compiler)

# Extra Credit
print("0 64 i <eps>",file=compiler)
print("64 65 c <eps>",file=compiler)
print("65 66 h <eps>",file=compiler)
print("66 67 a cook",file=compiler)
print("67 68 k <eps>",file=compiler)
print("68 69 i -THEME.PFV.IMPROSP",file=compiler)
print("69 70 ' <eps>",file=compiler)
print("70",file=compiler)
print("68 71 o -INF",file=compiler)
print("71 72 k <eps>",file=compiler)
print("72",file=compiler)
print("0 73 t <eps>",file=compiler)
print("73 74 s <eps>",file=compiler)
print("74 75 a cook",file=compiler)
print("75 76 k <eps>",file=compiler)
print("76 77 i -THEME.PFV.IMPROSP",file=compiler)
print("77 78 ' <eps>",file=compiler)
print("78",file=compiler)
print("76 79 o -INF",file=compiler)
print("79 80 k <eps>",file=compiler)
print("80",file=compiler)

morphSplitFST = compiler.compile()

#================================================
# Listen to users
#================================================

print("\nWhich word do you want to analyze?")
print("Enter the word and press ENTER: ", end = " ")
inputWord = input()

wordMorphemes = spellout(inputWord, fstSymbols, morphMeaningFST)
splitWord = spellout(inputWord, fstSymbols, morphSplitFST)
if (splitWord == None or wordMorphemes == None):
    print("Input is invalid. Please enter valid Bribri word.")
print("\nYour word:               " + inputWord)
print("Word split in morphemes: " + splitWord)
print("Meaning of morphemes:    " + wordMorphemes)

#================================================
# Draw the FST transitions
#================================================

morphMeaningFST.draw("exampleMeaning.gv")
render('dot','pdf','exampleMeaning.gv')

morphSplitFST.draw("exampleSplit.gv")
render('dot','pdf','exampleSplit.gv')

print("\nA graphical representation of your\nFST was saved in the files exampleMeaning.gv.pdf and exampleSplit.gv.pdf\n")
