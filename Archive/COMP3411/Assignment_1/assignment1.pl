% Assignment 1 - Prolog Programming
% Bethia Sun, z5165555

% Question 1: Sum the squares of only the even numbers in a list of integers. 

% even(X) and odd(X) checks if X is an odd or even number 

even(X):- 
    0 is X mod 2.
odd(X):-
    1 is X mod 2.

% sumsq_even(List, Result), sums the squares of only even numbers in a list and binds the result to Result

sumsq_even([], 0). % base case - if the list is empty, sum is 0
sumsq_even([H|T], Sum):- % recursive case - if H is even, we add it to the Sum of the Tail, which we find recursively
    even(H),
    sumsq_even(T, SumTail),
    Sum is SumTail+H*H.
sumsq_even([H|T], Sum):- % recursive case - if H is odd, we do not add it to the Sum of the Tail, and continue to find the sum recursively
    odd(H),
    sumsq_even(T, Sum).
    

% Question 2: Write a predicate same_name(Person1,Person2) that succeeds if it can be deduced from the facts in the database that Person1 and Person2 will have the same family name. A person has the same family name as their father. Married women retain their original birth name. 

% ancestor(A,B) is a predicate to check if A is an ancestor of B.

ancestor(A,A). % base case - every person is their own ancestor
ancestor(A,B):- % base case - a parent of a person is their ancestor
    parent(A,B).
ancestor(A,B):- % recursive case - if A is the parent of X and X is an ancestor of B, then A is an ancestor of B
    parent(A,X),
    ancestor(X,B).

% to check if Person1 and Person2 have the same family name, check if they have a common ancestor that is male. If so, they have the same family name    

same_name(Person1, Person2):- 
    ancestor(CommonAncestor, Person1),
    ancestor(CommonAncestor, Person2),
    male(CommonAncestor). 

% Question 3: Write a predicate sqrt_list(NumberList, ResultList) that binds ResultList to the list of pairs consisting of a number and its square root, for each number in NumberList. 

sqrt_list([],[]). % base case - if NumList is empty, ResultList is also empty
sqrt_list([H|T],[[H,T1]|Lists]):- % recursive case - find the 2 element sublists recursively
    T1 is sqrt(H),
    sqrt_list(T, Lists).
    
% Q4 Write a predicate sign_runs(List, RunList) that converts a list of numbers into the corresponding list of sign runs. % doesnt work with -X X -X

% same_sign is a predicate that checks if the two inputs are of the same sign

same_sign(First, Second):-
    First >= 0,
    Second >= 0.
same_sign(First, Second):-
    First < 0,
    Second < 0.
    
sign_runs([],[[]]). % base case - if list is empty, we have a empty sublist within a list
sign_runs([H],[[H]]). % base case - if list has one element, we have a 1 element sublist
sign_runs([H1,H2|Tail], [[H1|List]|Rest]):- % recursive case if H1 and H2 are the same
    same_sign(H1,H2),
    sign_runs([H2|Tail], [List|Rest]).
sign_runs([H1,H2|Tail],[[H1],List|Rest]):- % recursive case if H1 and H2 are not the same
    not(same_sign(H1,H2)),
    sign_runs([H2|Tail],[List|Rest]).
    
% Q5: Write a predicate is_heap(Tree) which returns true if True satisfies the heap property

% smaller tests if the current value, CurrVal is smaller than the value at a node

smaller(empty,_).
smaller(tree(_,NodeVal,_),CurrVal):-
    CurrVal < NodeVal. 
    
is_heap(empty). % base case - if tree is empty, must be a heap
is_heap(tree(Left,Val,Right)):- % recursive case - check that the value of the left and right nodes are smaller than the current node
    smaller(Left,Val),          % then recurr down the left subtree and right subtree to make sure this property holds for the left and right subtrees
    smaller(Right,Val), 
    is_heap(Left), 
    is_heap(Right).
    
    
    
% TESTING
% :- begin_tests(sumsq_even).

% tests for Q1 sumsq_even: 
% if the list is empty, expect sum = 0
% if the list contains zero even integers, expect sum = 0
% if the list contains a few even integers, expect sum = sum of the squares of all even integers in list
% if the list contains negative even integers, expect sum = sum of the squares of even integers in list

% test(sumsq_even):-
%    sumsq_even([],0),
%    sumsq_even([3,9,13,15],0),
%    sumsq_even([2,4,10,3,7,11],120),
%    sumsq_even([-2,-4,3,7,15],20).


% tests for Q2 same name (tested manually through terminal with family.pl facts)
% if the two inputs are the same person, expect true 
% if the two inputs are not related by blood (e.g. husband/wife, otherwise not blood related), expect false 
% if the two inputs are immediate father child, expect true
% if the two inputs are immediate mother child, expect false
% if the two inputs have a common male ancestor, expect true


% tests for Q3 sqrt_list:
% if NumberList is empty, expect ResultList = empty list
% if NumberList has one element, expect ResultList to contain 1 element that is a list containing the element & the square root of the element
% if NumberList has multiple elements, expect ResultList to contain multiple lists that contain each element-square root pair

%:- begin_tests(sqrt_list).

% test(sqrt_list):-
%    sqrt_list([],[]),
%    sqrt_list([4],[[4,2.0]]),
%    sqrt_list([0,2,4,16,25],[[0, 0.0], [2, 1.4142135623730951], [4, 2.0], [16, 4.0], [25, 5.0]]).
    
% tests for Q4 sign_runs
% test if list is empty - expect [[]]
% test if list has one element - expect [[E]]
% test if list has all elements of same sign - expect [[S1,S2...Sn]]
% test if list has element of different sign at the end - expect [[S1,S2...Sn],[Sdiff]]
% test if list has element of different sign at the start - expect [[Sdiff],[S1,S2..Sn]]
% test if list has element of different sign in the middle - expect [[S1,S2..Sdiff-1],[Sdiff], [Sdiff+1...Sn]]
% test multiple elements of different sign scattered randomly

%:- begin_tests(sign_runs).
    
% test(sign_runs):-
%    sign_runs([],[[]]),
%    sign_runs([5],[[5]]),
%    sign_runs([1,2,3,4,5],[[1,2,3,4,5]]),
%    sign_runs([1,2,3,4,-5],[[1,2,3,4],[-5]]),
%    sign_runs([1,-2,-3,-4,-5],[[1],[-2,-3,-4,-5]]),
%    sign_runs([1,2,-3,4,5],[[1,2],[-3],[4,5]]),
%    sign_runs([1,2,-3,-4,5,-6,-7,8,9,0],[[1,2],[-3,-4],[5],[-6,-7],[8,9,0]]).
    
% tests for Q5 is_heap (tested manually through terminal):
% if the tree is empty, expect is_heap to return true Y
% if the tree has one element (i.e. only the root), expect is_heap to return true Y
% if the tree has many nodes but one of the parents is less than one of its children, return false Y
% if the tree has many nodes but one of the parents is less than both children, return false Y
% if the tree has many nodes and all of the parents are greater than both of their children, return true Y

