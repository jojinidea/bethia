// getPeaks.c 
// Written by Ashesh Mahidadia, August 2017

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include "DLList.h"


/* 
    You will submit only this one file.

    Implement the function "getPeaks" below. Read the exam paper for 
    detailed specification and description of your task.  

    - DO NOT modify code in the file DLList.h . 
    - You can add helper functions in this file.  
    - DO NOT add "main" function in this file. 
    
*/
void insertpeaks(DLListNode *newpeak, DLList peaksL);

DLList getPeaks(DLList L){

	DLList peaksL = newDLList();
    // cases
    // 1. the list is empty or has less than 3 elements (so cannot have a peak, so just return) 
    // 2. the list has 3 or more elements (so can have a peak)
        // make curr = the second element, compare with prev & next
    // things to think about - cannot access elements that are NULL - think about condition at the start of the while loop
    // if list is empty, return empty list
        
    if (DLListLength(L) >= 3) {
        DLListNode *curr = L->first->next; 
        DLListNode *newpeak;
        while (curr->next != NULL) {
            fprintf(stderr, "Hello\n");
            if (curr->prev->value < curr->value && curr->next->value < curr->value) { 
                fprintf(stderr, "Entering loop\n");
                newpeak = newDLListNode(curr->value);
                // insert this peak 
                insertpeaks(newpeak, peaksL);
                peaksL->nitems++;
            }
        fprintf(stderr, "Hello1\n"); 
        curr = curr->next; 
        fprintf(stderr, "Hello2\n");
        }
    }
      
	return peaksL;

}


void insertpeaks(DLListNode *newpeak, DLList peaksL) {
    DLListNode *currpeak = peaksL->first;
    if (DLListLength(peaksL) == 0) {
        // inserting first element in the list
        peaksL->first = peaksL->last = peaksL->curr = newpeak;
        currpeak = newpeak;
    } else {
        currpeak->next = newpeak;
        newpeak->prev = currpeak;
        currpeak = newpeak;
        peaksL->last = newpeak;
        newpeak->next = NULL;
    }
    //peaksL->curr = peaksL->first;

}


