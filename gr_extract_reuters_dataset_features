# script_name: gr_extract_blog_dataset_features.py
# this script is part of gender recognition project, and used to extract features
# from reuters dataset, which was prior to this passed through stanford_tagger

from __future__ import division
import os
import sys
import re

# input and output file names
varOutputName="data/reuters_gender_features.arff"
varInputName="data/reuters_gender_tagged.dat"

# buffer variable used to write to file
_varBufferFile = open(varOutputName, 'w')

# some function word features
varPronounWords = "all, his, most, other, that, what, your, another, i, much, any, it, them, which, few, \
its, he, these, who, her, little, she, they, many, some, this, me, those, him, one, us, more, something, we, you"
varAuxiliaryVerbs = "are, can, didn't, do, 've, was, 'll, can't, don't, has, is, would, 're, \
could, does, were, be, 's, been, did, had, have, may, should, will"
varConjunctionWords = "and, or, though, because, so, when, if, while"
varInterjectionWords = "well, great, now"
varAdpositionWords = "down, of, through, about, at, off, on, after, before, for, out, from, in, over, \
like, up, into, around, but, with, as, by, next, since, than"

# psycho-linguistic cues
varNegations = ("varNegations", set(['no', 'not', 'never']))
varPositive_emotion = ("varPositive_emotion", set([ 'love', 'nice', 'sweet' ]))
varInsight = ("varInsight", set([ 'think', 'know', 'consider' ]))
varTentative = ("varTentative", set([ 'maybe', 'perhaps', 'guess' ]))
varCertainty = ("varCertainty", set([ 'always', 'never' ]))

varPsychoCuesList = [varNegations, varPositive_emotion, varInsight, varTentative, varCertainty]
varPsychoCues = ["varNegations", "varPositive_emotion", "varInsight", "varTentative", "varCertainty"]

# first we write attributes for weka (our features)
varFeatures = {"F1":0, "F2":0, "F3":0, "F4":0, "F5":0, "F6":0, "F7":0, "F8":0, "F9":0,
               "CC":0, "CD":0, "DT":0, "EX":0, "FW":0, "IN":0, "JJ":0, "JJR":0,
               "JJS":0, "MD":0, "NN":0, "NNP":0, "NNPS":0, "NNS":0,
               "PDT":0, "POS":0, "PRP":0, "PRP$":0, "RB":0, "RBR":0,
               "RP":0, "TO":0, "VB":0, "VBD":0, "VBG":0,
               "VBN":0, "VBP":0, "VBZ":0, "WDT":0, "WP":0, "WRB":0, 
               "''":0, "(":0, ")":0, ",":0, ".":0, ":":0, "``":0}

# here we add number of PronounWords, AuxiliaryVerbs, ConjunctionWords, InterjectionWords, AdpositionWords to feature list
varFeaturesList = varPronounWords.split(", ") + varConjunctionWords.split(", ") + varInterjectionWords.split(", ") + varAdpositionWords.split(", ") + varAuxiliaryVerbs.split(", ") + varPsychoCues
for feature in varFeaturesList: 
    varFeatures [feature.strip()] = 0

_varBufferFile.write("@relation texts.gender\n\n")

# we print attribute list to output for weka
for key in sorted(varFeatures.keys()):
    if(key == "#"):
        varString = "@attribute hash real\n"
    elif(key == "$"):
        varString = "@attribute dollar real\n"
    elif(key == "''"):
        varString = "@attribute aposapos real\n"
    elif(key == "("):
        varString = "@attribute openparen real\n"
    elif(key == ")"):
        varString = "@attribute closeparen real\n"
    elif(key == ","):
        varString = "@attribute comma real\n"
    elif(key == "."):
        varString = "@attribute period real\n"
    elif(key == ":"):
        varString = "@attribute colon real\n"
    elif(key == "``"):
        varString = "@attribute backtbackt real\n"
    else:
        varString = "@attribute " + key.replace(" ", "_").replace("'", "APOS").replace(",", "COMMA") + " real\n"
    _varBufferFile.write(varString)
_varBufferFile.write("@attribute gender {f, m}\n\n@data\n")

