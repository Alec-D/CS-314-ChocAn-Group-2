import verification_functions
global max_id
max_id = 971447942

class Member:
    def __init__(self, first_name, last_name, id, street, city, state, zip, is_suspended):
        if id == 0:
            self.first_name = ""
            self.last_name = ""
            self.id = 0
            self.street = ""
            self.city = ""
            self.state = ""
            self.zip = 0
            self.is_suspended = False
            self.name = ""
        else:
            self.first_name = first_name
            self.last_name = last_name
            self.id = id
            self.street = street
            self.city = city
            self.state = state
            self.zip = zip
            self.is_suspended = is_suspended
            self.name = first_name + " " + last_name

    def __iter__(self):
        yield self.name
        yield self.id
        yield self.street
        yield self.city
        yield self.state
        yield self.zip
        yield self.is_suspended

    def __str__(self):
        return f"Name: {self.first_name} {self.last_name}\nMember ID: {self.id}\nStreet: {self.street}\nCity: {self.city}\nState: {self.state}\nZipcode: {self.zip}"
    
    def build_member(self):
        self.first_name = input("First name: ")
        self.last_name = input("Last Name: ")
        full_name = self.first_name + " " + self.last_name
        self.name = full_name[0:25]
        global max_id
        max_id = max_id + 1
        self.id = max_id
        self.street = input("Street Address: ")
        self.street = self.street[0:25]
        self.city = input("City: ")
        self.city = self.city[0:14]
        self.state = input("State: ")
        valid_state = verification_functions.check_state(self.state)
        while valid_state  is False:
            print("Invalid State. Enter 2 letter state abbreviation: ")
            self.state = input("State: ")
            valid_state = verification_functions.check_state(self.state)
        self.zip = int(input("Zip: "))
        while self.zip < 1 or self.zip > 99999:
            print("Invalid Zip Code")
            self.zip = int(input("Zip: "))
        self.is_suspended = False
        print("If the information below is correct, press 1 to save the member data.")
        print("If the information is not correct, press 2 to re-enter the member data. ")
        save = int(input("1 or 2: "))
        match save:
            case 1:
                #send to file system
                pass
            case 2:
                print("Starting data entry for new member again")
                max_id = max_id - 1
                self.build_member()

    def edit_member(self):
        print("Current Member Data:")
        print(self)
        current_member = self

        choice = input("Enter field to edit: First Name, Last Name, Street Address, City, State, Zip, Status: ")
        match choice:
            case 'First Name':
                current_member.first_name = input("Enter New First Name: ")
            case 'Last Name':
                current_member.last_name = input("Enter New Last Name: ")
            case 'Street Address':
                current_member.street = input("Enter New Street Address: ")
            case 'City':
                current_member.city = input("Enter New City: ")
            case 'State':
                current_member.state = input("Enter New State: ")
                valid_state = verification_functions.check_state(current_member.state)
                while valid_state  is False:
                    print("Invalid State. Enter 2 letter state abbreviation: ")
                    current_member.state = input("State: ")
                    valid_state = verification_functions.check_state(current_member.state)
            case 'Zip':
                current_member.zip = input("Enter New Zip: ")
                while current_member.zip < 1 or current_member.zip > 99999:
                    print("Invalid Zip Code")
                    current_member.zip = input("Zip: ")
            case 'Status':
                if current_member.is_suspended is False:
                    print("Member Status is Suspended")
                else:
                    print("Member Status is Active") 
                change_status = input("Do you want to switch status? y/n")
                while change_status != 'y' and change_status != 'n':
                    print("Invalid Input")
                    change_status = input("Do you want to switch status? y/n")
                if change_status == 'y':
                    if current_member.is_suspended is False:
                        current_member.is_suspended = True
                    else:
                        current_member.is_suspended = False
                else:
                    print("No change in status entered")
        print("\n\nNew Member Data: ")
        print(current_member)
        change_accepted = input("If this new information is correct, enter y. \nIf it is wrong, enter n: ")
        while change_accepted != 'y' and change_status != 'n':
            print("please enter y or n.")
            change_accepted = input("y or n: ")
        if change_accepted == 'y':
            self = current_member
            #send to file system
        else:
            print("Restarting Member Edits")
            self.edit_member(self)


    def check_status(self):
        status = self.is_suspended
        return status
    
    def get_id(self):
        return self.id
    

# m1 = Member('Nathalie', 'Owen', 111111111, '1612 Grand St', 'Alameda', 'CA', 94501, False)
#m1.edit_member()
