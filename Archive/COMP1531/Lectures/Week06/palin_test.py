import pytest
from palin import is_palindrome #imports the function is_palindrome from palin

def test_function_accepts_palindromic_input():
    input = "Noon"
    assert is_palindrome(input) == True
    
    ##assertion test expecting the above is true, but we don't have implementation of this function, so it will fail
    
def test_function_ignore_case():
    input = "Level"
    assert is_palindrome(input) == True
    
    ##assertion test with different input that isn't the 'normal' input
    
def test_function_ignore_space():
    input = "Too bad I hid a boot"
    assert is_palindrome(input) == True
