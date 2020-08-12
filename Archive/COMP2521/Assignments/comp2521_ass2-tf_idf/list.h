// Linked list interface ... COMP2521 
// list.h was provided by COMP2521 from the week-5a exercises.
#include <stdbool.h>

typedef struct Node *List;

List insertLL(List, int);
List deleteLL(List, int);
bool inLL(List, int);
void freeLL(List);
void showLL(List);
