#include <stdio.h> 
#include <string.h>
#include <math.h>
#include "set.h"
#include "BSTree.h"
#include "readData.h"
#include "simpleList.h"

#define START_FREQUENCY 1
#define MAX_OUTPUT 30

Set findWords(Set allWords, Set searchWords);
Set getWords(Set invertedIndex);
Set invertedIndex(void);
Set correspondingURLs(char *searchWord);
float calculateTF(Set matchingURLs, char *searchWord);
double calculateIDF(Set matchingURLs);
SList returnTFIDFs(Set searchWords);


int main (int argc, char **argv) {
    
    char string[MAX_CHAR];
    Set searchWords = newSet();     // set containing all the searchWords a user enters
    char *inputWord = string;
    int i;
    
    for (i = 1; i < argc; i++) {    // creates a set containing all commandline arguments
        strcpy(inputWord, argv[i]);
        insertInto(searchWords, inputWord);
    }
    
    
    SList TFIDFs = returnTFIDFs(searchWords);
    disposeSet(searchWords);
    showSL(TFIDFs, MAX_OUTPUT);
    freeSL(TFIDFs);
    
}


// given a particular search-word that appears in the 'web', returns a Set of corresponding URLs that the word appears in

Set correspondingURLs(char *searchWord) {
    Set matchingURLs = newSet();
    FILE *fp = fopen("invertedIndex.txt", "r");  
    char string1[MAX_CHAR]; 
    char string[MAX_CHAR];
    char string2[MAX_CHAR];
    char *text = string;
    char *url = string2;
    
    while (fgets(string1, sizeof(string1), fp) != NULL) {
        if (sscanf(string1, "%s", text) != EOF) {
            if (strcmp(text, searchWord) == 0) {
                for (url = strtok(string1, " "); url!= NULL; url = strtok(NULL, " ")) {
                    if (strcmp(url, "\n") != 0 && strcmp(url, " ") != 0 && strcmp(url, searchWord) != 0) {
                        insertInto(matchingURLs, url);              
                    }
                }
            }
        }
          
    }
    
    fclose(fp);

return matchingURLs;

}

// for each URL the word is in, read the URL.txt file and count occurence of that search-word
float calculateTF(Set matchingURLs, char *searchWord) {
    Set text = returnSet(WANT_TEXT, TXT_NOT_NEEDED, leaveSet(matchingURLs));
    float totalWords = nElems(text);
    float occurences = frequency(text, searchWord);
    float TF = occurences/totalWords;
    
    disposeSet(text);

    return TF;

}

// calculate inverse document frequency

double calculateIDF(Set matchingURLs) {
    Queue collection = getCollection();
    double totalDocuments = Queuesize(collection);
    double termDocuments = nElems(matchingURLs);
    double ratio = totalDocuments/termDocuments;
    double IDF = log10(ratio);
    disposeQueue(collection);
        
    return IDF;

}

// calculate the product of term frequency and inverse document frequency

float calculateTFIDF(Set matchingURLs, char *searchWord) {

    return calculateTF(matchingURLs, searchWord) * calculateIDF(matchingURLs);
}


// return a linked list of URLs. Each node contains the URL name, the TFIDF value and the frequency

SList returnTFIDFs(Set searchWords) {
    int i;
    Set matchingURLs;
    char *searchWord;
    char *URL;
    int j;
    int frequency = START_FREQUENCY;
    SList TFIDFs = NULL;
    
    for (i = 0; i < nElems(searchWords); i++) {
        searchWord = leaveSet(searchWords);
        matchingURLs = correspondingURLs(searchWord); 
        for (j = 0; j < nElems(matchingURLs); j++) {
            URL = returnFirst(matchingURLs);
            if (inSL(TFIDFs, URL) == TRUE) {                                // if the URL is in the list, we want to change its TFIDF value
                SList elem = returnSLNode(TFIDFs, URL);
                changeValue(elem, calculateTFIDF(matchingURLs, searchWord));
            } else {
                TFIDFs = insertSL(TFIDFs, URL, calculateTFIDF(matchingURLs, searchWord), frequency); 
            }
        }
    }

arrangeList(TFIDFs);    // organise the list to be outputted in specified order
disposeSet(matchingURLs);

return TFIDFs;

}
