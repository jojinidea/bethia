
/* countEven.c 
   Written by Ashesh Mahidadia, October 2017
*/

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include "BSTree.h"

int isHeap(BTree t) {
    // base case, if t == NULL or t->left == NULL && t->right == NULL
    if (t == NULL || t->left == NULL && t->right == NULL) {
        return 1;
    }
    if (t->left == NULL) {
        if (t->data > t->right->data) {
            return isHeap(t->right);
        }   
    return 0;
    }
    if (t->right == NULL) {
        if (t->data > t->left->data) {
            return isHeap(t->left);
        }
    return 0;
    }
    if (t->left != NULL && t->right != NULL) {
        if (t->data > t->left->data && t->data > t->right->data){
            return (isHeap(t->left) && isHeap(t->right));
        }
    return 0;
    }


}


