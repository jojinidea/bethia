class Copier():
    def Copy():
        val = Keyboard.Read()
        Printer.Write(val)

class Keyboard():
    def Read():
        return input("Enter the number")

class Printer():
    def Write(user_input):
        print(user_input)


Copier.Copy()

