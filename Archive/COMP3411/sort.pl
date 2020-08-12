% insertInPlace(ELEMENT, LIST, RESULT)
% RESULT is the result of inserting ELEMENT into sorted list LIST
% at the correct place.

insertInPlace(ELEMENT, [], [ELEMENT]). % base case - empty list
insertInPlace(ELEMENT, [HEAD|TAIL], [ELEMENT|LIST]) :- 
   ELEMENT =< HEAD, insertInPlace(HEAD, TAIL, LIST).
insertInPlace(ELEMENT, [HEAD|TAIL], [HEAD|LIST]) :-
   ELEMENT > HEAD, insertInPlace(ELEMENT, TAIL, LIST). % if the number is greater than the head, we dont know what the rest of the list will be so use variable List
   
   
isort([], []).
isort([H|T], NewList):-
    isort(Tail, STail), 
    insert(H, STail, NewList).


The isort predicate strips off the head of the list, sorts the
tail recursively, then finally inserts the head item (X) into
the correct location.
The recursion stops when the list to be sorted become
empty.
We must now define the insert predicate. 

isort([H|T], NewList):-
    isort(Tail, X), % sort tail of list to get sorted tail
    insert(H, X, NewList). % insert head into sorted tail to get new list

split([H|T], List1, List2)
    

Read as "appending list A and list B results in original list L, length of A is some value N and also length of B is the same value N".


