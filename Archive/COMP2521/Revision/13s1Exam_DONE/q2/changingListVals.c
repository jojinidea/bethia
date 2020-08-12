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

// if L != NULL
// Cases
// if the list has no elements don't do anything
// if the list has one element, just return it
// if the list has more than one element, reverse

    int temp;
    int i = 0;
    if (L == NULL) {
        return;
    } else if (L->first == L->last) {
        return;
    } else {
        int numLinks = numNodes(L);
        Link first = L->first;
        Link last = L->last; 
        for (i = 0; i <numLinks/2; i++) { 
            temp = first->value;
            //fprintf(stderr, "First->val is %d, Last->value is %d\n", first->value, last->value);
            first->value = last->value; 
            last->value = temp;
            first = first->next; 
            last = findPrev(L, last);
        }
    }

}

// or

	assert(L != NULL);
	if (L->first == NULL) return;
	Link curr, next;
	curr = L->first;
	L->last = L->first;
	while (curr != NULL){
		next = curr->next;
		curr->next = L->first;
		L->first = curr;
		curr = next;
	}
	L->last->next = NULL;


Link findPrev(List L, Link last) {
    Link curr = L->first; 
    while (curr != NULL && curr->next != last) {
            curr = curr->next;
    }
    
return curr; 
}

int numNodes(List L) {
    Link curr = L->first;
    int num = 0;
    while (curr != NULL) {
        num++;
        curr = curr->next; 
    }
return num;
}
