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
        
        // Remove Value: 
        // If list is empty, return
        // If list is not empty, iterate through the list
        // While curr != NULL
        // if (curr->value == value), we need to remove this
        // 4 cases
        // 1 if the list has one element - need to modify first, last & curr
        // 2. if curr == L->first
            // TEMP = CURR
            // a. L->first = L->first->next
            // b. L->first->prev = NULL
            // c. curr = L->first; 
            // free(temp)
            // L->nitems--
            // WE DO NOT increment curr
        // 3. if curr == L-> last
            // TEMP = CURR
            // a. L->last = L->last->prev
            // b. L->last->next = NNULL
            // c. curr = L->last
            // c. free(temp)
            // L->nitems--
        // 4. if curr != L->last && curr != L->first
            // TEMP = CURR
            // a. after = temp->next;
            // b. before = temp->prev;
            // c. after->prev = before
            // d. before->next = after;
            // e. curr = before
            // f. free(temp)
            // L->nitems--
        // only increment curr if NOT first
        
        // INSERT
        // If the list has zero elements, need to modify first, last & curr
        // otherwise, if we want to insert at the start
            // new->next = L->curr
            // L->curr->prev = new
            // L->curr = new
            // L->first = new
        // If we want to insert at the end
            // L->last->next = new;
            // new->prev = L->last;
            // new->next = NULL 
            // L->last = new
        // if we want to insert in the middle
            // temp = L->curr->prev
            // L->curr->prev = new
            // new->next = L->curr
            // temp->next = new
            // new->prev = temp
            // L->curr = new
        
    } else if (L->first == L->curr) {                                       // Case 2: Change first pointer
        new->next = L->curr;
        L->curr->prev = new;
        L->curr = new; 
        L->first = new;
    } else {                                                                // Case 3: No need to change first/last, insert somewhere in the middle
        DLListNode *temp = L->curr->prev;
        L->curr->prev = new;
        new->next = L->curr;
        temp->next = new;
        new->prev = temp;
        L->curr = new;
         
    
    DLListNode *temp;
    DLListNode *curr = L->first; 
    DLListNode *after;
    DLListNode *before;
    int increment = 1;
    
    if (DLListLength(L) != 0) {
        while (curr != NULL) {
            if (DLListLength(L) == 1) {
                L->first = L->last = L->curr = NULL;
                L->nitems--;
                return;
            } else {
                if (curr->value == value) {
                    if (curr == L->first) {
                        temp = curr; 
                        L->first = L->first->next;
                        L->first->prev = NULL;
                        free(temp);
                        curr = L->first;
                        increment = 0;
                    } else if (curr == L->last) {
                        temp = curr;
                        L->last = L->last->prev;
                        L->last->next = NULL;
                        curr = L->last;
                        free(temp);
                    } else if (curr != L->last && curr != L->first) {
                        temp = curr;
                        after = curr->next; 
                        before = curr->prev;
                        after->prev = before;
                        before->next = after; 
                        free(temp);
                    }
                L->curr = L->first; 
                L->nitems--;
                }
            }
        if (increment == 1) {
            curr = curr->next;
        }
        increment = 1;
        }
    
    
    }   

return; 

}
