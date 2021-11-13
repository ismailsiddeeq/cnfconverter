import sys #for reading in from command line


def convertCNF(input) :
    if (isinstance(input, str)):
        return input
    elif(isinstance(input,list)) :

        if (input == []) : # empty list
            return input
        # implies
        if (input[0] == 'IMP'):
            return convertCNF(["OR", convertCNF(["NOT",convertCNF(input[1])]), convertCNF(input[2])])
        #if (input[0] == 'IMP') and len(input) <= 2 : check when empty?
      #      return []
        # for if and only if
        elif input[1] == "FALSE" and input[0] == "OR":
            input.remove("FALSE")
            sort(input) #sort to get order correct
            return input
        elif input[1] == "TRUE" and input[0] == "OR":
            input.remove("TRUE")
            sort(input) #sort to get order correct
            return input

        #elif input[1] == "TRUE" and input[0] == "AND": #case of TRUE with AND being the conjunctive
           # input.remove("TRUE")
          #  sort(input) #sort to get order correct
          #  return input
        #elif input[1] == "FALSE" and input[0] == "AND":
         #   return convertCNF(["OR", convertCNF(["NOT",convertCNF(input[1])]), convertCNF(input[2])])   
        #elif input[1] == "TRUE" and input[0] == "IMP":
         #   input.remove("TRUE")
         #   sort(input) #sort to get order correct
        #    return input
        #elif input[1] == "FALSE" and input[0] == "IMP": #redo for false
        #    return convertCNF(["OR", convertCNF(["NOT",convertCNF(input[1])]), convertCNF(input[2])])
        #elif input[1] == "TRUE" and input[0] == "IFF":
        #    input.remove("TRUE")
        #    sort(input) #sort to get order correct
        #    return input
       # elif input[1] == "FALSE" and input[0] == "IFF":
        #    return convertCNF(["OR", convertCNF(["NOT",convertCNF(input[1])]), convertCNF(input[2])])


        elif (input[0] == "NOT"):
            # for not
            if (isinstance(input[1], str)) :
                return input
            # for not not 
            elif (isinstance(input[1], list) and (input[1])[0] == "NOT") :
                return convertCNF((input[1])[1])
            # demorgans
            elif (isinstance(input[1], list) and (input[1])[0] == "AND") :
                disjuncts = []
                for index, item in enumerate(input[1]) :
                    if (index > 0) :
                        disjuncts.append(convertCNF(["NOT", item]))
                disjuncts.insert(0, "OR")
                return convertCNF(disjuncts)
            elif (isinstance(input[1], list) and (input[1])[0] == "OR") :
                conjuncts = []
                for index, item in enumerate(input[1]) :
                    if (index > 0) :
                        conjuncts.append(convertCNF(["NOT", item]))
                conjuncts.insert(0, "AND")
                return convertCNF(conjuncts)
            elif (isinstance(input[1], list) and ((input[1])[0] == 'IMP')) :
                return convertCNF(["AND", convertCNF((input[1])[1]), ["NOT", convertCNF((input[1][2]))]])
            elif (isinstance(input[1], list) and (input[1])[0] == "IFF") :
                return convertCNF(["NOT", convertCNF(input[1])])
        elif (input[0] == "IFF") :
            return convertCNF(["AND", convertCNF(["OR", convertCNF(["NOT", input[1]]), input[2]]), convertCNF(["OR", input[1], convertCNF(["NOT", input[2]])])])
        elif (input[0] == "OR") :
            
            input = sort(input)
            input = removeDups(input)
            
            input = removeOps(input)
            # has to sort after removing because order won't be correct.
            input = sort(input)
            if (len(input) == 1 or 0) :
                return input
            if ((isinstance(input[-1], list) and (input[-1])[0] == "AND")) :
                conjuncts = []
                for i, item in enumerate(input[-1]) :
                    if (i > 0) :
                        conjuncts.append(["OR", input[-2], item])
                conjuncts.insert(0, "AND")
            
                if (len(input) < 4) :
                    return convertCNF(conjuncts)
                else :
                    input.remove(input[-1])
                    input.remove(input[-1])
                input.append(conjuncts)
                return convertCNF(input)
             # a or b
            elif ((isinstance(input[1], str) and isinstance(input[2], str)) or (isinstance(input[1], str) and isinstance(input[2], list) and (input[2])[0] == "NOT" and isinstance((input[2])[1], str)) or (isinstance(input[2], str) and isinstance(input[1], list) and (input[1])[0] == "NOT" and isinstance((input[1])[1], str))) :
                input.append(["OR", input[1], input[2]])
                input.remove(input[1])
                input.remove(input[1])
                
                input = removeOps(input)
                input = sort(input)
                return input
            # not a or not b
            elif (isinstance(input[1], list) and (input[1])[0] == "NOT" and isinstance((input[1])[1], str) and isinstance(input[2], list) and (input[2])[0] == "NOT" and isinstance((input[2])[1], str)) :
                return input
            # For any other operator compute the inner operator after or
            else :
                disjuncts = []
                for i, item in enumerate(input) :
                    if (i > 0) :
                        disjuncts.append(convertCNF(item))
                disjuncts.insert(0, "OR")
                return convertCNF(disjuncts)
            
        elif (input[0] == "AND") :
            
            input = sort(input)
            input = removeDups(input)
            input = removeOps(input)
            input = sort(input)
            if (len(input) == 1) :
                return input
            disjuncts = []
            for i, item in enumerate(input) :
                if (i > 0) :
                    disjuncts.append(convertCNF(item))
            disjuncts.insert(0, "AND")
            disjuncts = removeOps(disjuncts)

            return disjuncts


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# reduces the operators that are repeated unnecesarily 
# example would be ["and", "L","and", "P", ["and", "Q", "R"]] would be the same and easier interpreted written as ["and", "L,","P", "Q", "R"]
def removeOps(input) :
    if (isinstance(input, str)) :
        return input
    operator = input[0] # sees which operator it is
    L = []
    propositions = []
    for index, item in enumerate(input) :
        if (index > 0) :
            if (isinstance(item, str)) :
                L.append(item)
            elif (isinstance(item, list)) :
                propositions.append(removeOps(item))
    newinput = L # create new input to store after repeated operators are gone
    for item in propositions :
        if (isinstance(item, list) and item[0] == operator) :
            for i,j in enumerate(item) :
                if (i > 0) :
                    newinput.append(j)
        else :
            newinput.append(item)
    newinput.insert(0, operator)
    return newinput


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Removes duplicate elements from operators that can be reduced
# ex: ["and", "P", "P"] is just "P"
def removeDups(input) :
    if (isinstance(input, str) or (isinstance(input, list) and input[0] == "NOT" and isinstance(input[1], str))):
        return input    
    for i, checkItem in enumerate(input) :
        if (i > 0) :
            for j, item in reversed(list(enumerate(input))) :
                if (j > i) :
                    if (isinstance(item, list)) :
                        newItem = removeDups(item)
                        input.insert(j, newItem)
                        input.remove(item)
                    if (checkItem == item) :
                        input.remove(item)
    if (isinstance(input, list) and input[0] != "NOT" and len(input) < 3) :
        return input[1]
    return input

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# helper func for removing dups in the list and maintaining correct format
def sort(input) :
    if (isinstance(input, str)) :
        return input
    operator = input[0]
    if (operator == 'IMP') :
        return input
    L = []
    propositions = []
    for index, j in enumerate(input) : #going through formula list
        if (index > 0) :
            if (isinstance(j, str)) :
                L.append(j)
            elif (isinstance(j, list)) :
                propositions.append(sort(j))
    if (len(L) > 0) :
        L.sort()
    if (len(propositions) > 0) :
        propositions = sorted(propositions, key=lambda proposition: proposition[0], reverse=True)
    newinput = L + propositions
    newinput.insert(0, operator)
    return newinput

# convertCNFs to CNF by taking different cases separately
#I believe it covers ALL cases that could be taken into account
# implement FALSE and TRUE 
#If it OR [t]/[f], then can remove, if it AND [t], remove if it AND [f], it comes out F

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

            
#Read the input file 
#based on sys
inputFile = open(sys.argv[2]) #commandline
numSentences = -1
sentences = []

for line in inputFile: # put number on top of .txt file to know lines to go thru
    if (numSentences > 0):
        sentences.append(eval(line.strip()))
    else:
        numSentences = int(line.strip())
outputFile = open('Input_TO_CNF.txt', 'w+') 
# For each sentence convertCNF it to CNF
for sentence in sentences: #loop through lines in file, HAS TO BE INPUTTED AS LIST
    #Use all simplications mentioned in order to maximize efficiency
    input = convertCNF(sentence)
    input = sort(input)
    input = removeDups(input)
    input = removeOps(input)
    input = sort(input)
    outputFile.write (str(input) + '\n')
inputFile.close()
