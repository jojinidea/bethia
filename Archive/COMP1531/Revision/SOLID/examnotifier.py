class Notifier(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def notify(self):
        pass
        
class EmailNotifier(Notifier):
    def __init__(self):
        Notifier.__init__(self):
    
    def notify(self):
        "Emailed client"

class SMSNotifier(Notifier):
    def __init__(self):
        Notifier.__init__(self):
   
    def notify(self):
        "SMSed client"
