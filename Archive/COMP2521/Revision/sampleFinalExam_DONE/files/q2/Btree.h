#include <stdio.h>
#include <stdlib.h>
#include <string.h>


#define data(tree)  ((tree)->data)
#define left(tree)  ((tree)->left)
#define right(tree) ((tree)->right)


typedef struct Node *BTree;
typedef struct Node {
   int  data;
   BTree left, right;
} Node;

