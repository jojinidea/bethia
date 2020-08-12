// removeValue.c 
// Written by Ashesh Mahidadia, August 2017

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include "DLList.h"


/* 
    You will submit only this one file.

    Implement the function "removeValue" below. Read the exam paper for 
    detailed specification and description of your task.  

    - DO NOT modify code in the file DLList.h . 
    - You can add helper functions in this file.  
    - DO NOT add "main" function in this file. 
    
*/


void removeValue(DLList L, int value){

    DLListNode *curr = L->first; 
    DLListNode *after;
    DLListNode *before; 
    DLListNode *temp;
    
    if (DLListLength(L) != 0) {
    // do this 
        while (curr != NULL) {
            if (curr->value == value) {
                temp = curr; 
                if (curr == L->first) {
                    fprintf(stderr, "L->nitems is %d\n", L->nitems);
                    // remove first
                    if (DLListLength(L) == 1) {
                        // we only have one element, modify last & first
                        L->last = L->first = L->curr = NULL;
                        free(temp);
                        L->nitems--;
                        return;
                    } else {
                    fprintf(stderr, "Hello\n");
                        L->first = curr->next; 
                        L->first->prev = NULL;
                        L->curr = L->first; 
                        free(temp);
                    }
                } else if (curr == L->last) {
                    fprintf(stderr, "L->last\n");
                    // remove last
                    if (DLListLength(L) == 1) {
                        L->first = L->last = L->curr = NULL;
                        free(temp);
                        L->nitems--;
                        return;
                    } else {
                        L->last = L->last->prev;
                        L->last->next = NULL;
                        free(temp);
                    }
                } else if (curr != L->first && curr != L->last) {
                fprintf(stderr, "L->middle\n");
                    after = temp->next;
                    before = temp->prev;
                    after->prev = before;
                    before->next = after; 
                    free(temp);
                    curr = before;
                    // remove middle
                }
            L->nitems--;  
            }
            }
            curr = curr->next;      
    } else {
        return; 
    }
         
         
       
	return;
}

