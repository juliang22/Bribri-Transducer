#==============================================================
# Dartmouth College, LING28, Winter 2020
# Rolando Coto-Solano (Rolando.A.Coto.Solano@dartmouth.edu)
# Examples for Homework 2: Finite State Transductors
#
# This program uses the openfst and graphviz packages:
# http://www.openfst.org/twiki/bin/view/FST/PythonExtension
# https://graphviz.readthedocs.io/en/stable/manual.html
#
# In this small example, you will see a transductor that
# reads English words and decomposes them morphologically
# For example:
#     cats   -> cat-PL
#     dogs   -> dog-PL
#     cities -> city-PL
#
# This program has four parts:
#
# (1) First, we have the fstSymbols. This is the
#     list of all of the elements you are going
#     to have in the FST. (Practical advice: Make
#     your transitions first, and THEN figure out
#     the symbols as you go).
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
# the FST processing. You do NOT need to
# modify them.
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
# You need to modify the list below to match
# the symbols you need. My advice would be:
# (1) Draw the lattice on a piece of paper,
# (2) Make a list of the transitions, and
# (3) As you go through the transitions, 
#     include your symbolss in the symbol
#     list.
#
# Notice that the first symbol is the 
# "epsilon", for when you expect empty strings.
#================================================

fstSymbols = fst.SymbolTable()
fstSymbols.add_symbol("<eps>", 0)
fstSymbols.add_symbol("c", 1)
fstSymbols.add_symbol("a", 2)
fstSymbols.add_symbol("t", 3)
fstSymbols.add_symbol("s", 4)
fstSymbols.add_symbol("-PL", 5)
fstSymbols.add_symbol("i", 6)
fstSymbols.add_symbol("e", 7)
fstSymbols.add_symbol("y-PL", 8)
fstSymbols.add_symbol("d", 9)
fstSymbols.add_symbol("o", 10)
fstSymbols.add_symbol("g", 11)
fstSymbols.add_symbol("y", 12)
fstSymbols.add_symbol("u", 13)
fstSymbols.add_symbol("-s", 14)
fstSymbols.add_symbol("-ies", 15)

#================================================
# Build the transitions of the FSTs
# You need to modify the list below. This is
# where you would put the transitions and the
# end states of your FST.
#================================================
	
# You do *not* need to comment every line. I put the comments below to
# make the program clearer, but you do not need to comment in such detail.
compiler = fst.Compiler(isymbols=fstSymbols, osymbols=fstSymbols, keep_isymbols=True, keep_osymbols=True)
print("0 1 c c",file=compiler)           # Transition from the start (state 0) to state 1. You get a 'c' and return a 'c'
print("1 2 a a",file=compiler)           # Transition from state 1 to state 2. You get an 'a' and return an 'a'
print("2 3 t t",file=compiler)           # Transition from state 2 to state 3. You get a 't' and return a 't'
print("3 4 <eps> <eps>",file=compiler)   # Transition from state 3 to state 4. You get an epsilon and return an epsilon.
print("4",file=compiler)                 # State 4 is an end state. The FST finished recognizing the word "cat"
print("3 5 s -PL",file=compiler)         # Transition from state 3 to state 5. You get an 's' and return "-PL"
print("5",file=compiler)                 # State 5 is an end state. The FST finished recognizing the word "cats"
print("1 6 i i",file=compiler)           # Transition from state 1 to state 6. You get an 'i' and return an 'i'
print("6 7 t t",file=compiler)           # Transition from state 6 to state 7. You get a 't' and return a 't'
print("7 8 y y",file=compiler)           # Transition from state 7 to state 8. You get a 'y' and return a 'y'
print("8",file=compiler)                 # State 8 is an end state. The FST finished recognizing the word "city"
print("7 9 i <eps>",file=compiler)       # Transition from state 7 to state 9. You get an 'i' and return an epsilon.
print("9 10 e <eps>",file=compiler)      # Transition from state 9 to state 10. You get an 'e' and return an epsilon.
print("10 11 s y-PL",file=compiler)      # Transition from state 10 to state 11. You get an 's' and return "y-PL"
print("11",file=compiler)                # State 11 is an end state. The FST finished recognizing the word "cities"
print("0 12 d d",file=compiler)          # Transition from state 0 to state 12. You get a 'd' and return a 'd'
print("12 13 o o",file=compiler)         # Transition from state 12 to state 13. You get an 'o' and return an 'o'
print("13 14 g g",file=compiler)         # Transition from state 13 to state 14. You get a 'g' and return a 'g'
print("14 15 <eps> <eps>",file=compiler) # Transition from state 14 to state 15. You get an epsilon and return an epsilon
print("15",file=compiler)                # State 15 is an end state. The FST finished recognizing the word "dog"
print("14 16 s -PL",file=compiler)       # Transition from state 14 to state 16. you get an 's' and return "-PL"
print("16",file=compiler)                # State 16 is an end state. The FST finished recognizing the word "dogs"

