int BSTreeFind(BStree t, int v) {
    if (t == NULL) {
        return 0; 
    } else {
        if (t->value == v && t->deleted != TRUE) {
            return 1; 
        }
        if (t->value > v) {
            return BSTreeFind(t->right, v);
        } 
        if (t->value < v) {
            return BSTreeFind(t->left, v);
        }
    
    }
    return 0;// if we get out of the while loop it means we haven't found it
}

// OR
if (t == NULL) 
    return 0
else if (v < t->value) 
    return BSTreeFind(t->left, v);
else if (v > t->value)
    return BSTreeFind(t->right, v);
else if (t->deleted)
    return 0
else if (v== t->value && !t->deleted)
    return 1;
    
