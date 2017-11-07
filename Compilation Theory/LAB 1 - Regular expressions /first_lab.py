from __future__ import print_function
import os
import sys
import re
import codecs


def processFile(filepath):
    fp = codecs.open(filepath, 'rU', 'iso-8859-2')

    content = fp.read()
    
    totalNumberOfEmails = 0
    totalNumberOfDates = 0
    totalNumberOfFloats = 0
    totalNumberOfIntegers = 0
    totalNumberOfAbbreviations = 0
    totalNumberOfSentences = 0 
    authorName = ""
    keywords = ""
    
    for emailResult in re.finditer(r'[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}', content):
        #print(emailResult.group())
        totalNumberOfEmails += 1

    for text in re.finditer(r'<P>(.*?)<\/P>', content, re.M | re.DOTALL):
        #rrrr-dd-mm or rrrr/dd/mm or rrrr.dd.mm
        for dateResult in re.finditer(r'([12]\d{3}[-./](0[1-9]|[12]\d|3[01])[-./](0[1-9]|1[0-2]))', text.group(1)):
            #print(dateResult.group())
            totalNumberOfDates += 1
        #dd-mm-rrrr or dd/mm/rrrr or dd.mm.rrrr
        for dateResult in re.finditer(r'((0[1-9]|[12]\d|3[01])[-./](0[1-9]|1[0-2])[-./][12]\d{3})', text.group(1)):
            #print(dateResult.group())
            totalNumberOfDates += 1
        for floatResult in re.finditer(r'[-+]?[0-9]*\.[0-9]+([eE][-+]?[0-9]+)?', text.group(1), re.DOTALL):
            #print(floatResult.group())
            totalNumberOfFloats += 1
        for abbreviationResult in re.finditer(r'\s([A-Za-z]{1,3}[.])', text.group(1)):
            #print(abbreviationResult.group())
            totalNumberOfAbbreviations += 1
        for integerResult in re.finditer(r'([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])', text.group(1)):
            #print(integerResult.group())
            totalNumberOfIntegers += 1
        for sentencesResult in re.finditer(r'([A-Z][^\.!?]*[\.!?])', text.group(1), re.DOTALL | re.M):
            #print(sentencesResult.group())
            totalNumberOfSentences += 1


    authorResult = re.search(r'<META NAME="AUTOR" CONTENT="(\w+\s+\w+)">', content)
    if authorResult:
        #print(authorResult.group(1))
        authorName = authorResult.group(1)
    
    for keywordResult in re.finditer(r'<META NAME="(\w+)"', content):
        #print(keywordResult.group(1))
        keywords += " " + keywordResult.group(1)

    fp.close()
    print("filename:", filepath)
    print("author:", authorName)
    print("keywords:", keywords)
    print("number of sentences:", totalNumberOfSentences)
    print("number of abbreviations:", totalNumberOfAbbreviations)
    print("number of integer numbers:", totalNumberOfIntegers)
    print("number of float number:", totalNumberOfFloats)
    print("number of dates:", totalNumberOfDates)
    print("number of email addresses:", totalNumberOfEmails)
    print("\n")


try:
    path = sys.argv[1]
except IndexError:
    print("Catalogue name is missing")
    sys.exit(0)


tree = os.walk(path)

for root, dirs, files in tree:
    for f in files:
        if f.endswith(".html"):
            filepath = os.path.join(root, f)
            processFile(filepath)
