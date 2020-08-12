class TapeWrite():
        def write(user_input):
                print(user_input)
class TapeReader():
        def read():
                return input("Enter input from tape: ")
        
class Keyboard():
        def read():
                return input("Enter some characters from keyboard: ")

class Printer():
        def write(output):
                print(output)

# remember to set the tape_reader flag to true if you want to read from tape
# remember to set the punch_writer flag to true if you want to write to tape
class Copier():
        tape_read = False
        tape_write = False
        def copy():
                if Copier.tape_read:
                        val = TapeReader.read()
                else:
                        val = Keyboard.read()
                if Copier.tape_write:
                        TapeWrite.write(val)
                else:
                        Printer.write(val)

Copier.tape_read = True
Copier.tape_write = True
Copier.copy()
#wants to read from keyboard
Copier.copy()
