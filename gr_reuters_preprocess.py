# script_name: gr_reuters_preprocess.py
# this script is part of gender recognition project, and used to extract all articles with respective authors,
# disregard all articles without body, author name or with multiple authors


import os
import sys
from bs4 import BeautifulSoup

def parse(varFileToParse):

    #TODO: parse file line by line, tags: reuters, author, body......

    # output file name and variables
    varOutputName="preprocess_output.dat"
    _varBufferFile = open(varOutputName, 'a')
    varOutputAuthors="outputAuthors.dat"
    _varBufferAuthors = open(varOutputAuthors, 'a')
    
    # we add root node to the output
    #_varBufferFile.write("<ROOT>\n")
    varStringToWrite = "<FILE : {} >\n".format(varFileToParse)
    _varBufferFile.write(varStringToWrite)


    # articles begin and end tags 
    varReutersBeginTag="<REUTERS"
    varReutersEndTag="</REUTERS>\n"
    
    # some other variables
    varStart = False
    _varArticleStart = False
    _varArticles = ""
    varArticlesCounter = 0

    # open file line by line, and send everything between two reuters tags to beautiful soup
    # then soup extracts author and body, if author present, write to output
    with open(varFileToParse, 'rb') as f:
        for varLineBinary in f:
            varLine = varLineBinary.decode('us-ascii')
           
            if (not varStart):
                if (varLine.startswith(varReutersBeginTag)):
                    varStart=True
                    _varArticles = _varArticles + varLine

            if (varStart):
                if (varLine.endswith(varReutersEndTag)):
                    varStart=False
                    _varArticles = _varArticles + varLine
                    
                    # now we process the article and write to file                
                  
                    varSoup = BeautifulSoup(_varArticles, "xml")
                    varBodyTag = varSoup.BODY
                    varAuthorTag = varSoup.AUTHOR
                    
                    if ( (repr(varBodyTag)=="None") or (repr(varAuthorTag)=="None") ):
                        # we are not interested in articles without body or author
                        pass
                    else:
                        #write author
                        _varBufferFile.write(repr(varAuthorTag))
                        _varBufferFile.write("\n")
                        # write author to aux file with authors only
                        _varBufferAuthors.write(repr(varAuthorTag))
                        _varBufferAuthors.write("\n")
                        #write article text
                        _varBufferFile.write(repr(varBodyTag))
                        _varBufferFile.write("\n")
                        # count articles
                        varArticlesCounter = varArticlesCounter + 1

                    _varArticles=""

                else:
                    _varArticles = _varArticles + varLine

    # we close buffer files...
    _varBufferFile.close()
    _varBufferAuthors.close()
       
parse("/data/reuters/reut2-001.sgm")
parse("/data/reuters/reut2-013.sgm")
parse("/data/reuters/reut2-011.sgm")
parse("/data/reuters/reut2-006.sgm")
parse("/data/reuters/reut2-016.sgm")
parse("/data/reuters/reut2-021.sgm")
parse("/data/reuters/reut2-010.sgm")
parse("/data/reuters/reut2-017.sgm")
parse("/data/reuters/reut2-008.sgm")
parse("/data/reuters/reut2-009.sgm")
parse("/data/reuters/reut2-014.sgm")
parse("/data/reuters/reut2-007.sgm")
parse("/data/reuters/reut2-020.sgm")
parse("/data/reuters/reut2-004.sgm")
parse("/data/reuters/reut2-005.sgm")
parse("/data/reuters/reut2-012.sgm")
parse("/data/reuters/reut2-003.sgm")
parse("/data/reuters/reut2-019.sgm")
parse("/data/reuters/reut2-015.sgm")
parse("/data/reuters/reut2-000.sgm")
parse("/data/reuters/reut2-002.sgm")
parse("/data/reuters/reut2-018.sgm")

# next line uncomment if you want to use test_data
#parse("data/reuters/reut_test.sgm")
