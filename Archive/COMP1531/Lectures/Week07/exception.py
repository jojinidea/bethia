try:
    file = open("test.txt", "r")
    file.read() #test.txt does not exist, exception occurs, so jumps to line 5
except IOError:
    print("Error occured in reading from file")
else:
    print("Successfully read the file")
finally:
    print("All done")

try: 
    num = int(input("enter numerator:"))
    den = int(input("enter denominator:"))
    result = num/den
except ValueError: 
    print("Enter numbers only")
except ZeroDivisionError: 
    print("Division by zero not possible")
else:
    print("You entered nos {}, {} and the result is {}".format(num, den, result))
finally:
    print("run")

try:
    file = open("testfile", "w")
    file.write("some writing to a testfile")
except IOError:
    print("Error occured in writing to file")
else:
    print("Successfully written to the file")
finally:
    print("All done")
