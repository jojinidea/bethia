// Linked list implementation ... COMP2521 
#include "simpleList.h"
#include <assert.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define TRUE 1
#define FALSE 0
#define SWAP_TFIDF 2
#define SWAP_FREQUENCY 3

typedef struct Node {
   double         tf_idf;
   char *v;
   int frequency;   // refers to number of search terms that appear in a given URL
   struct Node *next; 
} Node;

Node *makeSNode(char *URL, double value, int frequency) {
   Node *new = malloc(sizeof(Node));
   assert(new != NULL);
   new->tf_idf = value;
   new->v = URL;
   new->frequency = frequency;
   new->next = NULL;
   return new;
}

SList insertSL(SList L, char *URL, double value, int frequency) {
   if (inSL(L, URL))
      return L;

   // add new node at the beginning
   
    if (L == NULL) {
        L = makeSNode(URL, value, frequency);
        //printf("URL->value is %lf and char is %s\n", L->tf_idf, L->v);
        return L;
    } else {
        Node *new = makeSNode(URL, value, frequency);
        new->next = L;
        L = new;
        return L;
    
    }

}



SList deleteSL(SList L, char *URL) {
   if (L == NULL)
      return L;
   if (strcmp(L->v, URL) == 0)
      return L->next;

   L->next = deleteSL(L->next, URL);
   return L;

}

bool inSL(SList L, char *URL) {
   if (L == NULL)
      return false;
   if (strcmp(L->v,URL) == 0)
     return true;

   return inSL(L->next, URL);
}

void showSL(SList L, int arg) {
   if (L == NULL)
      return;
   if (arg == 0) {
      return;
   }
   else {
      printf("%s  %.6f\n", L->v, L->tf_idf);
      showSL(L->next, arg--);
   }
}

void bubbleSort (SList L, int arg) {
    int swapped = 1;
    SList curr;
    SList last = NULL;
    
    if (L == NULL) {
        return;
    }
    while (swapped) {
        swapped = 0;
        curr = L;
        while (curr->next != last) {
            if (toSwap(curr, arg) == TRUE) {
                swap(curr, curr->next);
                swapped = TRUE;
                
            } 
        curr = curr->next; 
        }
        last = curr;
    }
   
}

int toSwap (SList curr, int arg) {
    if (arg == SWAP_TFIDF) {
        if (curr->frequency == curr->next->frequency) {
            if (curr->tf_idf < curr->next->tf_idf) {
                return TRUE;
            } 
            if (curr->tf_idf == curr->next->tf_idf) {
                if (strcmp(curr->v, curr->next->v) < 0) {
                    return TRUE;
                }
            }
        }
    } else if (arg == SWAP_FREQUENCY) { 
        if (curr->frequency < curr->next->frequency) {
            return TRUE;
        }
    } 
       
return FALSE;

}

void swap(SList A, SList B) {
    double temp_tf_idf = A->tf_idf;
    char *temp_v = A->v;
    int temp_f = A->frequency;
    A->tf_idf = B->tf_idf;
    A->v = B->v;
    A->frequency = B->frequency;
    B->tf_idf = temp_tf_idf;
    B->v = temp_v;
    B->frequency = temp_f;
}

void freeSL(SList L) {
   if (L != NULL) {
      freeSL(L->next);
      free(L);
   }
}

SList returnSLNode(SList L, char *URL) {
    assert(L != NULL);
    SList curr = L;
    while (curr != NULL) {
        if (strcmp(URL, curr->v) == 0) {
            return curr;
        }
    curr = curr->next;
    }
    
return NULL;
}

// changes a tf-idf's value by adding value, also increments frequency by 1
void changeValue(SList L, double value) {
    L->tf_idf = L->tf_idf + value;
    L->frequency = L->frequency + 1;
}

// sorts list first based on the number of search terms that appear in a URL
// then sorts list based on TF_IDF values
void arrangeList(SList L) {
    // first arrange list based on frequency
    bubbleSort(L, SWAP_FREQUENCY);   
    bubbleSort(L, SWAP_TFIDF);

}


