// removeValue.c 
// Written by Ashesh Mahidadia, August 2017

// DO NOT FORGET DON'T MODIFY ANY OF THE POINTERS IN THE STRUCT
// NEED TO CHANGE NITEMS
// FIRST->PREV == NULL
// LAST->NEXT == NULL

// IF WE HAVEN'T DELETED AN ELEMENT, MOVE, IF WE HAVE, DON'T MOVE

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include "DLList.h"

void removeFirst(DLList L, DLListNode *remove);
void removeLast(DLList L, DLListNode *remove);
void removeMiddle(DLList L, DLListNode *remove);
//void printlist(DLList L);
/* 
    You will submit only this one file.

    Implement the function "removeValue" below. Read the exam paper for 
    detailed specification and description of your task.  

    - DO NOT modify code in the file DLList.h . 
    - You can add helper functions in this file.  
    - DO NOT add "main" function in this file. 
    
*/


void removeValue(DLList L, int value){
    // 2 big cases
    // 1. list is empty - return
    // 2. list is not empty - iterate through the list
        // IF THE LIST IS one element and value == curr->value, modify L->curr, L->head and L->last 
        // a. If value is first node
        // remove this node, make curr = L->first, don't increment curr at the end
        // b. If value is the last node
        // remove this node, make curr = L->last, don't increment curr at the end 
        // c. If the value is in the middle
        // make curr prev, increment curr at the end 
    
    DLListNode *curr = L->first; 
    DLListNode *after;
    DLListNode *before;
    DLListNode *temp;
    int increment = 1;
    if (DLListLength(L) != 0) {
        // iterate through the list
        while (curr != NULL) {
            if (curr->value == value) {
                if (DLListLength(L) == 1) {
                    temp = curr; 
                    L->first = L->last = L->curr = NULL;
                    free(temp);
                    L->nitems--;
                    return;
                } else if (curr == L->first) {
                    // remove first
                    temp = curr; 
                    L->first = L->first->next; 
                    L->first->prev = NULL;
                    curr = L->first; 
                    free(temp);
                    increment = 0;
                } else if (curr == L->last) {
                    temp = curr;
                    L->last = L->last->prev;
                    L->last->next = NULL;
                    curr = L->last; 
                    free(temp);
                } else {
                    // remove middle 
                    temp = curr;
                    after = curr->next;
                    before = curr->prev;
                    after->prev = before;
                    before->next = after; 
                    free(temp);
                }
            L->nitems--;
            L->curr = L->first; 
            }        
            if (increment == 1) {
                curr = curr->next; 
            }
            increment = 1;
        }
    
    }       

return; 

}
