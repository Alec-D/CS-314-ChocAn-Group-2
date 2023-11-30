from file_system import FileSystem
from employee import Employee
from utility_functions import *


class User:
    """

    Class to handle all login functionalities for employees and providers

    """

    def __init__(self, id):
        self.id = id
        self.userType = None
        self.fileSystem = FileSystem("member_data.csv", "provider_data.csv",
                                     "service_dir.csv", "employee_data.csv")

    def isValid(self):
        if (self.userType == "employee"):
            return self.fileSystem.is_valid_employee(self.id)
        elif (self.userType == "provider"):
            return self.fileSystem.get_provider_by_id(self.id)
        else:
            return False

    def loginUI(self):
        while True:
            print("\nWelcome to the ChocAn Terminal System\n")
            print("Please choose an option below by entering a number between 1 and 3")
            print("1. I am a ChocAn Employee")
            print("2. I am a Provider")
            print("3. Exit")
            userInput = getInputNumberSafe(3)
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
            self.id = getInputNumberSafe(999999999)
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
                emp = Employee(self.id, self.fileSystem)
                isManager = self.fileSystem.is_manager(self.id)

                print("1. Add Member")
                print("2. Edit Member")
                print("3. Delete Member")
                if isManager:
                    print("4. Add Provider")
                    print("5. Edit Provider")
                    print("6. Delete Provider")
                    print("7. Request report")
                    print("8. Save all data to files")
                    print("9. Exit to main terminal")
                    numOptions = 9
                else:
                    print("4. Save all data to files")
                    print("5. Exit to main terminal")
                    numOptions = 5

                userInput = getInputNumberSafe(numOptions)
                match userInput:
                    case 1:  # Add member
                        emp.add_member()
                    case 2:  # Edit member
                        emp.edit_member()
                    case 3:  # Delete member
                        memberID = int(input("Please enter the member ID: "))
                        emp.delete_member(memberID)
                    case 4:  # Add provider
                        if isManager:
                            emp.add_provider()
                        else:
                            self.fileSystem.save_dirs()
                    case 5:  # Edit provider
                        if isManager:
                            emp.edit_provider()
                        else:
                            return
                    case 6:  # Delete provider
                        if isManager:
                            providerID = int(
                                input("Please enter the member ID: "))
                            emp.delete_provider(providerID)
                        else:
                            print("ERROR!!!")
                            continue
                    case 7:  # Request manager report
                        if isManager:
                            print(self.fileSystem.get_manager_report_as_string())
                        else:
                            print("ERROR!!!")
                            continue
                    case 8:  # Save changes
                        if isManager:
                            self.fileSystem.save_dirs()
                            print("saved!")
                        else:
                            print("ERROR!!!")
                            continue
                    case 9:  # Exit terminal
                        if isManager:
                            return
                        else:
                            print("ERROR!!!")
                            continue

                    case _:  # Invalid option
                        print("ERROR!!!")

            else:  # user is a provider
                # call provider terminal
                pass
