from file_system import FileSystem
from service import Service
from member import Member
from provider import Provider
from datetime import datetime
from utility_functions import *


class ProviderTerminal():

    def __init__(self, file_system: FileSystem, id: int, provider: Provider):
        self.file_system = file_system
        self.id = id
        self.provider = provider
        # self.member = None
        # example - self.service_number = service_number.service_code 
        # self.service_name = service_name
        # self.service_number = 0
        # self.service_date = None
        # self.fileSystem = fileSystem
        # self.comments = None
        # self.providerID = providerID
        # self.memberID = memberID
        # self.fee = fee


    def get_member_status(self) -> str:
        print("Enter the member's ID: ")
        member_id = getInputNumberSafe(999999999)
        member = self.file_system.get_member_by_id(member_id)
        if member is None:
            print("***Invalid Number***\n")
            return "invalid"
        elif member.is_suspended:
            print("***Member suspended***\n")
            print(f"Reason: {member.first_name} has not paid "
                  "membership fees for at least a month")
            return "suspended"
        else:
            print("***validated***\n")
            return "valid"


    def generateReport(self, date, memberID, serviceCode):
        print(f"Current date and time: {date.strftime('%m-%d-%Y %H:%M:%S')}")
        print(
            f"Date service was provided: {date.strftime('%m-%d-%Y')}")
        print(f"Provider number: {self.providerID}")
        print(f"Member number: {memberID}")
        print(f"Service code: {serviceCode}")
        if (self.comments is not None):
            print(f"Comments: {self.comments}")


    def run(self):
        print("Provider Terminal Reached")
        while True:
            try:
                memberID = int(input("Enter the member's ID: "))
                break
            except ValueError:
                print("Invalid input")

        self.member = self.fileSystem.get_member_by_id(memberID)

        if (self.member is None):
            print("Invalid member ID.")
            exit()
        elif (self.member.is_suspended):
            print("Member has been suspended.")
            print(
                f"Reason: {self.member.first_name} has not paid membership fees for at least a month")
            exit()

        print("Validated")
        today = datetime.now()

        # call get service function

        # generate report
        while (True):
            print("Would you like to add a comment about the service?")
            print("1-Yes\n2-No")
            try:
                userIn = int(input("->"))
                break
            except ValueError:
                print("Invalid input try again")

        if (userIn == 1):
            self.comments = input(
                "Please enter your comments here (up to 100 characters): ")
            while (len(self.comments) > 100):
                print("You exceeded the 100 character limit. Please try again.")
                print(f"Here is what you wrote previously: {self.comments}")
                self.comments = input(
                    "Please enter your comments here (up to 100 characters): ")

        self.generateReport(today, memberID, 0)
        # Examples for runs, providerID: 263034389, memberID: 182191072


    # def get_service(self): adrian
    # get the info about the service
    def get_service(self):
        #self.service_number = Service()
        #self.service_number.service_code

        number = self.service_number

        while len(number <= 6):
         input("Enter the six digit service number: ")
         if len(number <= 6):
             print(f"The code entered is{number}.  The code is verified")
        else:
            print(f"Invalid entry.  Try again")

            name = self.fileSystem.get_service_name_by_code(number)
            while True:
                print(f"Since you entered{number} This means you're requesting \
                      {name}")
                
                if name is None:
                    print(f"Invalid.  Try again")

                else:
                    print(f"Entry is valid")
