class Reporter(object):
    
    # This class knows too much about how the report is generated, formatted and emailed
    # This class has many reasons to change i.e. many responsibilities
    # e.g., if the business logic behind the report changes, then the class is changed
    # e.g., if the configuration to the email server changes, the class is changed

    def email_report_hours(self,email, time_period,emp_id):
    
        report_data = self.get_report_data(time_period, emp_id)
        body = self.format_report(report_data)
        self.send_email(email, body)

    def get_report_data(self,time_period,emp_id):
        # Open connection to database
        # Prepare a SQL query based on business logic
        # Run the SQL query and parse the result set
        print("Generating the report data")
    
    def format_report(self,report_data):    
        print("Formating the report in PDF")
        return "formatted_report"

    def send_email(self,email,body):
        print("Configuring smtp server...sending report to:" + email)       

r = Reporter()
r.email_report_hours("a.nat@unsw.edu.au",12,1)


