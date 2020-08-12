class Job():
    def __init__(self, ID, date, Customer):
        self._ID = ID
        self._date = date
        self._Customer = Customer
    
    @property
    def ID(self):
        return self._ID

class JobManager():
    def __init__(self):
        self._Jobs = []
   
class Customer():
    def __init__(self, name, contact):
        self._name = name
        self._contact = contact

class System():
    def __init__(self, JobManager):
        self._JobManager = JobManager
    
    def notify(self, Notifier, Customer):
        Notifier.notify(Customer)

class Notifier(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def notify(Customer):
        pass

class EmailNotifier(Notifier):
    def __init__(self):
        Notifier.__init__()
    
    def notify(Customer):
        print("Notifying customer via email")

class SMSNotifier(Notifier):
    def __init__(self):
        Notifier.__init__()
    
    def notify(Customer):
        print("notifying customer via SMS")
        
