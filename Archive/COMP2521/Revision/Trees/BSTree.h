// Binary Search Tree ADT interface ... 

#include <stdbool.h>
#include "set.h"

typedef char* Item;      // item is just a key

typedef struct Node *Tree;
typedef struct SetRep *Set;

Tree newTree();        // create an empty Tree
void freeTree(Tree);   // free memory associated with Tree
void showTree(Tree);   // display a Tree (sideways)

bool TreeSearch(Tree, Item);   // check whether an item is in a Tree
int  TreeHeight(Tree);         // compute height of Tree
int  TreeNumNodes(Tree);       // count #nodes in Tree
Tree TreeInsert(Tree, Item, char *URL);   // insert a new item into a Tree
Tree TreeDelete(Tree, Item);   // delete an item from a Tree
Tree returnNode(Tree t, char *key); // returns a node containing key 
void showNode(Tree t);
Set returnURLSet(Tree t); // returns set associated with a specific node

// internal functions made visible for testing
Tree rotateRight(Tree);
Tree rotateLeft(Tree);
Tree insertAtRoot(Tree, Item);
Tree partition(Tree, int);
Tree rebalance(Tree);
void InfixTraversal(Tree t);

