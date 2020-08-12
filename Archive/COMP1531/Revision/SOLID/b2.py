class TapeReader():
        def read():
                return input("Enter input from tape: ")
        
class Keyboard():
        def read():
                return input("Enter input from keyboard: ")

class Printer():
        def write(output):
                print(output)

# remember to set the tape_reader flag to true
class Copier():
        tape_reader = False
        def copy():
                if Copier.tape_reader:
                        val = TapeReader.read()
                else:
                        val = Keyboard.read()
                Printer.write(val)

Copier.tape_reader = True
Copier.copy()