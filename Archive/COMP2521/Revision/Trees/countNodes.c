int BSTreeNumNodes(BSTree t) {
    if (t == NULL) {
        return 0;
    } else {
        if (t->deleted == FALSE) {
            return 1 + BSTreeNumNodes(t->left) + BSTreeNumNodes(t->right);
        }
        return BSTreeNumNodes(t->left) + BSTreeNumNodes(t->right);
        // current node + num nodes in left subtree + num nodes in right subtree
    }


}
