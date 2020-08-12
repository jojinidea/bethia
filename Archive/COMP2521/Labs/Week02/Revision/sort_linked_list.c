// implement bubblesort to sort a linked list in C

#include <stdio.h>
#include <stdlib.h> 

struct node {
    int data;
    struct node *next;

};

int main (void) {



}

void swap_nodes(struct node *left, struct node *right, struct node *head) {

// left is bigger, right is smaller 

// left's_prev->next = right
// right->next = left 

// but we have to consider the cases where
// right is the first node (so there is nothing before it) 



}


// use bubblesort, compare two elements in a linked list, if the one on the right is smaller than the one on the left, swap nodes 
// Keep doing this until we no longer need to sort the list anymore
