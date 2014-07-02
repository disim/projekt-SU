# this script is used to make test_feature_vector for ONE article
# which should be stored in test_data.dat file
from __future__ import division
import nltk
import os
import sys
import re
import subprocess

# some file variables
varInputFileName = "tmp/final2/test_data.dat"
varOutputName = "tmp/final2/test_feature_vector.arff"

# some aux variables for initializing stanford tagger
path_to_model = os.path.abspath("../Users/Ivo/Desktop/stanford-postagger-2014-01-04/models/english-bidirectional-distsim.tagger")
path_to_jar = os.path.abspath("../Users/Ivo/Desktop/stanford-postagger-2014-01-04/stanford-postagger.jar")
path_to_java = os.path.abspath("../Program Files/Java/jdk1.8.0_05/bin/java.exe")
nltk.internals.config_java(path_to_java, ["-Xmx1024m"])
tagger = nltk.tag.stanford.POSTagger(path_to_model, path_to_jar)


##########################################################################################
#                           Functions
##########################################################################################

def stanford_tagger(varFileName):
    
    varArticle = ""
    with open(varFileName, 'rb') as f:
        # read whole article
        for varLineBinary in f:
            varLine = varLineBinary.decode('UTF-8')
            varArticle += varLine
        #print varArticle
        
        varTokens = nltk.tokenize.word_tokenize(varArticle)
        varTagged = tagger.tag(varTokens)
        #print (varTagged)
        
        return (varTagged)

def feature_extractor (varTaggedString):
    _varBufferFile = open(varOutputName, 'w')

    # some features for feature extractor
    # some function word features
    varPronounWords = "all, his, most, other, that, what, your, another, i, much, any, it, them, which, few, its, he, these, who, her, little, she, they, many, some, this, me, those, him, one, us, more, something, we, you"
    varAuxiliaryVerbs = "are, can, didn't, do, 've, was, 'll, can't, don't, has, is, would, 're, could, does, were, be, 's, been, did, had, have, may, should, will"
    varConjunctionWords = "and, or, though, because, so, when, if, while"
    varInterjectionWords = "well, great, now"
    varAdpositionWords = "down, of, through, about, at, off, on, after, before, for, out, from, in, over, like, up, into, around, but, with, as, by, next, since, than"

    # psycho-linguistic cues
    varNegations = ("varNegations", set(['no', 'not', 'never']))
    varPositive_emotion = ("varPositive_emotion", set([ 'love', 'nice', 'sweet' ]))
    varInsight = ("varInsight", set([ 'think', 'know', 'consider' ]))
    varTentative = ("varTentative", set([ 'maybe', 'perhaps', 'guess' ]))
    varCertainty = ("varCertainty", set([ 'always', 'never' ]))

    varPsychoCuesList = [varNegations, varPositive_emotion, varInsight, varTentative, varCertainty]
    varPsychoCues = ["varNegations", "varPositive_emotion", "varInsight", "varTentative", "varCertainty"]

    # Dictionary to which we (later) add features
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


    # next line resets all feature values to 0
    varFeatures = dict.fromkeys(varFeatures, 0)
    #print (varFeatures)
    varWordLen = []
    varWordsSet = set ()
    for varWordTagPair in varTaggedString:
        
        try:
            varWord = varWordTagPair[0]
            varTag = varWordTagPair[1]
            
            #print (varTag)
            #print (varWord)
            #break
            if(varTag != "#" and varTag != "$" and varTag != "WP$" and varTag != "UH" and varTag != "SYM" and varTag != "RBS" and varTag != "LS"):
                try:
                    varFeatures[varTag] += 1
                except:
                    pass
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
               


            # number of psycho cues
            varTmpWord = varWord.lower()
            for cue in varPsychoCuesList:
                if (varTmpWord in cue [1]):
                    varFeatures [cue [0]] += 1

        except:
            raise





    # f7 - now we calculate average of word lenght 
    varWordLenSum = 0
    for varLen in varWordLen:
        varWordLenSum += varLen
    #varFeatures ["F7"] = ( (varWordLenSum * 4.0) / len(varWordLen) )
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
            varString += str( varFeatures[key] / len(varTaggedString) ) + ","
    varString = varString + "f"
    _varBufferFile.write(varString)

    _varBufferFile.close()
    # sys.exit()
     
    return(varString)
  
        
varTaggedString = stanford_tagger(varInputFileName)
varFeatureVector = feature_extractor (varTaggedString)
#print (varFeatureVector)
varCmdCommand = 'java -cp "C:\Program Files\Weka-3-7\weka.jar" weka.classifiers.functions.MultilayerPerceptron -l "tmp\\final2\\model.model" -T tmp\\final2\\test_feature_vector.arff >> tmp\\final2\\prediction.txt '
subprocess.check_call(varCmdCommand, shell=True )
           



