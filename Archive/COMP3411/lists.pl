    % identifies if a given thing is a list
    
    is_a_list([]). % base case, is list empty
    is_a_list(.(Head, Tail)) :- % recursive case
        is_a_list(Tail).
        
    
    % separates list into head and tail
    head_tail(List, Head, Tail):-
        List = [A|B],
        Head = A,
        Tail = B.
        
    % test if an element is a member in a list
    is_member(Element, list(Element,_)). % base case - if element in head
    is_member(Element, list(_, Tail)):- % recursive case - if element is in tail
        is_member(Element, Tail).
 
    % concatenate two lists recursively
    % two cases, if list is empty and if it is not
    
    cons([], L2, Result):-
        Result = L2.
    
    cons(L1, [], Result):-
        Result = L1.
    
    cons([X|L1], L2, [X|L3]):- % split first list into head (first element) and L1. Result, [X|L3] will be head of L1 and L3
        cons(L1, L2, L3).
    
    
