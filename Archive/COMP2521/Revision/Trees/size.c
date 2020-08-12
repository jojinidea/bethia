int size(struct node *t) {

    if (t == NULL) {
        return 0;
    } else {
        return size(t->left) + size(t->right) + 1;  
        // size is size of left subtree + size of right subtree + 1 (for current node) 
    }
}
