#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <assert.h>
#include "set.h"
#include "graph.h"
#include "queue.h"

#define FALSE 0
#define TRUE 1
#define WANT_URLS 2
#define WANT_TEXT 3
#define TXT_NEEDED 4
#define TXT_NOT_NEEDED 5
#define MAX_CHAR 1000

Set returnSet(int arg, int txt_needed, char *fileName);
Set GetCollection();
Queue getCollection();
Graph GetGraph(Queue collection);
void addURLs(Set URLSet, char *URL);
void addText(Set textSet, char *text);
int toAdd(char *word);
char *addTxtSuffix(char *string);
int endsWithSpecialChar(char *text);
char *normaliseWord(char *text);

// returns a set of urls to process by reading data from file
// collection.txt
Set GetCollection() {
    
    FILE *stream;
    stream = fopen("collection.txt", "r");
    
    if (stream == NULL) {
        fprintf(stderr, "file not found");
        return 0;
    }
    
    char s[MAX_CHAR];
    Set collection = newSet();
    while (fscanf(stream, "%s", s) != EOF) {  
        insertInto(collection, s);
    }
    
    fclose(stream);
    
    return collection;

}

Queue getCollection() {

    FILE *stream;
    stream = fopen("collection.txt", "r");
    
    if (stream == NULL) {
        fprintf(stderr, "file not found");
        return 0;
    }
    
    char s[MAX_CHAR];
    Queue collection = newQueue();
    while (fscanf(stream, "%s", s) != EOF) {  
        enterQueue(collection, s);
    }
    
    fclose(stream);

    return collection;
}

Graph GetGraph(Queue collection) {
  
    Graph URLgraph = newGraph(Queuesize(collection));
    /*
    while (!emptyQueue(collection)) {
        char *url = leaveQueue(collection);
        Set edges = returnSet(WANT_URLS, TXT_NEEDED, url);
        insertEdges(URLgraph, url, edges);
        free(url);
    }
    assert(emptyQueue(collection) == 1);
    */
    return URLgraph;
   

}

// reads a text file and creates two sets - a URL set (set of URLs in ascending order) & a text set (set of all words in section 2 in A-Z order)
//
Set returnSet(int arg, int txt_needed, char *fileName) {
    char *fileName_txt = fileName;
    if (txt_needed == TXT_NEEDED) {
        fileName_txt = addTxtSuffix(fileName);
        //addTxtSuffix(fileName);
    }
    FILE *file = fopen(fileName_txt, "r");
    char string1[MAX_CHAR];
    char string2[MAX_CHAR];
    char *text = string1; 
    char *prev = string1; 
    char *curr = string1;
    int endSection1 = 0;
    Set URLSet = newSet();
    Set textSet = newSet();

    while (fscanf(file, "%s", text) != EOF) {
        curr = text; 
        if (endSection1 == 0) {
            if (strcmp(fileName, curr) != 0) addURLs(URLSet, curr);
        } else { 
            addText(textSet, curr);
            //printf("text %s\n", curr);
        } 
        if (strcmp(curr, "Section-1") == 0 && strcmp(prev, "#end") == 0) {
            fseek(file, strlen("Section-2"), SEEK_CUR);
            endSection1 = 1;
            //printf("FOUND\n");
        }
        strcpy(string2, text);
        prev = string2;
        
    }
    
    fclose(file);
    if (txt_needed == TXT_NEEDED) {
        free(fileName_txt);
    }
 
    
    //printf("URL set is: \n");
    //showSet(URLSet);
    //printf("Text set is: \n");
    //showSet(textSet);
    
 
    if (arg == WANT_URLS) {
        disposeSet(textSet);
        return URLSet;
    } else {
        disposeSet(URLSet);
        return textSet;
    }


}

// helper functions

void addURLs(Set URLSet, char *URL) {
    if (toAdd(URL) == TRUE) {
        insertInto(URLSet, URL); 
    }   
}

void addText(Set textSet, char *text) {
    char string1[MAX_CHAR];
    //char *normalisedWord = string1;
    char *normalisedWord = normaliseWord(text);
    strcpy(string1, normalisedWord);
    free(normalisedWord);
    if (toAdd(text) == TRUE) {      
        insertIntoDuplicates(textSet, string1);
    }     
}

int toAdd(char *word) {
    if (strcmp(word, "#start") == 0 || strcmp(word, "Section-1") == 0 || strcmp(word, "#end") == 0 || strcmp(word, "Section-2") == 0) {
        return FALSE; 
    }
    return TRUE;
}

// adds the .txt suffix to a string
char *addTxtSuffix(char *string) {
    char *suffix = ".txt";
    char *fileName = malloc(strlen(suffix) + strlen(string) + 1);
    strcpy(fileName, string);
    strcat(fileName, suffix);
    return fileName;
}



char *normaliseWord(char *text) {
    char string1[MAX_CHAR];
    char *normalisedWord = string1; 
    //char *finalWord = string1;
    int i = 0;
    
    for (i = 0; text[i] != '\0'; i++) {
            normalisedWord[i] = tolower(text[i]);
    }
    //printf("normalised word is %s\n", normalisedWord);
    if (endsWithSpecialChar(text) == TRUE) {
        normalisedWord[i-1] = '\0';
    } 
    normalisedWord[i] = '\0';
    char *finalWord = malloc(strlen(normalisedWord) + 1);
    strcpy(finalWord, normalisedWord);
    //strcpy(normalisedWord, finalWord);
    //normalisedWord = string1;
    //printf("Final word is %s\n", finalWord);
    
    return finalWord;

}

int endsWithSpecialChar(char *text) {
    if (strlen(text) >= 1 && strcmp(text + strlen(text) -1, ".") == 0) {
        return TRUE;
    } else if (strlen(text) >= 1 && strcmp(text + strlen(text) -1, ";") == 0) {
        return TRUE;
    } else if (strlen(text) >= 1 && strcmp(text + strlen(text) -1, ",") == 0) {
        return TRUE;
    } else if (strlen(text) >= 1 && strcmp(text + strlen(text) -1, "?") == 0) {
        return TRUE;
    }
    
return FALSE;
}
 


