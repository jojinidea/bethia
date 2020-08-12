import ABC, abstractmethod

class SemesterEnrolment(object):
    def __init__(self):
        self._courses = []
    
    def generate_bill(self, RateScalar):
        result = 0
        for course in self.courses:
            result += course.fee * RateScalar.getrate()
        
        return result

class RateScalar(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def getrate(self):
        pass
 
class InternationalStudent(RateScalar):
    def __init__(self):
        RateScalar.__init__()
    
    def getrate(self):
        return 2
        

            
