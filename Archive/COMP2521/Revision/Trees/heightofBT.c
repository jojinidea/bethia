// binary tree is one with at most 2 children per parent
// height is the longest root to leaf path (WITHOUT the nodes) 
// we can break this problem down - find height of LST and height of RST, return the largest one of the two

int height(Node* root) {
    int height = 0;
    if (root == NULL) {
        return -1;
    } else {
        int LH = height(root->left) + 1; 
        int RH = height(root->right) + 1;
        // WE WANT TO add 1 everytime we go down one level
    }
    if (LH >= RH) {
        return (LH);
    } else {
        return (RH); // CANNOT PUT -1 here otherwise everytime we call the function this happens
    }
    // evaluate the expression, if TRUE, return first thing, if false, return second
    

}

// OR

int height(BSTree t) {

    if (t == NULL) {
        return 0;
    } else if (t->left == NULL && t->right == NULL) {
        return 0;   // this way, we aren't adding one for a leaf node!
    } else {
        int l = height(t->left);
        int r = height(t->right);
        if (l > r) {
            return l + 1;
        } 
        return r + 1;   
    }




}
