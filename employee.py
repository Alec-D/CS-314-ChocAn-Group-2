# This is the employee class
from file_system import FileSystem
from member import Member
from provider import Provider


class Employee:

    file_system = FileSystem(
        "member_data.csv", "provider_data.csv", "service_dir.csv", "employee_data.csv")

    def __init__(self, id):
        self.id = id

    def displayOptions(self) -> int:
        print("1.\tAdd Member")
        print("2.\tEdit Member")
        print("3.\tDelete Member")
        if (file_system.is_manager(self.id)):
            print("4.\tAdd provider")
            print("5.\tEdit provider")
            print("6.\tDelete provider")

        user = int(input("->"))
        return user

    def add_member(self):
        first_name = input("First name: ")
        last_name = input("Last name: ")
        member = self.file_system.get_member_by_name(last_name)
        if member is None:
            member = Member.build_member()
        else:
            print("Member has exists")

    def edit_member(self):
        last_name = input("Last name: ")
        member = self.file_system.get_member_by_name(last_name)
        if member is None:
            print("No member is found")
        else:
            member.edit_member()

    def delete_member(self, member_id):
        member = self.file_system.get_member_by_id(member_id)
        if member is None:
            print("No such member")
        else:
            self.file_system.remove_member(member)

    def add_provider(self):
        first_name = input("First name: ")
        last_name = input("Last name: ")
        provider = self.file_system.get_provider_by_name(last_name)
        if provider is None:
            provider = Provider.build_provider()
        else:
            print("Provider has exists")

    def edit_provider(self):
        last_name = input("Last name: ")
        provider = self.file_system.get_provider_by_name(last_name)
        if provider is None:
            print("No provider is found")
        else:
            provider.edit_provider()

    def delete_provider(self, provider_id):
        provider = self.file_system.get_provider_by_id(provider_id)
        if provider is None:
            print("No such provider")
        else:
            self.file_system.remove_provider(provider)
