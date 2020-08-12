class SemesterEnrolment():
    def __init__(self):
        self._courses = []
     
    @property
    def courses(self):
        return self._courses
    
    def add_course(self, course):
        self.courses.append(course)
   
    def generate_bill(self, RateScalar): # the function that is previously dependent on the low-level modules should be injected with the Abstract Class
        result = 0
        for course in self.courses:
            result += course.fee * RateScalar.scale_factor() #RateScalar is an abstract class 
        
        return result
    

class Course():
    def __init__(self, name, fee):
        self._name = name
        self._fee = fee
    
    @property
    def name(self):
        return self._name
    
    @property
    def fee(self):
        return self._fee 
    

class RateScalar(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def scale_factor()
        pass

class International(RateScalar): #dependencies inherit from the abstract class
    def __init__(self):
        RateScalar.__init__(self):
    
    def scale_factor():
        return 2

class Scholarship(RateScalar):
    def __init__(self):
        RateScalar.__init__(self):
        
    def scale_factor():
        return 0.5
        
        
class Local(RateScalar):
    def __init__(self):
        RateScalar.__init__(self):
    
    def scale_factor():
        return 1

s = SemesterEnrolment()
s.generate_bill(Local())
s.generate_bill(International())
s.generate_bill(Scholarship())
# the dependency is the type of student/scalar
