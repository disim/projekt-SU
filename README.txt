This project is composed of several python scripts.

First we have raw data as found online, from two sources:

1) reuters-21578 data corpus - there are 21 files, named
reut02-000.sgm,...reurt02-021.sgm
we use gr_reuters_preprocess.py script to parse all articles
with author name, author body and just one author, from all incoming files,
and output is file named "preprocess_output.dat"

2) blog_gender data corpus - there was one xlsx (blog-gender-dataset.xlsx)
file which we converted to blog-gender-dataset.csv and run stanford_tagger
on this data

Next step is to run gr_stanford_tagger.py on blog-gender-dataset.csv and preprocess_output.dat
which is used to tag all words with tags such as "NN" for "noun" etc....

Now we use two almost identical scripts, (difference in file names and function calls)
to extract features from both datasets gr_reuters_preprocess.py, and gr_blog_preprocess.py
Output  of these scripts is one file, blog+features.arff, which contains feature vectors
for all articles.

After this is done, blog+features.arff is provided to weka via GUI


We used two libraries in this project, one is beautifulSoup, which is XML parser, and we used it
in our gr_reuters_preprocess.py script to extract authors and articles from original .sgm files
It can be obtained from link:
https://pypi.python.org/pypi/beautifulsoup4/4.3.2
And last, we used nltk, Natural Language Toolkit, which provided necessary stanford_tagger
http://www.nltk.org/
