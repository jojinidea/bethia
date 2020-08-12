// PREORDER Root-Left-Right
// 1. Visit root
// 2. Visit left subtree
// 3. Visit right subtree

void Preorder(struct Node *root) {
    if (root == NULL) {
        return;
    }
    printf("%d", root->data);
    Preorder(root->left); 
    Preorder(root->right);
    

}

//INORDER Left-Root-Right
// 1. Visit left subtree
// 2. Visit root
// 3. Visit right subtree

void Inorder(struct Node *root) {
    if (root == NULL) {
        return;
    }
    Inorder(root->left);
    printf("%d", root->data);
    Inorder(root->right);

}

// POSTORDER
// LEFT, RIGHT, ROOT
// 1. Visit left subtree
// 2. Visit right subtree
// 3. Visit root

void Postorder(struct Node *root) {
    if (root == NULL) {
        return;
    }
    Postorder(root->left);
    Postorder(root->right);
    printf("%d", root->data);
}

// Hackerrank Q: Tree Postorder Traversal 
// LEFT, RIGHT, ROOT 

void postOrder(Node *root) {
    if (root == NULL) {
        return; 
    }
    postOrder(root->left);
    postOrder(root->right);
    printf("%d ", root->data);


}

// Hackerrank Q: Tree Inorder Traversal
// LEFT, ROOT, RIGHT

void inOrder(Node *root) {
    if (root == NULL) {
        return;
    }
    inOrder(root->left);
    printf("%d ", root->data);
    inOrder(root->right);

}

















