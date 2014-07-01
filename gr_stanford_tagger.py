from __future__ import division
import nltk
import os
import sys

path_to_model = os.path.abspath("../Users/Ivo/Desktop/stanford-postagger-2014-01-04/models/english-bidirectional-distsim.tagger")
path_to_jar = os.path.abspath("../Users/Ivo/Desktop/stanford-postagger-2014-01-04/stanford-postagger.jar")
path_to_java = os.path.abspath("../Program Files/Java/jdk1.8.0_05/bin/java.exe")
nltk.internals.config_java(path_to_java, ["-Xmx1024m"])
tagger = nltk.tag.stanford.POSTagger(path_to_model, path_to_jar)

#tokens = nltk.tokenize.word_tokenize("This is a test.")
#tmp = tagger.tag(tokens)
#print (tmp)

def parse(varFileToParse):
    
    varOutputName="tmp/blog_gender_dataset_tagged.dat"
    # _varBufferFile = open(varOutputName, 'a')
    
    # articles begin and end tags 
    varGenderTag = "<"
    
    # some other variables
    varStart = False
    _varArticles = ""
    _varCurrentArticle = ""
    _varI = 0
    
    with open(varFileToParse, 'rb') as f:
        varNumLines = len(f.readlines())
    
    print varNumLines
    varCurrentLineNum = 0
    
    with open(varFileToParse, 'rb') as f:
        for varLineBinary in f:
            if(varCurrentLineNum % 228 == 0):
                print ((varCurrentLineNum / varNumLines) * 100.0)
            varCurrentLineNum += 1
            
            varLine = varLineBinary.decode('UTF-8')
            
            # print varLine
            
            if (varLine.startswith(varGenderTag)):
                try:
                    varLine = varLine[1:2]
                    # print varLine
                    tokens = nltk.tokenize.word_tokenize(_varCurrentArticle)
                    tagged = tagger.tag(tokens)
                    _varArticles += varLine + "\n" + str(tagged) + "\n"
                    _varCurrentArticle = ""
                    # break
                    continue
                except:
                    _varCurrentArticle = ""
                    pass
            _varCurrentArticle += varLine
            
    _varBufferFile = open(varOutputName, 'a')
    _varBufferFile.write(_varArticles)
    _varBufferFile.close()

parse("tmp/blog-gender-dataset.csv")
