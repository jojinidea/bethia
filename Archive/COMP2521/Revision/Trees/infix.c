void showBSTreeInfix(BSTree t) {
    
    if (t == NULL) {
        return; 
    }

    showBSTreeInfix(t->left);
    if (t->deleted == FALSE) {
        printf("%d", t->value);
    }
    showBSTreeInfix(t->right);

}

// infix is L, N, R
