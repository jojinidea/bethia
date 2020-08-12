// given a BST, return true if a node with the target data is found

int lookup(struct node *node, int target) {
    //1. Base case == empty true
    if (node == NULL) {
        return(false);
    } else {
    // 2. See if found here
        if (target == node->data) {
            return(true);
   // 3. Otherwise recur down correct subtree
        } else {
            if (target < node->data) {
                return lookup(node->left, target);
            } else {
                return lookup(node->right, target);
            }
        
        }
    
    }

}

// 1. Base case (tree is empty)
// 2. Deal with current node
// 3. Use recursion to deal with subtrees (need to know if we should move left or right) 
