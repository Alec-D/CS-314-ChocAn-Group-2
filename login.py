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

                if not isManager:
                    numOptions = 6
                    print("1. View all members (can be large!)")
                    print("2. Add member")
                    print("3. Edit member")
                    print("4. Delete member")
                    print("5. Save all data to files")
                    print("6. Exit to main terminal")
                    userInput = getInputNumberSafe(numOptions)
                    match userInput:
                        case 1:  # View all members
                            self.fileSystem.print_all_members()
                        case 2:  # Add member
                            emp.add_member()
                        case 3:  # Edit member
                            emp.edit_member()
                        case 4:  # Delete member
                            memberID = int(input("Please enter the member ID: "))
                            emp.delete_member(memberID)
                        case 5:  # Save changes
                            self.fileSystem.save_dirs()
                            print("All files saved!\n")
                        case 6:  # Exit terminal
                            return
                        case _:  # Invalid option
                            print("ERROR!!!")

                elif isManager:
                    numOptions = 11
                    print("1. View all members (can be large!)")
                    print("2. Add member")
                    print("3. Edit member")
                    print("4. Delete member")
                    print("5. View all providers (can be large!)")
                    print("6. Add provider")
                    print("7. Edit provider")
                    print("8. Delete provider")
                    print("9. Request report")
                    print("10. Save all data to files")
                    print("11. Exit to main terminal")
                    userInput = getInputNumberSafe(numOptions)
                    match userInput:
                        case 1:  # View all members
                            self.fileSystem.print_all_members()
                        case 2:  # Add member
                            emp.add_member()
                        case 3:  # Edit member
                            emp.edit_member()
                        case 4:  # Delete member
                            memberID = int(input("Please enter the member ID: "))
                            emp.delete_member(memberID)
                        case 5:  # View all providers
                            self.fileSystem.print_all_providers()
                        case 6:  # Add provider
                            emp.add_provider()
                        case 7:  # Edit provider
                            emp.edit_provider()
                        case 8:  # Delete provider
                            providerID = int(
                                input("Please enter the member ID: "))
                            emp.delete_provider(providerID)
                        case 9:  # Request manager report
                            print(self.fileSystem.get_manager_report_as_string())
                        case 10:  # Save changes
                            self.fileSystem.save_dirs()
                            print("All files saved!\n")
                        case 11:  # Exit terminal
                            return
                        case _:  # Invalid option
                            print("ERROR!!!")
                else:
                    print("ERROR!!!")
                    return

            else:  # user is a provider
                # call provider terminal
                pass
