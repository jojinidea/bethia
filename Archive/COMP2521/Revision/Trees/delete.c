struct Node *Delete(struct Node *root, int data) {
    if (root == NULL) {
        return root;
    } else if (data < root->data) // in left subtree {
        // delete data in left subtree 
        root->left = Delete(root->left, data);
        // root of left subtree may change after deletion, delete function will return modified address of root of left subtree, so set root->left = Delete(root->left, data)
    } else if (data > root->data) {
        root->right = Delete(root->right, data);
    } else {    // if we are at the child
        // case 1: no child
        if(root->left == NULL && root->right == NULL) {
            free(root);
            root = NULL;
            return root;
            // link will be corrected
        } else if (root->left == NULL) {
            // case 2: one child
            struct Node *temp = root;
            root = root->right;
            free(temp);
            return root;
        } else if (root->right == NULL) {
            struct Node *temp = root;
            root = root->left; 
            free(temp);
            return root;    
        } else {
            // two children - need to search for minimum element of subtree
            struct Node *temp = FindMin(root->right);
            root->data = temp->data; // set data in node to min value
            root->right = Delete(root->right, temp->data); // delete duplicate
        
        }
        
    
    
    }


}
