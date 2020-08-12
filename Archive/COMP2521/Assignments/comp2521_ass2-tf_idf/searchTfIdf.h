// interface to use tfidf
#include "set.h"
#include "BSTree.h"
#include "readData.h"
#include "simpleList.h"
#define START_FREQUENCY 1
#define MAX_OUTPUT 30

#ifndef SEARCHTFIDF_H
#define SEARCHTFIDF_H

Set findWords(Set allWords, Set searchWords);
Set getWords(Set invertedIndex);
Set invertedIndex(void);
Set correspondingURLs(char *searchWord);
float calculateTF(Set matchingURLs, char *searchWord);
float calculateIDF(Set matchingURLs);
SList returnTFIDFs(Set searchWords);


#endif
