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

    L->curr = L->first;
    struct DLListNode *temp = NULL; 
    //struct DLListNode *after = NULL; 
    //struct DLListNode *before = NULL;
    
    // 2 big cases
    // 1. list is empty - return empty list 
    // 2. list is not empty
        // a. Remove first node 
            // 1. Remove first node and there's other stuff in the list
            // 2. Remove first node and nothing else in the list
        // b. Remove last node
            // 1. Remove last node and there's other stuff in the list
            // 2. Remove last node and there's nothing else in the list
        // c. Remove node in the middle 
        
   // DON'T UPDATE CURR MANUALLY, make curr = L->first 
   // BE CAREFUL WITH IFs - L->curr could be NULL so don't want to be accessing L->curr->value
   
    if (DLListLength(L) == 0) {
        return;
    } 
    
    }
         
         
       
	return;
}

