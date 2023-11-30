from file_system import FileSystem
from employee import Employee

class User:
    """

    Class to handle all login functionalities for employees and providers

    """
    fileSystem = FileSystem("member_data.csv", "provider_data.csv",
                      "service_dir.csv", "employee_data.csv")

    def __init__(self, ID):
        self.ID = ID
        self.userType = None

    def isValid(self):
        if (self.userType == "employee"):
            return self.fileSystem.is_valid_employee(self.ID)
        elif (self.userType == "provider"):
            return self.fileSystem.get_provider_by_id(self.ID)
        else:
            return False
    
    @staticmethod
    def getInputNumberSafe(numOptions: int) -> int:
        while True:
            response = input("--> ")
            print("-------------------------------------------------")
            try:
                response = int(response)
                # if response in range(1, numOptions+1):
                if response >= 1 and response <= numOptions:
                    return response
            except:
                pass
            print(f"Please enter a number between 1 and {numOptions}!")

    def loginUI(self):
        while True:
            print("\nWelcome to the ChocAn Terminal System\n")
            print("Please choose an option below by entering a number between 1 and 3")
            print("1. I am a ChocAn Employee")
            print("2. I am a Provider")
            print("3. Exit")
            userInput = self.getInputNumberSafe(3)
            match userInput:
                case 1:
                    self.userType = "employee"
                case 2:
                    self.userType = "provider"
                case 3:
                    return
                case _:
                    print("ERROR!!!")
            print(f"Please enter your {self.userType} ID: ")
            self.ID = self.getInputNumberSafe(999999999)
            if self.isValid() == None or not self.isValid():
                print("ID not registered within our system!")
                continue
            else:
                print("Access Granted")
                self.accessGranted()
    
    def accessGranted(self):
        while True:

            # TODO: if employeee, display employee info and permissions
            # TODO: call employee terminal or provided terminal

            if self.userType == "employee":
                emp = Employee(self.ID)
                option = emp.displayOptions()
                if option == 1:  # add member
                    emp.add_member()
                elif option == 2:  # edit member
                    emp.edit_member()
                elif option == 3:  # delete member
                    memberID = int(input("Please enter the member ID: "))
                    emp.delete_member(memberID)
                elif option == 4:  # add provider
                    emp.add_provider()
                elif option == 5:  # edit provider
                    emp.edit_provider()
                elif option == 6:  # delete provider
                    providerID = int(input("Please enter the member ID: "))
                    emp.delete_provider(providerID)
                elif option == 7:
                    return

            else:  # user is a provider
                # call provider terminal
                pass

    # fileSystem.save_dirs()
