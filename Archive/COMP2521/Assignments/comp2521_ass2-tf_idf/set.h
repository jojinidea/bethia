// set.h ... interface to simple Set of Strings
// Written by John Shepherd, September 2015

#ifndef SET_H
#define SET_H

typedef struct SetRep *Set;

// Function signatures

Set newSet();
void disposeSet(Set);
void insertInto(Set,char *);
void insertIntoDuplicates(Set s, char *);
void dropFrom(Set,char *);
int  isElem(Set,char *);
int  nElems(Set);
void showSet(Set);
char *leaveSet(Set);
char *returnFirst(Set);
int frequency(Set, char *searchWord); 

#endif
