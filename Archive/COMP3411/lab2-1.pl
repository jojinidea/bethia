% Descendant is a descendant of person if person is a parent of descendant

descendant(Person, Descendant) :-
    parent(Person, Child), %if Person is a parent of Child, then Child is a Descendent
    descendant(Child, Descendant). % find all other descendants of child
