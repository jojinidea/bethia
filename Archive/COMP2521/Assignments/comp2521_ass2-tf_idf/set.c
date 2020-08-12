// set.c ... simple, inefficient Set of Strings
// Written by John Shepherd, September 2015

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include "set.h"

#define strEQ(s,t) (strcmp((s),(t)) == 0)
#define strLT(s,t) (strcmp((s),(t)) < 0)

typedef struct Node *Link;

typedef struct Node {
	char *val;
	Link  next;
} Node;
	
typedef struct SetRep {
	int   nelems;
	Link  elems;
} SetRep;

// Function signatures

Set newSet();
void disposeSet(Set);
void insertInto(Set,char *);
void dropFrom(Set,char *);
int  isElem(Set,char *);
int  nElems(Set);
char *leaveSet(Set);
static Link newNode(char *);
static void disposeNode(Link);
static int  findNode(Link,char *,Link *,Link *);
char *returnFirst(Set);
int frequency(Set, char *searchWord); 


// newSet()
// - create an initially empty Set
Set newSet()
{
	Set new = malloc(sizeof(SetRep));
	assert(new != NULL);
	new->nelems = 0;
	new->elems = NULL;
	return new;
}

// disposeSet(Set)
// - clean up memory associated with Set
void disposeSet(Set s)
{

	Link next, curr = s->elems;
	while (curr != NULL) {
		next = curr->next;
		disposeNode(curr);	
		curr = next;
	}

	free(s);
	return;

}

// insertInto(Set,Str)
// - ensure that Str is in Set
// PLEASE DO NOT MODIFY THIS
void insertIntoDuplicates(Set s, char *str)
{
	//assert(s != NULL);
	Link curr, prev;
	//assert(s->elems != NULL);
	findNode(s->elems,str,&curr,&prev); // found comment out and next line
	//if (found) return; // already in Set
	Link new = newNode(str);
	s->nelems++;
	if (prev == NULL) {
		// add at start of list of elems
		new->next = s->elems;
		s->elems = new;
	}
	else {
		// add into list of elems
		new->next = prev->next;
		prev->next = new;
	}
}

void insertInto(Set s, char *str)
{
	//assert(s != NULL); / *THIS IS NOT COMMENTED OUT ON THE OLD VER
	Link curr, prev;
	//assert(s->elems != NULL);
	int found = findNode(s->elems,str,&curr,&prev); // found comment out and next line
	if (found) {
	    //free(str);
	    return; // already in Set
	}
	Link new = newNode(str);
	//free(str);
	s->nelems++;
	if (prev == NULL) {
		// add at start of list of elems
		new->next = s->elems;
		s->elems = new;
	}
	else {
		// add into list of elems
		new->next = prev->next;
		prev->next = new;
	}
}

// dropFrom(Set,Str)
// - ensure that Str is not in Set
void dropFrom(Set s, char *str)
{
	assert(s != NULL);
	Link curr, prev;
	//if (s->elems == NULL) {
	//    return;
	//}
	//assert(s->elems != NULL); // NOT IN ORIGINAL
	int found = findNode(s->elems,str,&curr,&prev);
	if (!found) return;
	s->nelems--;
	if (prev == NULL)
		s->elems = curr->next;
	else
		prev->next = curr->next;
	disposeNode(curr);
}

// isElem(Set,Str)
// - check whether Str is contained in Set
int isElem(Set s, char *str)
{
	assert(s != NULL);
	Link curr, prev;
	//assert(s->elems != NULL); // NOT IN ORIGINAL
	return findNode(s->elems,str,&curr,&prev);
}

// nElems(Set)
// - return # elements in Set
int  nElems(Set s)
{
	assert(s != NULL);
	return s->nelems;
}



// showSet(Set)
// - display Set (for debugging)
void showSet(Set s)
{
	Link curr;
	if (s->nelems == 0)
		printf("Set is empty\n");
	else {
		//printf("Set has %d elements:\n",s->nelems);
		int id = 0;
		curr = s->elems;
		while (curr != NULL) {
			printf("%s ", curr->val);
			//printf("[%03d] %s\n", id, curr->val); // CHANGED THIS PRINT FORMAT TO ABOVE BECAUSE I NEED THE ABOVE FOR INVERTED INDEX
			id++;
			curr = curr->next;
		}
	}
}

// DON'T HAVE GET ELEM

// Helper functions

static Link newNode(char *str)
{
	Link new = malloc(sizeof(Node));
	assert(new != NULL);
	char *strdup = malloc(strlen(str)+1);
	strcpy(strdup, str);
	new->val = strdup;
	new->next = NULL;
	return new;
}

static void disposeNode(Link curr)
{
	assert(curr != NULL);
	free(curr->val);
	free(curr);
}

// findNode(L,Str)
// - finds where Str could be added into L
// - if already in L, curr->val == Str
// - if not already in L, curr and prev indicate where to insert
// - return value indicates whether Str found or not
static int findNode(Link list, char *str, Link *cur, Link *pre)
{
	Link curr = list, prev = NULL;
	while (curr != NULL && strLT(curr->val,str)) {
		prev = curr;
		curr = curr->next;
	}
	*cur = curr; *pre = prev;
	return (curr != NULL && strEQ(str,curr->val));
}


// FUNCTIONS NOT IN ORIGINAL
char *leaveSet(Set s)
{
	assert (s != NULL && s->elems != NULL);
    char *str = s->elems->val;
	Link old = s->elems;
	s->elems = old->next;
	//if (q->front == NULL)
	//	q->back = NULL;
	free(old);
	return str;
}


char *returnFirst(Set s) {
    assert(s != NULL && s->elems != NULL);
    char *str = s->elems->val;
    return str;

}

char *getElem(Set s, int pos) 
{
    int counter = 0;
    char *elem = NULL;
    int found = 0;
    assert(pos < s->nelems);
    assert(pos >= 0);
    assert(s->nelems > 0);
    Link curr = s->elems;
    while (!found && curr != NULL) {
        if (counter == pos) {
            found = 1;
            elem = curr->val;
        }
        counter++;
        curr = curr->next;
    }
    return elem;
}

int frequency(Set s, char *searchWord) {
    assert(s != NULL && s->elems != NULL); 
    Link curr = s->elems;
    int frequency = 0;
    
    while (curr != NULL) {
        if (strcmp(curr->val, searchWord) == 0) {
            frequency++;
        }
    curr = curr->next; 
    }
    
    return frequency;
}

