from abc, import ABC, abstractmethod

class Course():
    def __init__(self, name, fee):
        self._name = name
        self._fee = fee
        
    def get_name(self):
        return self._name
        
    def get_fee(self):
        return self._fee
        
class RateScalar(ABC):
    
    def __init__(self):
        pass

    @abstractmethod
    def get_rate():
        pass


class LocalStudentRateScalar(RateScalar):
    def __init__(self):
        pass
        
    def get_rate(self):
        return 0.5


class SemesterEnrolent():
    def __init__(self, courses):
        self._courses = courses #given a list of Course objects on construction
     
    @abstractmethod
    # a method that changes depending on the dependency we inject into it   
    def generate_student_bill(self, rate_scalar):
        result = 0
        for course in self._courses:
            result += course.get_fee()*rate_scalar.get_rate() #some realised abstract class that has implemented this
    return result   
            
        
courses = [Course("COMP1531", 1000), Course("FINS1613", 4000)]
sem_e = SemesterEnrolment(courses)
#now we can call generate_student bill
sem_e.generate_student_bill(LocalStudentRateScalar()) #passing in the dependency when we call the method
