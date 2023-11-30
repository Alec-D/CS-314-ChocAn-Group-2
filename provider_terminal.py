from file_system import *
from service import *
from member import *
from provider import *

class ProviderTerminal(Provider):

    def __init__(self, member, service_number, service_date, service_time, file_system, provider):
       
        self.member = member
        self.service_number = service_number
        self.service_date = service_date
        self.service_time = service_time
        self.file_system = file_system

      
    #def run_visit(self):
     

    def get_service(self):
        self.service_number = Service()
        self.service_number.service_code
        self.service_date = Service()
        self.service_date.current_date
        self.service_time = Service()
        self.service_time.current_time

        while True:
         code = input("Enter the six digit service number: ")
        
         print("You entered ",input)
         print("Checking if it's six digits",input.isdigit())
        
         if code == self.service_code:
            print("This is correct ")
            break

         else:
            print("Try again")

    

     
                

            

        





     

         #   def get_date_of_service(self):

       #  while True:

          #  return [self.service_date, self.service_time]
        # else:
               # print("Incorrect information!")
            

           
    #def get_member(self):
           

           

    #def document_service(self):

    
