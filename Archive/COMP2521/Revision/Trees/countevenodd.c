// for counting even: 
// if n == NULL, return;
// if n is even, return 1 + countEven(n->left) + countEven(n->right)
// if n is odd, return countEven(n->left) + countEven(n->right) 
// similar to Python Fibonacci exercise

    if (t == NULL) {
        return 0;
    } if (t->key % 2 == 0) {
        return 1 + countEven(t->right) + countEven(t->left);
    } else {
        return countEven(t->right) + countEven(t->left);
    }
    
    int countEven(BSTree t){
    int count = 0;
    if (t == NULL) {
        return 0;
    } else {
        count = countEven(t->left) + countEven(t->right); // enables us to reach furthest node and go up
        // if we put this at the end it won't work
        if (t->key % 2 == 0) {
            count ++; // don't want to return this
            printf("Count is %d\n", count);
            printf("T curr is %d\n", t->key);
        }
        return count;
    }
    
}

int countEven(BSTree t){
    if (t == NULL) {
        return 0;
    } else {
        printf("t->key is %d\n", t->key);
        if (t->key%2 == 0) {
            return 1;
        } else {
            return 0;
        }
    }
    return countEven(t->left) + countEven(t->right);
}

// THE ABOVE WILL NOT WORK BECAUSE THE FUNCTION WILL RETURN AT THE FIRST VALUE (DIFFERENT TO FIBONNACCI NUMBERS) !!
