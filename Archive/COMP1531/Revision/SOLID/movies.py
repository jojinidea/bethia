class Movie(ABC):
    
    def __init__(self, title, pricecode):
        self._title = title
        self_pricecode = pricecode

    @abstractmethod    
    def return_scalar(self):
    
        
        
class Rental():
    def __init__(self, movie, days_rented):
        self._movie = movie
        self._days_rented = days_rented

    def calculate_rental(self):
        rental_cost = Movie.scalar * self._days_rented
        

class Regular(Movie):
    def __init__(self, title, pricecode):
        Movie.__init__(self, title, pricecode):
    
    def return_scalar(self):
        return 2
        

class NewRelease(RentalType):
    def __init__(self, title, pricecode):
        Movie.__init__(self, title, pricecode):
   
    def return_scalar(self):
        return 3
        
        
class Children(RentalType):
    def __init__(self):
        Movie.__init__(self, title, pricecode)
        
    def return_scalar(self):
        return 1.5

movie = Regular("Gone with the wind", Movie.REGULAR)
rental = Rental(movie, 4)
print(rental.calculate_rental()) 
