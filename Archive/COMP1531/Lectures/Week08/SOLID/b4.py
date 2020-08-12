from abc import ABC, abstractmethod

class Reader(ABC):
        @abstractmethod
        def read():
                pass
class Writer(ABC):
        @abstractmethod
        def write():
                pass

class TapeReader(Reader):
        def read(self):
                return input("Enter input from tape: ")
class TapeWriter(Writer):
        def write(self,output):
                print(output)
        
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

#client code
reader = Keyboard()
writer = Printer()
Copier.copy(reader,writer)
Copier.copy(TapeReader(),TapeWriter())