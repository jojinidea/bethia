from abc import ABC, abstractmethod

class Car(ABC):

    def __init__(self, make, model, year, registration, daily_rental_fee, car_id):
        self._make = make
        self._model = model
        self._year = year
        self._registration = registration
        self._car_id = car_id
        self._daily_rental_fee = daily_rental_fee
        
    @abstractmethod
    def compute_rental_fee(self):
        pass
        
    @abstractmethod
    def calculate_discount(self):
        pass
        
    def get_make(self):
        return self._make
        
    def get_model(self):
        return self._model
            
    def get_year(self):
        return self._year
        
    def get_registration(self):
        return self._registration
        
    def get_car_id(self):
        return self._car_id
        
    def get_daily_rental_fee(self):
        return self._daily_rental_fee
    
    def set_make(self):
        self._make = make
        
    def set_model(self):
        self._model = model
    
    def set_year(self):
        self._year = year
        
    def set_registration(self):
        self._registration = registration
    
    def set_car_id(self):
        self._car_id = car_id
     
    def set_daily_rental_fee(self):
        self._daily_rental_fee = daily_rental_fee

    def __str__(self):
        return 'Make: {}, model {}, year {}, registration {}, car_ID {}, daily rental fee {}'.format(get_make(), get_model(), get_year(), get_registration(), get_car_id(), get_daily_rental_fee())
        
class SmallCar(Car):
    def __init__(self, make, model, year, registration, car_id, daily_rental_fee):
        super().__init(make, model, year, registration, car_id, daily_rental_fee)
        
    def calculate_discount(self):
        discount = 0;
        return discount

    def compute_rental_fee(self):
        rental_fee = (get_daily_rental_fee() * get_rental_period()) - calculate_discount()
        return rental_fee
        

class MediumCar(Car):
    def __init__(self, make, model, year, registration, car_id, daily_rental_fee):
        super().__init(make, model, year, registration, car_id, daily_rental_fee)
        
    def calculate_discount(self):
        discount = 0;
        return discount
        
    def compute_rental_fee(self):
        rental_fee = (get_daily_rental_fee() * get_rental_period()) - calculate_discount()
        return rental_fee
        

class LargeCar(Car):
    def __init__(self, make, model, year, registration, car_id, daily_rental_fee, discount):
        super().__init(make, model, year, registration, car_id, daily_rental_fee)
        self._discount = 0.05
    
    def calculate_discount(self):
        total_discount = 0
        if (get_rental_period() > 7):
            total_discount = 0.05 * get_daily_rental_fee() * get_rental_period()
        return total_discount      
  
    def compute_rental_fee(self):
        rental_fee = (get_daily_rental_fee() * get_rental_period()) - calculate_discount()
        return rental_fee


class PremiumCar(Car):
    def __init__(self, make, model, year, registration, car_id, daily_rental_fee, discount, premium):
        super().__init(make, model, year, registration, car_id, daily_rental_fee)
        self._premium = 0.15
        self._discount = 0.05

    def calculate_discount(self):
        total_discount = 0
        if (get_rental_period() > 7):
            total_discount = 0.05 * get_daily_rental_fee() * get_rental_period()*get_premium()
        return total_discount  
        
    def compute_rental_fee(self):
        rental_fee = (get_daily_rental_fee() * get_rental_period()*get_premium()) - calculate_discount()
        return rental_fee
        
        
class AdminStaff(): 
    def __init__(self, username, password):
        self._username = username
        self._password = password 
        
    def get_username(self):
        return self._username
    
    def get_password(self): 
        return self._password

    def set_username(self):
        self._username = username
    
    def set_password(self): 
        self._password = password

    def __str__(self):
        return 'Username: {}'.format(get_username())

class Manager(AdminStaff): 
    def __init__(self, username, password): 
        super().__init__(username, password)


