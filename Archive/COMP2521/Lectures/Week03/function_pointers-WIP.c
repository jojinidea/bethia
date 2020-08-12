#include <stdio.h> 
#include <stdlib.h>

struct listnode {
    
    struct listnode *next; // creates a pointer called next of the type listnode 
    int value;
    char *name;
    
};

struct listnode *create_new_node (int value, char *name);
struct listnode *create_linked_lisit(int value1, int value2, int value3, char *name1, char *name2, char *name3);
void traverse_linked_list (struct listnode *first);

int main (void) {
    int value1 = 0;
    int value2 = 0;
    int value3 = 0; 
    int value4 = 0;
    char *name1 = NULL;
    char *name2 = NULL;
    char *name3 = NULL;

    printf("Enter three values and names\n");
    scanf("%d", &value1);
    scanf("%d", &value2);
    scanf("%d", &value3);
    scanf("%s", name1);
    scanf("%s", name2);
    scanf("%s", name3);
    
    //struct listnode *first = create_linked_lisit(value1, value2, value3, name1, name2, name3);
    //traverse_linked_list(first);

return 0;

}


struct listnode *create_new_node (int value, char *name) {
    struct listnode *new = malloc(sizeof(struct listnode));
   
    new->next = NULL;
    new->value = value;
    new->name = name;
    
    return new;
 
}

struct listnode *create_linked_list(int value1, int value2, int value3, char *name1, char *name2, char *name3) {
    
    struct listnode *head = NULL;
    struct listnode *temp = NULL;
    struct listnode *first = NULL;
    
    int i = 0;
    while (i < 3) {
        if (head == NULL) {
            head = create_new_node(value1, name1);
            first = head;
        } else {
            temp = create_new_node(value2, name2);
            head->next = temp;
            head = temp;
        } 
    
    } 

return first;

}
    

void traverse_linked_list (struct listnode *first) {
    struct listnode *curr = first;
    
    while (curr != NULL) {
        curr = curr->next;
    }

}
