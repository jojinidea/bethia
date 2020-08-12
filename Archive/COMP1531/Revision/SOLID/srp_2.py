class Reporter(object):
    
    # This class is only responsible for the orchestration of the process to email a report
    
    def email_report_hours(self,email, time_period,emp_id):
        report_data = ReportReader.get_report_data(time_period, emp_id)
        body = ReportFormatter.format_report(report_data)
        EmailService.send_email(email, body)

# Decompose responsibilities into separate independent classes
class ReportReader:
    def get_report_data(time_period,emp_id):
        # Open connection to database
        # Prepare a SQL query 
        # Run the SQL query and parse the result set
        print("Generating the report data")

class ReportFormatter:   
    def format_report(report_data):
        print("Formating the report in PDF")
        return "formatted data"

class EmailService:
    def send_email(email,body):
        print("Configuring smtp server...sending report to:" + email)
        
##r = Reporter()
##r.email_report_hours("a.nat@unsw.edu.au",12,1)
