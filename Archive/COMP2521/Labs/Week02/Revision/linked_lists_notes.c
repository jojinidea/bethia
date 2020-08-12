struct node {
    int data;
    struct node *next; 
};

struct node *node_one = malloc(sizeof(struct node));
// gives us a pointer to a struct

node_one->value = 1;
node_one->next = address of struct two

// *node_two is a pointer which means it stores an address, we do not need to dereference node_two with an &

struct node *current;
current->next = head; 
// current is a pointer to a struct node (arrow has no direction)
// current->next = head - points to head (arrow has a direction)
