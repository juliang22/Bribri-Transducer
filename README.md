# Bribri-Transducer
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
