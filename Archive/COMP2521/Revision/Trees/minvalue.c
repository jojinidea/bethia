// min value of a tree is just the node at the bottom left

while (t != NULL) {
    t = t->left;
}
return t->key;
