// List.c ... implementation of simple List ADT

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include "List.h"


typedef struct Node *Link;

typedef struct Node {
	int  value;
	Link next;
} Node;

typedef struct ListRep {
	int  nnodes;
	Link first;
	Link last;
} ListRep;

Link findPrev(List L, Link last);
int numNodes(List L);

// newList ... make new empty List
List newList()
{
	List new = malloc(sizeof(ListRep));
	assert(new != NULL);
	new->nnodes = 0;
	new->first = NULL;
	new->last = NULL;
	return new;
}

// ListShow ... display List as <a, b, c, d, ...z>
void ListShow(List L)
{
	assert(L != NULL);
	printf("[");
	Link curr = L->first;
	while (curr != NULL) {
		printf("%d",curr->value);
		if (curr->next != NULL) printf(", ");
		curr = curr->next;
	}
	printf("]\n");
}

// ListLength ... number of nodes in List
int ListLength(List L)
{
	assert(L != NULL);
	return (L->nnodes);
}

// ListAppend ... append a new value to List
void ListAppend(List L, int value)
{
	assert(L != NULL);
	Link new = malloc(sizeof(Node));
	assert(new != NULL);
	new->value = value;
	new->next = NULL;
	L->nnodes++;
	if (L->first == NULL)
		L->first = L->last = new;
	else {
		L->last->next = new;
		L->last = new;
	}
}

// ListReverse ... reverse a List
void ListReverse(List L)
{

Link prev;
Link curr; 
Link next; 

if (L == NULL) {
    return; 
} else if (L->first == L->last) {
    return;
} else {
    prev = L->first; 
    L->last = L->first; 
    curr = prev->next;
    next = curr->next; 
    for (curr = prev->next; curr->next != NULL; curr = next) {
        next = curr->next; 
        curr->next = prev;
        prev = curr;
    }
    curr->next = prev;
    L->first = curr; 
    L->last->next = NULL;


}

// PLAN HEAPS FIRST THEN CODE
// careful with CASES, make sure you never set a value to NULL- can't access NULLs

}
