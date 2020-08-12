// LEVEL ORDER - need a queue to implement this

void BSTreeLevelOrder(BSTree t) {
    Queue Qt = newQueue();
    if (t != NULL) {
        QueueJoin(Qt, t); 
    }
    while (QueueIsEmpty(Qt) != TRUE) {
        Item popped = QueueLeave(Qt);
        printf("%d ", popped->data);
        if (popped->left != NULL) {
            QueueJoin(Qt, popped->left);
        }
        if (popped->right != NULL) {
            QueueJoin(Qt, popped->right);
        }
    
    }


}
