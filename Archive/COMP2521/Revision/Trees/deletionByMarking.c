BSTree BSTreeDelete(BSTree t, int value) {
    if (t == NULL) 
    else if (value < t->value) {
        BSTreeDelete(t->left, value);
    } else if (value > t->value) {
        BSTreeDelete(t->left, value);
    } else if (value == t->value) {
        t->deleted = TRUE;
    }
    
    // search for node we want to delete
    // then if found, mark deleted

}

// why do we have to do t->left = BSTreeDelete(t->left, v) ?? because we aren't actually changing the links in the the BST... ? 
