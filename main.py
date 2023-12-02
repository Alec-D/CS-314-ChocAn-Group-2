# import pandas as pd
# import numpy as np
# from member import Member
# from provider import Provider
# import os
from service import Service
from file_system import FileSystem
from login import User


def main():
    file_system = FileSystem("member_data.csv", "provider_data.csv",
                             "service_dir.csv", "employee_data.csv")

    newUser = User(file_system)
    newUser.loginUI()


if __name__ == "__main__":
    main()
