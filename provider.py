import verification_functions


class Provider:
    def __init__(self,
                 first_name: str,
                 last_name: str,
                 id: str | int,
                 street: str,
                 city: str,
                 state: str,
                 zip: str | int):
        if id == 0:
            self.first_name = ""
            self.last_name = ""
            self.id = 0
            self.street = ""
            self.city = ""
            self.state = ""
            self.zip = 0
            self.name = ""
        else:
            self.first_name = first_name
            self.last_name = last_name
            self.id = id
            self.street = street
            self.city = city
            self.state = state
            self.zip = zip
            self.name = first_name + " " + last_name

    def __str__(self):
        return (f"Name: {self.first_name} {self.last_name}\n"
                f"Provider ID: {self.id}\n"
                f"Street: {self.street}\n"
                f"City: {self.city}\n"
                f"State: {self.state}\n"
                f"Zipcode: {self.zip}")

    def __iter__(self):
        yield self.name
        yield self.id
        yield self.street
        yield self.city
        yield self.state
        yield self.zip

    @staticmethod
    def build_provider() -> 'Provider':
        tmp = Provider('', '', 0, '', '', '', 0)
        tmp.first_name = input("First name: ")
        tmp.last_name = input("Last Name: ")
        full_name = tmp.first_name + " " + tmp.last_name
        tmp.name = full_name[0:25]
        tmp.id = input("ID: ")
        tmp.street = input("Street Address: ")
        tmp.street = tmp.street[0:25]
        tmp.city = input("City: ")
        tmp.city = tmp.city[0:14]
        tmp.state = input("State: ")
        valid_state = verification_functions.check_state(tmp.state)
        while valid_state  is False:
            print("Invalid State. Enter 2 letter state abbreviation: ")
            tmp.state = input("State: ")
            valid_state = verification_functions.check_state(tmp.state)
        tmp.zip = input("Zip: ")
        while tmp.zip < 1 or tmp.zip > 99999:
            print("Invalid Zip Code")
            tmp.zip = input("Zip: ")
        print("If the information below is correct, press 1 to save the provider data.")
        print("If the information is not correct, press 2 to re-enter the provider data. ")
        save = int(input("1 or 2: "))
        match save:
            case 1:
                return tmp
            case 2:
                print("Starting data entry for new provider again")
                Provider.build_provider()

    def edit_provider(self):
        print("Current Provider Data:")
        print(self)
        current_provider = self
        changes_done = 'n'
        while changes_done == 'n':
            choice = input("Enter field to edit: First Name, Last Name, Street Address, City, State, Zip")
            match choice:
                case 'First Name':
                    current_provider.first_name = input("Enter New First Name: ")
                case 'Last Name':
                    current_provider.last_name = input("Enter New Last Name: ")
                case 'Street Address':
                    current_provider.street = input("Enter New Street Address: ")
                case 'City':
                    current_provider.city = input("Enter New City: ")
                case 'State':
                    current_provider.state = input("Enter New State: ")
                    valid_state = verification_functions.check_state(current_provider.state)
                    while valid_state  is False:
                        print("Invalid State. Enter 2 letter state abbreviation: ")
                        current_provider.state = input("State: ")
                        valid_state = verification_functions.check_state(current_provider.state)
                case 'Zip':
                    current_provider.zip = input("Enter New Zip: ")
                    while current_provider.zip < 1 or current_provider.zip > 99999:
                        print("Invalid Zip Code")
                        current_provider.zip = input("Zip: ")
            print("\n\nNew Provider Data: ")
            print(current_provider)
            changes_done = input("Are you done making changes? y or n: ")
        change_accepted = input("If this new information is correct, enter y. \nIf it is wrong, enter n: ")
        while change_accepted != 'y' and change_accepted != 'n':
            print("please enter y or n.")
            change_accepted = input("y or n: ")
        if change_accepted == 'y':
            self = current_provider
            #send to file system
        else:
            print("Restarting Provider Edits")
            self.edit_provider(self)
    
    def get_id(self):
        return self.id

    