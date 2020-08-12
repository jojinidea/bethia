class System():
    def __init__(self, JobManager):
        self._JobManager = JobManager
    
    @property
    def JobManager(self):
        return self._JobManager
    
    def NotifyCustomer(self, Job, Notifier):

class JobManager():
    def __init__(self):
        self._jobs = []
    
    @property
    def jobs(self):
        return self._jobs
    
    def delete_job(self, ID):
    
    def add_job(self, Job):
    
    def get_Cust(self, Job):
    
    def mark_job_complete(self, Job):
    
class Job():
    def __init__(self, ID, date, Customer, completed):
        self._ID = ID
        self._date = date
        self._Customer = Customer
        self._completed = completed

    @property
    def ID(self):
        return self._ID
    
    @property
    def date(self):
        return self._date
    
    @property
    def Customer(self):
        return self._Customer
    
    @property
    def completed(self):
        return self._completed

class Customer():
    def __init__(self, name, email):
        self._name = name
        self._email = email
    
    @property
    def name(self):
        return self._name
    
    @property
    def email(self):
        return self._email

class Notifier(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def notify_cust(self):
        pass
        
class EmailNotifier(Notifier):
    def __init__(self):
        Notifier.__init__(self):
    
    def notify_cust(self):
    # implementation

class SMSNotifier(Notifier):
    def __init__(self):
        Notifier.__init__(self):
    
    def notify_cust(self):
    # implementation
    
