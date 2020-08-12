// is BST 


int isBST(BSTree t) {
    if (t == NULL) {
        return 1;
    }
    if (isBST(t->left) && isBST(t->right) && isSubtreeGreater(t->right, t->data) && isSubtreeLesser(t->left, t->data)) {
        return 1;
    }
    return 0;
}

int isSubtreeGreater(BSTree t, int data) {
    if (t->data > data) {
        return 1;
    } 
    if (isSubtreeGreater(t->left, t->data) && isSubtreeGreater(t->right, t->data) && t->data > data) {
        return 1;
    }   
    return 0;
    
}

int isSubtreeLesser(BSTree t, int data) {
    if (t == NULL) {
        return 1;
    }
    if (t->data < data && isSubtreeLesser(t->left, t->data) && isSubtreeLesser(t->right, t->data)) {
        return 1;    
    }
return 0;
}
