# This is the employee class
from file_system import FileSystem
from member import Member
from provider import Provider


class Employee:

    def __init__(self, id, fileSystem: FileSystem):
        self.id = id
        self.fileSystem = fileSystem

    def add_member(self):
        last_name = input("Let's check if the member exists already. Enter their last name: ")
        member = self.fileSystem.get_member_by_name(last_name)
        if member is None:
            print("Member does not already exist. Add Member: ")
            member = Member.build_member()
            self.fileSystem.add_member(member)
        else:
            print("Member already exists")

    def edit_member(self):
        last_name = input("Enter their last name: ")
        member = self.fileSystem.get_member_by_name(last_name)
        if member is None:
            print("Member does not exist")
        else:
            member.edit_member()
            self.fileSystem.update_member(member)

    def delete_member(self, member_id):
        member = self.fileSystem.get_member_by_id(member_id)
        if member is None:
            print("Member does not exist")
        else:
            self.fileSystem.remove_member(member)

    def add_provider(self):
        last_name = input("Let's check if the provider exists already. Enter their last name: ")
        provider = self.fileSystem.get_provider_by_name(last_name)
        if provider is None:
            print("Provider does not already exist. Add Provider: ")
            provider = Provider.build_provider()
            self.fileSystem.add_provider(provider)
        else:
            print("Provider already exists")

    def edit_provider(self):
        last_name = input("Last name: ")
        provider = self.fileSystem.get_provider_by_name(last_name)
        if provider is None:
            print("Provider does not exist")
        else:
            provider.edit_provider()
            self.fileSystem.update_provider(provider)

    def delete_provider(self, provider_id):
        provider = self.fileSystem.get_provider_by_id(provider_id)
        if provider is None:
            print("Provider does not exist")
        else:
            self.fileSystem.remove_provider(provider)
