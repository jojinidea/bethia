#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "set.h"
#include "graph.h"


#define FALSE 0
#define TRUE 1
#define WANT_URLS 2
#define WANT_TEXT 3


Set returnSet(int arg, char *fileName);
Set GetCollection();
Graph GetGraph(Set collection);
void addURLs(Set URLSet, char *URL);
void addText(Set textSet, char *text);
int toAdd(char *word);
void addTxtSuffix(char *string);
char *normaliseWord(char *text);
int endsWithSpecialPunctuation(char *text);


// returns a set of urls to process by reading data from file
// collection.txt
Set GetCollection() {
    
    FILE *stream;
    stream = fopen("collection.txt", "r");
    
    if (stream == NULL) {
        fprintf(stderr, "file not found");
        return 0;
    }
    
    char s[1000];
    Set collection = newSet();
    while (fscanf(stream, "%s", s) != EOF) {  
        insertInto(collection, s);
    }
    
    fclose(stream);
    
    return collection;

}

Graph GetGraph(Set collection) {
    
    Graph URLgraph = newGraph(nElems(collection));
    
    
    return URLgraph;
}

// reads a text file and creates two sets - a URL set (set of URLs in ascending order) & a text set (set of all words in section 2 in A-Z order)
//
Set returnSet(int arg, char *fileName) {
    addTxtSuffix(fileName);
    FILE *file = fopen(fileName, "r");
    char string1[1000];
    char string2[1000];
    char *text = string1; 
    char *prev = string1; 
    char *curr = string1;
    int endSection1 = 0;
    Set URLSet = newSet();
    Set textSet = newSet();

    while (fscanf(file, "%s", text) != EOF) {
        curr = text; 
        if (endSection1 == 0) {
            addURLs(URLSet, curr);
        } else { 
            addText(textSet, curr);
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
 
    
    printf("URL set is: \n");
    showSet(URLSet);
    printf("Text set is: \n");
    showSet(textSet);
    
 
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
    char string[1000];
    char *normalisedWord = string;
    if (toAdd(text) == TRUE) {
        normalisedWord = normaliseWord(text);
        insertInto(textSet, normalisedWord);
    }     
}

int toAdd(char *word) {
    if (strcmp(word, "#start") == 0 || strcmp(word, "Section-1") == 0 || strcmp(word, "#end") == 0 || strcmp(word, "Section-2") == 0) {
        return FALSE; 
    }
    return TRUE;
}

// adds the .txt suffix to a string
void addTxtSuffix(char *string) {
    char *suffix = ".txt";
    strcat(string, suffix);
    return;
}

char *normaliseWord(char *text) {
    int i = 0;
    char string[1000];
    char *lowerString = malloc(strlen(text) + 1);
    if (endsWithSpecialPunctuation(text) == TRUE) {
        for (i = 0; i < strlen(text) - 1; i++) {
            string[i] = tolower(text[i]);
        }
        printf("%s", string);
        strcpy(lowerString, string);
    } else {
        for (i = 0; i < strlen(text); i++) {
            string[i] = tolower(text[i]);
        }
        printf("%s", string);
        strcpy(lowerString, string);
    }
return lowerString;

}

// returns TRUE if the last letter in a word is a special character (., ?, ; or ,)
int endsWithSpecialPunctuation(char *text) {
    if (strlen(text) >= 1 && strcmp(text + strlen(text) - 1, ".") == 0) {
        return TRUE;
    } else if (strlen(text) >= 1 && strcmp(text + strlen(text) - 1, "?") == 0) {
        return TRUE; 
    } else if (strlen(text) >=1 && strcmp(text + strlen(text) - 1, ";") == 0){ 
        return TRUE;
    } else if (strlen(text) >=1 && strcmp(text + strlen(text) - 1, ",") == 0) {
        return TRUE;
    }
    
return FALSE;

}



