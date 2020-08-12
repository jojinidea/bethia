import pytest
from product import Shirt, Pant, Electrical


def test_create_shirt():
    s = Shirt("Cool Shirt", 25.2, "S", "Red")
    assert(s.name == "Cool Shirt")
    assert(s.price == 25.2)
    assert(s.__str__() == "1: Cool Shirt, 25.2, S, Red, round")
    
    
