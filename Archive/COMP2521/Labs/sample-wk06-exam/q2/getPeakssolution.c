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

DLList getPeaks(DLList L){

	DLList peaksL = newDLList();
    
    DLListNode *curr = L->first;
    DLListNode *currpeak;
    DLListNode *newpeak;
    int peak;
    fprintf(stderr, "nitems is %d\n", peaksL->nitems);
    
    if (DLListLength(L) >= 3) {
        // there is such a thing as a peak
        curr = L->first->next; 
        while (curr->next != NULL)  {        // cannot have a peak that's the last element in the list
            if (curr->value > curr->prev->value && curr->value > curr->next->value) {
                // curr is a peak 
                peak = curr->value;
                newpeak = newDLListNode(peak);
                if (DLListLength(peaksL) == 0) {
                    fprintf(stderr, "Inserting first peak\n");
                    // inserting first peak into the list
                    peaksL->first = peaksL->last = peaksL->curr = newpeak;
                    currpeak = newpeak;
                    peaksL->nitems++;
                } else {
                    // inserting a peak alongside existing peaks
                    fprintf(stderr, "Inserting next peak\n");
                    currpeak->next = newpeak;
                    newpeak->prev = currpeak;
                    currpeak = newpeak;
                    peaksL->last = newpeak;
                    peaksL->nitems++;
                }
            
            fprintf(stderr, "nitems 1 is %d\n", peaksL->nitems);
            }
        curr = curr->next;
        }
    
    }
    fprintf(stderr, "nitems from peaks is %d, nitems from L is %d\n", peaksL->nitems, L->nitems);

	return peaksL;

}



