// Linked list interface ... COMP2521 
// list.h was provided by COMP2521 from the week-5a exercises.
#include <stdbool.h>

typedef struct Node *SList;
#define TRUE 1
#define FALSE 0
#define SWAP_TFIDF 2
#define SWAP_FREQUENCY 3

SList insertSL(SList, char *URL, double value, int frequency);
SList deleteSL(SList, char *URL);
bool inSL(SList, char *URL);
void freeSL(SList);
void showSL(SList, int arg);
SList returnSLNode(SList, char *URL);
void changeValue(SList, double value);
void swap(SList A, SList B);
void bubbleSort (SList L, int arg);
int toSwap (SList curr, int arg);
void arrangeList(SList L);