morphMeaningFST = compiler.compile()


compiler = fst.Compiler(isymbols=fstSymbols, osymbols=fstSymbols, keep_isymbols=True, keep_osymbols=True)
print("0 1 c c",file=compiler)
print("1 2 a a",file=compiler)
print("2 3 t t",file=compiler)
print("3 4 <eps> <eps>",file=compiler)
print("4",file=compiler)
print("3 5 s -s",file=compiler)
print("5",file=compiler)
print("1 6 i i",file=compiler)
print("6 7 t t",file=compiler)
print("7 8 y y",file=compiler)
print("8",file=compiler)
print("7 9 i <eps>",file=compiler)
print("9 10 e <eps>",file=compiler)
print("10 11 s -ies",file=compiler)
print("11",file=compiler)
print("0 12 d d",file=compiler)
print("12 13 o o",file=compiler)
print("13 14 g g",file=compiler)
print("14 15 <eps> <eps>",file=compiler)
print("15",file=compiler)
print("14 16 s -s",file=compiler)
print("16",file=compiler) 

morphSplitFST = compiler.compile()

#================================================
# Listen to users
#================================================

print("\nWhich word do you want to analyze?")
print("Enter the word and press ENTER: ", end = " ")
inputWord = input()

wordMorphemes = spellout(inputWord, fstSymbols, morphMeaningFST)
splitWord = spellout(inputWord, fstSymbols, morphSplitFST)
print("\nYour word:               " + inputWord)
print("Word split in morphemes: " + splitWord)
print("Meaning of morphemes:    " + wordMorphemes)

#================================================
# The following are examples for you to see the
# instructions involved in the morphological
# analysis. You can uncomment each block to see
# how it behaves.
#================================================

#word = "cats"
#wordMorphemes = spellout(word, fstSymbols, morphMeaningFST)
#splitWord = spellout(word, fstSymbols, morphSplitFST)
#print(word)
#print(splitWord)
#print(wordMorphemes)

#word = "dogs"
#wordMorphemes = spellout(word, fstSymbols, morphMeaningFST)
#splitWord = spellout(word, fstSymbols, morphSplitFST)
#print(word)
#print(splitWord)
#print(wordMorphemes)

#word = "cities"
#wordMorphemes = spellout(word, fstSymbols, morphMeaningFST)
#splitWord = spellout(word, fstSymbols, morphSplitFST)
#print(word)
#print(splitWord)
#print(wordMorphemes)

print("")
print("----- This is the set of transitions -----")
print(morphMeaningFST)
print("------------------------------------------")


#================================================
# Draw the FST transitions
#================================================

morphMeaningFST.draw("morphs.gv")
render('dot','pdf','morphs.gv')

print("\nA graphical representation of your\nFST was saved in morphs.gv.pdf\n")
