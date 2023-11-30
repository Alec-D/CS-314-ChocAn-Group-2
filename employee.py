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
        if (self.file_system.is_manager(self.id)):
            print("4.\tAdd Provider")
            print("5.\tEdit Provider")
            print("6.\tDelete Provider")
        print("7.\tExit to main terminal")

        user = int(input("->"))
        return user

    def add_member(self):
        last_name = input("Last name: ")
        member = self.file_system.get_member_by_name(last_name)
        if member is None:
            member = Member.build_member()
            self.file_system.add_member(member)
        else:
            print("Member already exists")

    def edit_member(self):
        last_name = input("Last name: ")
        member = self.file_system.get_member_by_name(last_name)
        if member is None:
            print("Member does not exist")
        else:
            member.edit_member()
            self.file_system.update_member(member)

    def delete_member(self, member_id):
        member = self.file_system.get_member_by_id(member_id)
        if member is None:
            print("Member does not exist")
        else:
            self.file_system.remove_member(member)

    def add_provider(self):
        last_name = input("Last name: ")
        provider = self.file_system.get_provider_by_name(last_name)
        if provider is None:
            provider = Provider.build_provider()
            self.file_system.add_provider(provider)
        else:
            print("Provider already exists")

    def edit_provider(self):
        last_name = input("Last name: ")
        provider = self.file_system.get_provider_by_name(last_name)
        if provider is None:
            print("Provider does not exist")
        else:
            provider.edit_provider()
            self.file_system.update_provider(provider)

    def delete_provider(self, provider_id):
        provider = self.file_system.get_provider_by_id(provider_id)
        if provider is None:
            print("Provider does not exist")
        else:
            self.file_system.remove_provider(provider)
