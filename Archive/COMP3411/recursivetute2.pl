% 1.  Write a prolog predicate insert(Num, List, NewList) that takes a number Num along with a list of numbers List which is already sorted in increasing order, and binds NewList to the list obtained by inserting Num into List so that the resulting list is still sorted in increasing order.

insert(Num,[],[Num]).
insert(Num, [H|T], [Num,H|T]):-
    Num =< H.
insert(Num, [H|T], [H|NewTail]):-
    Num > H,
    insert(Num, T, NewTail). % we want to insert Num in the correct position of T
    

%  Write a predicate isort(List,NewList) that takes a List of numbers in any order, and binds NewList to the list containing the same numbers sorted in increasing order. Hint: your predicate should call the insert() predicate from part .

isort([],[]).
isort([H|T], NewList):-
    isort(T, STail), % strips off head of list, recursively sorttail
    insert(H, STail, NewList). % then put head into correct position
    
%  Write a predicate split(BigList,List1,List2) which takes a list BigList and divides the items into two smaller lists List1 and List2, as evenly as possible (i.e. so that the number of items in List1 and List2 differs by no more that 1). Can it be done without measuring the length of the list?

split([],[],[]):-
split([A,B|T], [A|X], [B|Y]):-
    split(T, [A|X], [B|Y]).


% UNSURE
%  Write a predicate merge(Sort1,Sort2,Sort) which takes two lists Sort1 and Sort2 that are already sorted in increasing order, and binds Sort to a new list which combines the elements from Sort1 and Sort2, and is sorted in increasing order.

merge([],[],[]).
merge([A|Tail1], [B|Tail2], [A,B|TNL1]):-
    A =< B.
    merge(Tail1, Tail2, TNL1).
merge([A|Tail1], [B|Tail2], [B,A|TNL1]):-    
    B =< A.
    merge(Tail1, Tail2, TNL1).
    

