#include <stdio.h> 
#include <string.h>
#include <stdlib.h>
#include "set.h"
#include "BSTree.h"
#include "readData.h"

Tree createInvertedIndex (void);
Tree addInvertedIndex (Set textCollection, Tree invertedIndex, char *URL);

/*
int main (void) {
    Tree t = createInvertedIndex();
    
    freopen("invertedIndex.txt", "w", stdout);
    showTree(t);
    freeTree(t);
    return 0;
}
*/

// creates an inverted index

Tree createInvertedIndex (void) {
    Set URLCollection = GetCollection();
    Set textCollection;
    Tree invertedIndex = newTree();
    Tree temp;
    char string[MAX_CHAR];
    char *URL = string;

    int i = 0;
    
    for (i = 0; i < nElems(URLCollection) ; i++) {
        strcpy(URL, leaveSet(URLCollection)); 
        textCollection = returnSet(WANT_TEXT, TXT_NEEDED, URL);
        temp = addInvertedIndex(textCollection, invertedIndex, URL);
        invertedIndex = temp;
      
    }
    disposeSet(URLCollection);
    disposeSet(textCollection);
    
    return invertedIndex;


}

// adds a URL to the inverted index
Tree addInvertedIndex (Set textCollection, Tree invertedIndex, char *URL) {
    Tree temp;
    int i = 0;
    char *key;
    Tree node; 
    Set URLSet;
    
    for (i = 0; i < nElems(textCollection); i++) {                          
        key = leaveSet(textCollection);
        if (TreeSearch(invertedIndex, key) == false) {                      // if the word is not in the tree, add it
            temp = TreeInsert(invertedIndex, key, URL); 
            invertedIndex = temp;  
        } else {                                                            // otherwise, find the word and append the URL to its URL set
            node = returnNode(invertedIndex, key);
            URLSet = returnURLSet(node);
            if (isElem(URLSet, URL) == FALSE) {
                insertInto(URLSet, URL);
            }
        }
    }

return invertedIndex; 

}


