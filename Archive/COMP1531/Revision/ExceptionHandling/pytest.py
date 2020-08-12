from examq import UserInputError, validate_user_name #don't forget to import user-defined exception class & any functions we need
import pytest #don't forget to import pytest

def test_correct_input():
    input = "apple345"
    assert validate_user_name(input) == True

def test_validate_empty_user_name():
    input = ""
    with pytest.raises(UserInputError):
        validate_user_name(input) # test will pass if UserInputError is raised
    
def test_validate_space():
    input = "appl 345"
    with pytest.raises(UserInputError):
        validate_user_name(input)
    
def test_validate_too_long():
    input = "aksjdkasjdkajsdkjaksdjkajsdkajskdjaksdj"
    with pytest.raises(UserInputError):
        validate_user_name(input)
