class UserInputError(Exception)
    "Raised when the user-name field is invalid"
    pass

def validate_user_name(user_name):
    # length >= 1 and <= 25, does not contain a space
    if (user_name.find(" ") != -1):
        raise UserInputError("User input error") #this will print out when the exception is raised
    if len(user_name) < 1:
        raise UserInputError("User input error")
    if (len(user_name) > 25:
        raise UserInputError("User input error")
        
#b) equvialence classes:
# 1. Valid name. Length between 1 and 25 not containing space
# 2. Invalid name. Length < 1
# 3. Invalid name. Length > 25
# 4. Contains space


