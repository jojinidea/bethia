// Binary Search Tree ADT implementation ... 
// Used in COMP2521 exercises
// Written by Jas Shepherd 

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include "BSTree.h"
#include "set.h"

#define text(tree)  ((tree)->text)
#define left(tree)  ((tree)->left)
#define right(tree) ((tree)->right)

typedef struct Node {
   char *text; // key
   Set URLList;
   Tree left, right;
} Node;

// make a new node containing text
Tree newNode(char *key, char *URL) {
   Tree new = malloc(sizeof(Node));
   assert(new != NULL);
   new->URLList = newSet();
   insertInto(new->URLList, URL);
   text(new) = key;
   left(new) = right(new) = NULL;
   return new;
}

// create a new empty Tree
Tree newTree() {
   return NULL;
}

// free memory associated with Tree
void freeTree(Tree t) {
   if (t != NULL) {
      freeTree(left(t));
      freeTree(right(t));
      disposeSet(t->URLList);
      free(t);
   }
}


// display Tree sideways
void showTreeR(Tree t, int depth) {
   if (t != NULL) {
      showTreeR(left(t), depth+1);
	  //putchar(' ');            // TAB character
      printf("%s  ", text(t));
      showSet(t->URLList);
      printf("\n");
      showTreeR(right(t), depth+1);
   }
}


void showNode(Tree t) {
    printf("%s\n", text(t));
}

void showTree(Tree t) {
   showTreeR(t, 0);
}

// compute height of Tree
int TreeHeight(Tree t) {

   // not yet implemented

   return -1;
}

// count #nodes in Tree
int TreeNumNodes(Tree t) {
   if (t == NULL)
      return 0;
   else
      return 1 + TreeNumNodes(left(t)) + TreeNumNodes(right(t));
}

// check whether a key is in a Tree
bool TreeSearch(Tree t, char *key) {
   if (t == NULL)
      return false;
   else if (strcmp(key, text(t)) < 0) 
      return TreeSearch(left(t), key);
   else if (strcmp(key, text(t)) > 0)
      return TreeSearch(right(t), key);
   else                                 // key == word(t)
      return true;
}

Tree returnNode(Tree t, char *key) {
    if (strcmp(key, text(t)) == 0) {
        return t;
    } else if (strcmp(key, text(t)) < 0) {
        return returnNode(left(t), key);
    } else  {
        return returnNode(right(t), key);
    }

}

Set returnURLSet(Tree t) {
    return t->URLList;

}

// insert a new item into a Tree
Tree TreeInsert(Tree t, char *key, char *URL) {
   if (t == NULL)
      t = newNode(key, URL);
   else if (strcmp(key, text(t)) < 0) 
      left(t) = TreeInsert(left(t), key, URL);
   else if (strcmp(key, text(t)) > 0) 
      right(t) = TreeInsert(right(t), key, URL);
   return t;
}

Tree joinTrees(Tree t1, Tree t2) {
   if (t1 == NULL)
      return t1;
   else if (t2 == NULL)
      return t2;
   else {
      Tree curr = t2;
      Tree parent = NULL;
      while (left(curr) != NULL) {    // find min element in t2
	 parent = curr;
	 curr = left(curr);
      }
      if (parent != NULL) {
	 left(parent) = right(curr);  // unlink min element from parent
	 right(curr) = t2;
      }
      left(curr) = t1;
      return curr;                    // min element is new root
   }
}

// delete an item from a Tree
Tree TreeDelete(Tree t, char *key) {
   if (t != NULL) {
      if (strcmp(key, text(t)) < 0)
	 left(t) = TreeDelete(left(t), key);
      else if (strcmp(key, text(t)) > 0)
	 right(t) = TreeDelete(right(t), key);
      else {
	 Tree new;
	 if (left(t) == NULL && right(t) == NULL) 
	    new = NULL;
	 else if (left(t) == NULL)    // if only right subtree, make it the new root
	    new = right(t);
	 else if (right(t) == NULL)   // if only left subtree, make it the new root
	    new = left(t);
	 else                         // left(t) != NULL and right(t) != NULL
	    new = joinTrees(left(t), right(t));
	 free(t);
	 t = new;
      }
   }
   return t;
}

Tree rotateRight(Tree n1) {
   if (n1 == NULL || left(n1) == NULL)
      return n1;
   Tree n2 = left(n1);
   left(n1) = right(n2);
   right(n2) = n1;
   return n2;
}

Tree rotateLeft(Tree n2) {
   if (n2 == NULL || right(n2) == NULL)
      return n2;
   Tree n1 = right(n2);
   right(n2) = left(n1);
   left(n1) = n2;
   return n1;
}

Tree insertAtRoot(Tree t, Item key) {

   printf("Not yet implemented.\n");
   
   return t;
}

Tree partition(Tree t, int i) {
   if (t != NULL) {
      assert(0 <= i && i < TreeNumNodes(t));
      int m = TreeNumNodes(left(t));
      if (i < m) {
	 left(t) = partition(left(t), i);
	 t = rotateRight(t);
      } else if (i > m) {
	 right(t) = partition(right(t), i-m-1);
	 t = rotateLeft(t);
      }
   }
   return t;
}

Tree rebalance(Tree t) {
   int n = TreeNumNodes(t);
   if (n >= 3) {
      t = partition(t, n/2);           // put node with median key at root
      left(t) = rebalance(left(t));    // then rebalance each subtree
      right(t) = rebalance(right(t));
   }
   return t;
}

void InfixTraversal(Tree t) {
    if (t == NULL) {
        return;
    } else {
        InfixTraversal(left(t));
        printf("%s  ", t->text);
        showSet(returnURLSet(t));
        InfixTraversal(right(t));
    }

}
