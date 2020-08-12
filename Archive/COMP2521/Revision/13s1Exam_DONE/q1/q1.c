// q1.c ... Question 1 in COMP1927 13s1 Final Exam
// Find maximum value in an array via recursive divide-and-conquer

#include <stdlib.h>
#include <stdio.h>

#define MAXARRAY 1000


int main(int argc, char **argv)
{
	int array[MAXARRAY];  // array storage
	int n;  // count of elements in array
	int val;  // next value read from stdin
	int ArrayMax(int *, int);

	// read array contents from stdin
	n = 0;
	while (fscanf(stdin,"%d",&val) == 1)
		array[n++] = val;

	// display maximum value
	if (n > 0)
		printf("Max = %d\n", ArrayMax(array,n));
	else
		printf("Array is empty\n");

	return 0;
}

// find maximum value in a[0..n-1]
int ArrayMax(int a[], int n)
{
	int max(int *, int, int);

	return max(a, 0, n-1);
}

// recursive function to find maximum in a[lo..hi]
int max(int a[], int lo, int hi)
{
    // base case: max of a single item array is that single item
    // max of an array is max of the first item or max of the rest
    
    if (lo + 1 == hi) {
        if (a[lo] > a[hi]) {
            return a[lo];
        }
        return a[hi];
    } else {
        int leftMax = max(a, lo, (hi+lo)/2);
        int rightMax = max(a, (hi+lo)/2, hi);
        if (leftMax > rightMax) {
            printf("Left max is %d\n", leftMax);
            return leftMax; 
        } else {     
            printf("Right max is %d\n", rightMax);
            return rightMax;
        }   
    }
  
// don't try and think too much, just think recursively
// the max of an element is the max of the first element and the remaining n -1 elements
// base case, if we have two elements, return the largest of those two elements

if (hi - lo = 1) {
    if (a[hi] > a[lo]) {
        return a[hi];
    }
    return a[lo];
} else {
    int leftMax = max(a, lo, (hi+lo)/2);
    int rightMax = max(a, lo, (hi+lo)/2);
    if (leftMax > rightMax) {
        return leftMax;
    } else {
        return rightMax;
    }

}

}

int sum(int a[], int n) {
    if (n == 0) {
        return 0;
    } else {
        return (sum(a, n-1) + a[n-1]);
    }
    // the sum of something is the sum of the first n-1 elements and the sum of the n-1th element
    // base case - if n = 0, return 0
}

