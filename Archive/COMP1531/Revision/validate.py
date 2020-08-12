def validate_user_name(username):
    if len(username) < 1 or len(username) > 25 or username.find(" ") != -1:
        raise UserInputError
    else:
        return True
        
        
class UserInputError(Exception):
    "raised when a user input error occurs"
    pass

from validate import *
from UserInputError import *

def test_valid_input():
    username = "valid"
    assert(validate_user_name(username) == True)

def test_invalid_length_short():
    username = ""
    with pytest.raises(UserInputError) as info:
        validate_user_name(username)

def test_invalid_length_long():
    username = "askdjaksjdkajsdkjaskdjaksjdaksd"
    with pytest.raises(UserInputError) as info:
        validate_user_name(username)

def test_invalid_space():
    username = " "
    with pytest.raises(username) as info: #CATCH THE EXCEPTION!!! 
        validate_user_name(username)

    
