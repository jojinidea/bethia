void rn(int n) {
    if (n == 0) {
        return;
    }
    int i;
    for (i = 0; i < n - 1; i++) {
        if (b[i+1] > b[i]) {
        // swap the two values
        int j = b[i+1];
        b[i+1] = b[i];
        b[i] = j;
        
        }
    
    }

rb(n-1);

}
