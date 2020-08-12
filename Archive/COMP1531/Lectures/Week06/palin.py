def is_palindrome(letters):
    letters = [c for c in letters.lower() if c.isalpha()]
    return letters == letters[::-1] 
    
#with test-driven development, don't provide implementation first
