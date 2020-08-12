/*
an empty tree has width zero
a tree with just one node has width three (to keep reasonable spacing)
all other trees have width which is three more than the combined width of the subtrees
*/

int BSTWidth(BStree t) {
    if (t == NULL) {
        return 0;
    } else if (t->left == NULL || t->right == NULL) {
        return 3;
    } else {
        return BSTWidth(t->left) + BSTWidth(t->right) + 3;
    }

}
