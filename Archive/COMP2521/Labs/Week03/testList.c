// testList.c - testing DLList data type
// Written by John Shepherd, March 2013

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include "DLList.h"

#define BEFORE 0
#define AFTER 1

void show_state(DLList testList);

typedef struct DLListNode {
	char   *value;  // value of this list item (string)
	struct DLListNode *prev;
	               // pointer previous node in list
	struct DLListNode *next;
	               // pointer to next node in list
} DLListNode;

typedef struct DLListRep {
	int  nitems;      // count of items in list
	DLListNode *first; // first node in list
	DLListNode *curr;  // current node in list
	DLListNode *last;  // last node in list
} DLListRep;


int main(int argc, char *argv[])
{
	
    printf("---Making new list---\n"); 
    DLList testList = newDLList();
   
    // Insert After
    // Case 1: Empty List
    printf ("---TESTING INSERT AFTER---\n");
    printf("    ---Case 1: Empty List---\n\n");
    show_state(testList);
    printf("    ---Inserting Line 1 in an Empty List---\n");
    DLListAfter(testList, "Line 1");
    assert(validDLList(testList));
    putDLList(stdout, testList);
    show_state(testList );
    // Case 2: Need to modify last pointer
    // Case 2a: Need to modify last pointer in an 1 element list
    printf("    ---Case 2: Inserting at the End---\n");
    printf("    ---2a: Inserting Line 2 at the End of a 1 Element List---\n");
    putDLList(stdout, testList);
    show_state(testList );
    DLListAfter(testList, "Line 2");  
    assert(validDLList(testList));
    putDLList(stdout, testList);
    show_state(testList );
    // Case 2b: Need to modify last pointer in a multi-element list 
    printf("    ---2b: Inserting Line 3 at the End of a Multi-Element List---\n");
    putDLList(stdout, testList);
    show_state(testList );
    DLListAfter(testList, "Line 3");
    assert(validDLList(testList));
    putDLList(stdout, testList); 
    show_state(testList );
    // Case 3: Inserting in the middle of a list 
    DLListMove(testList, -1);
    printf("    ---Case 3: Inserting Line 3a in the Middle of a List---\n");
    putDLList(stdout, testList);
    show_state(testList );
    DLListAfter(testList, "Line 3a");
    assert(validDLList(testList));
    putDLList(stdout, testList);  
    show_state(testList );

    printf("--COMPLETED TESTING FOR INSERTAFTER---\n\n");
    
   
    // Delete
    printf("---TESTING DELETE ---\n");
    // Case 1: Deleting first and last in Multi-element lists
    // Case 1a: Modifying last in Multi-element Lists
    DLListMove(testList, 2);
    printf("    ---Case 1a: Deleting last in Multi-element Lists---\n");
    putDLList(stdout, testList);
    show_state(testList );
    DLListDelete(testList); 
    putDLList(stdout, testList); 
    show_state(testList ); 
    assert(validDLList(testList));
    // Case 1b: Modifying first in Multi-element Lists
    DLListMove(testList, -4);
    printf("    ---Case 1b: Deleting first in Multi-element Lists---\n");
    putDLList(stdout, testList);
    show_state(testList );
    DLListDelete(testList); 
    putDLList(stdout, testList); 
    show_state(testList ); 
    assert(validDLList(testList));
    // Case 2: Deleting an element with elements on either side in a multi-element list
    DLListBefore(testList, "Line 1");
    DLListBefore(testList, "Line 1b");
    printf("    ---Case 2: Deleting elements with elements on either side in Multi-element Lists---\n");
    putDLList(stdout, testList);
    show_state(testList );
    DLListDelete(testList);
    putDLList(stdout, testList); 
    show_state(testList ); 
    assert(validDLList(testList));
    DLListDelete(testList);
    DLListDelete(testList);
    // Case 3: Deleting in a single-element list
    printf("    ---Case 3: Deleting elements in a single-element list---\n");
    putDLList(stdout, testList);
    show_state(testList );
    DLListDelete(testList);
    putDLList(stdout, testList); 
    show_state(testList ); 
    
    printf("--COMPLETED TESTING FOR DELETE---\n\n");
    
    
    // Insert Before
    printf("---TESTING INSERT BEFORE---\n");
    // Case 1: Empty List
    printf("    ---Case 1: Empty List---\n");
    putDLList(stdout, testList);
    show_state(testList);
    printf("    ---Inserting Line 1 in an Empty List---\n");
    DLListBefore(testList, "Line 1");
    assert(validDLList(testList));
    putDLList(stdout, testList);
    show_state(testList );
    // Case 2: Inserting at the front of the list
    // Case 2a: Inserting at the front of a single-element list
    printf("    ---Case 2: Inserting at the End---\n");
    printf("    ---2a: Inserting Line 2 at the Start of a 1 Element List---\n");
    putDLList(stdout, testList);
    show_state(testList );
    DLListBefore(testList, "Line 2");  
    assert(validDLList(testList));
    putDLList(stdout, testList);
    show_state(testList );
    // Case 2b: Inserting at the front of a multi-element list
    printf("    ---2b: Inserting Line 3 at the Start of a Multi-Element List---\n");
    putDLList(stdout, testList);
    show_state(testList );
    DLListBefore(testList, "Line 3");
    assert(validDLList(testList));
    putDLList(stdout, testList); 
    show_state(testList );
    // Case 3: Inserting between two elements 
    DLListMove(testList, -1);
    printf("    ---Case 3: Inserting Line 3a in the Middle of a List---\n");
    putDLList(stdout, testList);
    show_state(testList );
    DLListBefore(testList, "Line 3a");
    assert(validDLList(testList));
    putDLList(stdout, testList);  
    show_state(testList );

    printf("--COMPLETED TESTING FOR INSERTBEFORE---\n\n");
 
   return 0;

}

void show_state(DLList testList) {
    
    if (testList->curr == NULL) {
        printf("    *** %d objects, L->curr->value = NULL ***\n", DLListLength(testList));
    } else {
        printf("    *** %d objects, L->curr->value = %s ***\n", DLListLength(testList), DLListCurrent(testList));
    } 

}
