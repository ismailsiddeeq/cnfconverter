# CNF converter 2020
# Made by Ismail Siddeeq

converter.py converts any propositional logic sentence into its equivalent CNF sentence.



INPUT:
Takes a file with propositonal logic formulas in the form of a lists on each line
First line MUST be integer to read file properly.
EXAMPLE formula as list:['IFF', ['NOT', 'C'], 'B'] which would be read as NOT C IFF B in regular syntax for proposotional logic

OUTPUT:
Output will automatically be transferred into a new .txt file by the name "Input_TO_CNF", and it will be outputted on seperate lines.
EXAMPLE OUTPUT LINE: ['AND', ['OR', 'B', 'C'], ['OR', ['NOT', 'C'], ['NOT', 'B']]] which would be read as (B OR C) AND (NOT C OR NOT B) in regular syntax for proposotional logic

IMPORTANT NOTES:
-In order to run the program, you must use this command in terminal: python converter.py –i inputfilename (ie. ourCASES.txt input file will be covnerted into Input_TO_CNF.txt)
-Propositional Logic Formula MUST be inputted in the format listed above, or else it will not run
-Must not call a OR, AND, IMP, etc to an Empty list or it will return error because empty cannot convert to anything
-ourCASES.txt is personal tests that range through atleast one case of each IFF, IMP, AND, NOT, and OR.
-All other test cases MUST be in eligible format listed above or it will give error

 


