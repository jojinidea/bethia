int add (BSTree t) {
    if (t == NULL) {
        return 0; 
    } else {
        return t->data + add(t->left) + add(t->right);
    }

}

// think on the microscopic level - we want to add t->data (current node) + sum of values in left subtree + sum of values in right subtree
// always think of ONE node and then recursive structure (curr + left subtree + right subtree)
