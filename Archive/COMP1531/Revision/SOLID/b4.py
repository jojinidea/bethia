from abc import ABC, abstractmethod

class Reader(ABC):
        @abstractmethod
        def read():
                pass

#abstract class called reader with read method

class Writer(ABC):
        @abstractmethod
        def write():
                pass

#abstract class called writer with write method

class TapeReader(Reader):
        def read(self):
                return input("Enter input from tape: ")
#overwrites read method

class TapeWriter(Writer):
        def write(self,output):
                print(output)
#overwrites write method

class Keyboard(Reader):
        def read(self):
                return input("Enter input from keyboard: ")

class Printer():
        def write(self,output):
                print(output)

# remember to set the tape_reader flag to true
class Copier():
        def copy(reader,writer):
                value = reader.read()
                writer.write(value)

#copier module uses dependency injection so that it is passed in the appropriate reader type and writer type (what it's dependent on)


#client code
reader = Keyboard()
writer = Printer()
Copier.copy(reader,writer)
Copier.copy(TapeReader(),TapeWriter())
