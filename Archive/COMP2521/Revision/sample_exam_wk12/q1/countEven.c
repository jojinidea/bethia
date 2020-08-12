
/* countEven.c 
   Written by Ashesh Mahidadia, October 2017
*/

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include "BSTree.h"

int treeDepth(BSTree t);
int isHeapUtil(BSTree t);

/* 
    You will submit only this one file.

    Implement the function "countEven" below. Read the exam paper for 
    detailed specification and description of your task.  

    - You can add helper functions in this file, if required.  

    - DO NOT modify code in the file BSTree.h . 
    - DO NOT add "main" function in this file. 
*/

// count number of nodes in BST
int countEven(BSTree t){ 
    if (isHeapUtil(t) == true) {
        printf("True, we have a heap\n");
        return 1;
    }
    printf("We do not have a heap\n");
    

return 0;

}


// we want to check whether each subtree satisfies the heap property
// base case t == NULL || t->left == NULL && t->right == NULL
int isHeapUtil(BSTree t) {
    if (t == NULL || (t->left == NULL && t->right == NULL)) {
        return 1;
    }
    if (t->left == NULL) {
        if (t->key > t->right->key) {
            return isHeapUtil(t->right);
        }
    return 0;
    }
    if (t->right == NULL) {
        if (t->key > t->left->key) {
            return isHeapUtil(t->left);
        }
    return 0;
    }
    if (t->key > t->left->key && t->key > t->right->key) {
        return (isHeapUtil(t->right) && isHeapUtil(t->left));
    } else {
        return 0;
    }


}



// check whether each subtree satisfies this property
