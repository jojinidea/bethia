// Practicing doubly_linked_lists

#include <stdio.h>
#include <stdlib.h>



typedef struct DLListNode {
    int value;
    struct DLListNode *prev;
    struct DLListNode *next; 

} DLListNode; 

typedef struct DLListRep {
    int nitems;
    DLListNode *first;
    DLListNode *curr;
    DLListNode *last; 

} DLListRep;

void print_list(DLListRep *L);
void remove_num(DLListRep *L, int num); 
void remove_first(DLListRep *L);
void remove_middle(DLListRep *L, int num);
void remove_last(DLListRep *L);
void print_list_backwards(DLListRep *L);

int main (void) {
    struct DLListRep *L;
    struct DLListNode *nodeone;
    struct DLListNode *nodetwo;
    struct DLListNode *nodethree;
    struct DLListNode *nodefour; 
    L = malloc(sizeof(struct DLListRep));
    nodeone = malloc(sizeof(struct DLListNode));
    nodetwo = malloc(sizeof(struct DLListNode));
    nodethree = malloc(sizeof(struct DLListNode));
    nodefour = malloc(sizeof(struct DLListNode));
    nodeone->value = 1;
    nodetwo->value = 2; 
    nodethree->value = 2; 
    nodefour->value = 2;
    L->first = nodeone;
    nodeone->next = nodetwo;
    nodetwo->next = nodethree;
    nodethree->next = nodefour;
    nodefour->next = NULL;
    L->last = nodefour;
    nodefour->prev = nodethree;
    nodethree->prev = nodetwo;
    nodetwo->prev = nodeone;
    L->curr = nodeone; 
    
    int num = 0;
    scanf("%d", &num);
    remove_num(L, num);
    print_list(L); 
    print_list_backwards(L);
    // remove num  

}

void print_list(DLListRep *L) {
    struct DLListNode *currr = L->first;
    printf("Printing in order\n"); 
    int num = 0;
    while (currr != NULL) {
        printf ("%d - > ", currr->value);
        currr = currr->next; 
        num++;
    }
    printf("%d elements\n", num);
}

void print_list_backwards(DLListRep *L) {
    struct DLListNode *currr = L->last;
    printf("L->last is %d\n", L->last->value);
    printf("L->last->last is %d\n", L->last->prev->value);
    printf("Printing in reverse\n"); 
    int num = 0;
    while (currr != NULL) {
        printf ("%d - > ", currr->value);
        currr = currr->prev; 
        num++;
    }
    printf("%d elements\n", num);
}


void remove_num(DLListRep *L, int num) {
    if (L->first->value == num) {
        remove_first(L); 
    } 
    if (L->last->value == num) {
        remove_last(L); 
    } else {
        remove_middle(L,num);     
    }

}

void remove_first(DLListRep *L) {
    struct DLListNode *temp = L->first; 
    L->first = temp->next; 
    L->curr = L->first; 
    free(temp);
}


void remove_last(DLListRep *L) {
    struct DLListNode *temp = L->last; 
    L->last = temp->prev;
    L->last->next = NULL;
    L->curr = L->last; 
    free(temp);

}

void remove_middle(DLListRep *L, int num) {
    struct DLListNode *curr = L->first; 
    struct DLListNode *previous;
    struct DLListNode *after; 
    struct DLListNode *temp; 
    while (curr != NULL) {
        if (curr != L->first && curr != L->last && curr->value == num) {
            temp = curr;
            previous = curr->prev; 
            after = curr->next; 
            previous->next = after;
            after->prev = previous;
            L->curr = previous;
            curr = previous;
            free(temp);
        }
    curr = curr->next; 
    }

}