with open(varInputName, 'rb') as Articles :
    for varLineBinary in Articles:
            
        
        # next line resets all feature values to 0
        varFeatures = dict.fromkeys(varFeatures, 0)
        #print (varFeatures)
        varWordLen = []
        varWordsSet = set ()

        varLine = varLineBinary.decode('UTF-8')
        
        if (varLine.startswith("f") or varLine.startswith("m") ):
            varGender=varLine[0]
            #print(varLine[0])
        else:
            varLine = varLine.strip()
            varLine = varLine[2:-4]
            varTagged = varLine.split("), (")
            
            for i in range(len(varTagged)):
            # for varPair in varTagged:
                varPair = varTagged[i]
                varWordTagPair = varPair.split(", ")
                varNextWordTagPair = None
                varNextWord = None
                if (i < len(varTagged)-1):
                    varNextWordTagPair = varTagged[i+1].split(", ")
                    varNextWord = varNextWordTagPair[0]
                    varNextWord = varNextWord[1:-1]
                else:
                    varNextWord = ""
                try:
                    varWord = varWordTagPair[0]
                    varTag = varWordTagPair[1]
                    varWord = varWord[1:-1]
                    varTag = varTag[1:-1]
                    #print varTag
                    if(varTag != "#" and varTag != "$" and varTag != "WP$" and varTag != "UH" and varTag != "SYM" and varTag != "RBS" and varTag != "LS"):
                        varFeatures[varTag] += 1
                    #print (varWord)
                    
                    # check f1 - char count
                    varFeatures ["F1"] += len(varWord)
                    
                    # f2 - number of letters a-z 
                    if (re.findall("[a-z]", varWord)):
                        varFeatures ["F2"] += len(re.findall("[a-z]", varWord)) 
                    
                    # f3 - number of letters A-Z
                    if (re.findall("[A-Z]", varWord)):
                        varFeatures ["F3"] += len(re.findall("[A-Z]", varWord))
                        #print string1 + " contains a character other than A-Z"
                    
                    # f4 - number of digits 0-9
                    if (re.findall("[0-9]", varWord)):
                        varFeatures ["F4"] += len(re.findall("[0-9]", varWord))
                        #print string1 + " contains a character other than A-Z"
                    
                    # f5 - total number of words longer than 6 chars
                    if (len(varWord) > 6):
                       varFeatures ["F5"] += 1 
                    
                    # f6 - total number of words (word has three upper cases as tag)
                    # f7 - average word length
                    # f8 - number of short words -> 1-3 characters
                    if (re.findall("[A-Z]", varTag)):
                       varFeatures ["F6"] += 1 
                       varWordLen.append(len(varWord) - 2)
                       if (len(varWord) - 2 < 4):
                            varFeatures ["F8"] += 1
                    
                    # f9 - number of distinct words in article
                    varWordsSet.add(varWord)

                    # features number of PronounWords, AuxiliaryVerbs, ConjunctionWords, InterjectionWords, AdpositionWords etc..
                    for key in varFeatures.keys():
                        if (varWord.lower() == key ):
                            varFeatures [key] += 1
                        if (varWord.lower() + varNextWord.lower() == key):
                            varFeatures [key] += 1


                    # number of psycho cues
                    varTmpWord = varWord.lower()
                    for cue in varPsychoCuesList:
                        if (varTmpWord in cue [1]):
                            varFeatures [cue [0]] += 1

                    #sys.exit()
                    #print varTag
                    
                except:
                    pass
                
                
                
            # f7 - now we calculate average of word lenght 
            varWordLenSum = 0
            for varLen in varWordLen:
                varWordLenSum += varLen
            varFeatures ["F7"] = ( (varWordLenSum * 4.0) / len(varWordLen) )

            # f9 - we count different words ( case sensitive )
            varFeatures ["F9"] = len(varWordsSet)

            
            # print (varFeatures)    
            # sys.exit()

            # we write result to output file
            varString = ""
            for key in sorted(varFeatures.keys()):
                if (key == "F7" or key == "F9"):
                    varString += str(varFeatures[key]) + ","
                else:
                    varString += str( varFeatures[key] / len(varTagged) ) + ","
            varString += varGender + "\n"
            _varBufferFile.write(varString)
            # sys.exit()
            
           

_varBufferFile.close()
