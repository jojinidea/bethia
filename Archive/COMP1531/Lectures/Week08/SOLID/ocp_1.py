from abc import ABC, abstractmethod
from srp_2 import ReportReader, EmailService

class ReportFormatter(ABC):

        @abstractmethod
        def format_report():
                pass

class PDFFormatter(ReportFormatter):
        def format_report(self,report_data):
                print("formatting for pdf")
                return "pdf formatted data"

class HTMLFormatter(ReportFormatter):
        def format_report(self,report_data):
                print("formatting for html")
                return '<HTML><BODY>......report_data </BODY></HTML>'

class Reporter(object):
    
    # This class is only responsible for the orchestration of the process to email a report
    
    def email_report_hours(self,email, time_period,emp_id):
        report_data = ReportReader.get_report_data(time_period, emp_id)
        formatter = HTMLFormatter()
        body = formatter.format_report(report_data)
        EmailService.send_email(email, body)

        
r = Reporter()
r.email_report_hours("a.nat@unsw.edu.au",12,1)

