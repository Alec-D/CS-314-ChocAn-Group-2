from file_system import FileSystem
from employee import Employee


class User:
    """ 

    Class to handle all login functionalities for employees and providers

    """
    userType = "Bot"
    temp = FileSystem("member_data.csv", "provider_data.csv",
                      "service_dir.csv", "employee_data.csv")

    def __init__(self, ID):
        self.ID = 0

    def isValid(self, ID: int):
        if (self.userType == "employee"):
            return self.temp.is_valid_employee(ID)
        elif (self.userType == "provider"):
            return self.temp.get_provider_by_id(ID)
        else:
            return False

    def loginUI(self):
        while (True):
            # Add while loop for isValid
            print("ChocAn Software\n")
            user = 0
            while (user != 1 and user != 2):
                try:
                    user = int(
                        input("Please select:\n1-Employee\n2-Provider\n->"))
                except ValueError:
                    print("Invalid input, please enter a numeric ID")
            if (user == 1):
                self.userType = "employee"
            else:
                self.userType = "provider"
            while (True):
                try:
                    self.ID = int(
                        input(f"Please enter your {self.userType} ID: "))
                    if (isinstance(self.ID, int)):
                        break
                except ValueError:
                    print("Invalid ID, please enter a numeric ID")
            if (self.isValid(self.ID) == None or not self.isValid(self.ID)):
                print("ID not registered within our system")
                break
            else:
                print("Access Granted")
                break

        # TODO: if employeee, display employee info and permissions
        # TODO: call employee terminal or provided terminal

        if (self.userType == "employee"):
            emp = Employee(self.ID)
            option = emp.displayOptions()
            if (option == 1):  # add member
                emp.add_member()
            elif (options == 2):  # edit member
                emp.edit_member()
            elif (options == 3):  # delete member
                memberID = int(input("Please enter the member ID: "))
                emp.delete_member(memberID)
            elif (options == 4):  # add provider
                emp.add_provider()
            elif (options == 5):  # edit provider
                emp.edit_provider()
            elif (options == 6):  # delete provider
                memeberID = int(input("Please enter the member ID: "))
                emp.delete_provider()

        else:  # user is a provider
            # call provider terminal
            pass

    # temp.save_dirs()
