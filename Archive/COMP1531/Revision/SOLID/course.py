class SemesterEnrolment():
    def __init__(self):
        self._courses = []
        
    @property
    def courses(self):
        return self._courses
    
    def add_course(self, course):
        self.courses.append(course)
    
    def generate_bill(self, RateScalar):
        result = 0
    
        for course in self.courses:
            result += course.fee * RateScalar.get_rate()
        
        return result
        
        
class RateScalar(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def get_rate(self):
        pass

class International(RateScalar):
    def __init__(self):
        RateScalar.__init__(self):
    
    def get_rate(self):
        return 2

s = SemesterEnrolment()
print(s.generate_bill(International))
