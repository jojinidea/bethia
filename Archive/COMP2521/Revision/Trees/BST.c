// Binary search tree - search tree that is binary (each parent has at most 2 children) and left subtree <= parent and right subtree >= parent for all nodes
#define FALSE 0
#define TRUE 1

struct BSTNode {
    int data;
    struct BSTNode* left; // stores address of left child
    struct BSTNode* right; // stores address of right child

};

// these nodes will be created using malloc 
// we always keep address of the root node in all nodes

void Insert(BSTNode* root, int data); 

int main () {
    struct BSTNode *rootPtr; // pointer to node
    rootPtr = NULL; // empty tree
    
    Insert(root, 15);
    Insert(root, 10);
    Insert(root, 20);
    
}

void Insert(BSTNode* root, int data) {
    if (root == NULL) {
        root = GetNewNode(data);
        return root;
    } else { // need to insert in either LST or RST, can do this recursively
        if (data <= root->data) {
            root->left = Insert(root->left, data);
        } else if (data > root->data) {
            root->right = Insert(root->right, data);
        }
    }

}

bool Search (BSTNode *root, int data) {
    // think of this recursively
    if (root == NULL) {
        return FALSE;
    } 
    if (root == data) {
        return TRUE;
    } else {
        if (data >= root->data) {
            Search(root->right, data);
        } else {
            Search(root->left, data);
        }
    }

}
