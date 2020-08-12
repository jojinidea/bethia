class Customer():
    def __init__(self, name, contact):
        self._name = name
        self._contact = contact
 
    @property
    def name(self):
        return self._name
    
    @property
    def contact(self):
        return self._contact

class Job():
    def __init__(self, ID, date, completed, Customer):
        self._ID = ID
        self._date = date
        self._completed = completed
        self._Customer = Customer

    @property
    def ID(self):
        return self._ID
    
    @property
    def date(self):
        return self._date
    
    @property
    def completed(self):
        return self._completed
    
    @property
    def Customer(self):
        return self._Customer
        
class JobManager():
    def __init__(self):
        self._jobs = []
    
    def add_job(self, Job):
    def delete_job(self, ID):
    def return_job(self, ID):
    def complete_job(self, ID):
    def notify_cust(self, Job, Notifier): 
        Notifier.notify(Job.customer)

class System():
    def __init__(self, JobManager):
        self._JobManager = JobManager
    
    @property
    def JobManager(self):
        return self._JobManager

class Notifier(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def notify(self, customer):
        pass

class EmailNotiication(Notifier):
    def __init__(self):
        pass
    
    def notify(self, customer):
        print("Job finished. Sending email to %s..." %(Customer.name))

class SMSNotiication(Notifier):
    def __init__(self):
        pass
        
    def notify(self, customer):
        print("Job finished. Sending email to %s..." %(Customer.name))

