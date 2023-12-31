from file_system import FileSystem
from service import Service
from provider import Provider
from datetime import datetime
from utility_functions import *
import datetime

class ProviderTerminal():

    def __init__(self, file_system: FileSystem, id: int, provider: Provider):
        self.file_system = file_system
        self.id = id
        self.provider = provider
        self.member = None
        self.service_date = None
        self.service_code = None
        self.service_name = None
        self.comments = None
        self.service_fee = None


    def get_member_status(self) -> str:
        print("Enter the member's ID: ")
        member_id = getInputNumberSafe(999999999)
        self.member = self.file_system.get_member_by_id(member_id)
        if self.member is None:
            print("***Invalid Number***\n")
            return "invalid"
        elif self.member.is_suspended:
            print("***Member suspended***")
            print(f"Reason: {self.member.first_name} {self.member.last_name} has not paid "
                  "membership fees for at least a month\n")
            return "suspended"
        else:
            print("***validated***\n")
            return "valid"


    def get_service_directory(self) -> None:
        print(self.file_system.get_service_directory_as_string())


    def record_service(self) -> None:
        status = self.get_member_status()
        if status != "valid":
            return
        while True:
            self.service_date = input("Please enter the date of service in the format: MM-DD-YYYY\n--> ")
            try:
                date = datetime.datetime.strptime(self.service_date, "%m-%d-%Y")
                if date.year >= 1900 and date.year <= 3000:
                    break
                print("Incorrect date format!\n")
            except:
                print("Incorrect date format!\n")

        self.get_service_directory()
        print("Please enter the six-digit service code for the service provided:")
        self.service_code = getInputNumberSafe(999999)
        self.service_name = self.file_system.get_service_name_by_code(self.service_code)
        if self.service_name is None:
            print("Invalid service code!")
            return
        print(f"Service selected: {self.service_name}")
        print("Is this correct? 1 = Yes  2 = No")
        match getInputNumberSafe(2):
            case 1:
                pass
            case 2:
                return
            case _:
                print("ERROR!")
        print("Would you like to enter comments about the service? 1 = Yes  2 = No")
        match getInputNumberSafe(2):
            case 1:
                self.comments = self._get_comments()
            case 2:
                self.comments = "None"
            case _:
                print("ERROR!")
        self.service_fee = self.file_system.get_fee_by_code(self.service_code)
        self._document_service()


    def _document_service(self):
        service = Service(self.service_date, self.provider, self.member, self.service_code,
                          self.service_name, self.comments, self.service_fee)
        self.file_system.document_service(service)


    def _get_comments(self) -> str:
        comments = input("Please enter your comments here (up to 100 characters): ")
        while len(comments) > 100:
            print("You exceeded the 100 character limit. Please try again.")
            comments = input("Please enter your comments here (up to 100 characters): ")
        return comments