from member import Member
from service import Service
from provider import Provider
import pandas as pd
import os
import datetime


class FileSystem:
    """
    Class to handle all file system operations

    Will lazily initialize all dataframes when needed by the program. To ensure that all data is saved, call save_dirs()
    before exiting the program.

    Example Usage:

    >>> file_system = FileSystem("member_data.csv", "provider_data.csv", "service_dir.csv", "employee_data.csv")
    >>> file_system.add_member(Member("Steve", "Test", 123456789, "1234 Test St", "Test City", "CA", 12345, False))
    >>> file_system.save_dirs()

    :ivar _member_info: path to member data csv
    :ivar _provider_info: path to provider data csv
    :ivar _service_directory: path to service directory csv
    :ivar _employee_directory: path to employee directory csv
    :ivar _member_df: dataframe containing member data
    :ivar _provider_df: dataframe containing provider data
    :ivar _employee_df: dataframe containing employee data
    :ivar _service_directory_df: dataframe containing service directory data
    :ivar _all_services_df: dataframe containing all service data
    """

    def __init__(self, member_file, provider_file, service_directory, employee_directory):
        self._member_info = member_file
        self._provider_info = provider_file
        self._service_directory = service_directory
        self._employee_directory = employee_directory
        self._member_df = None
        self._provider_df = None
        self._employee_df = None
        self._service_directory_df = None
        self._all_services_df = None

        if not os.path.isdir("member_reports"):
            os.mkdir("member_reports")

        if not os.path.isdir("provider_reports"):
            os.mkdir("provider_reports")

        if not os.path.isdir("summary_reports"):
            os.mkdir("summary_reports")

    #     _______             __                       __
    #    |       \           |  \                     |  \
    #    | $$$$$$$\  ______   \$$ __     __  ______  _| $$_     ______
    #    | $$__/ $$ /      \ |  \|  \   /  \|      \|   $$ \   /      \
    #    | $$    $$|  $$$$$$\| $$ \$$\ /  $$ \$$$$$$\\$$$$$$  |  $$$$$$\
    #    | $$$$$$$ | $$   \$$| $$  \$$\  $$ /      $$ | $$ __ | $$    $$
    #    | $$      | $$      | $$   \$$ $$ |  $$$$$$$ | $$|  \| $$$$$$$$
    #    | $$      | $$      | $$    \$$$   \$$    $$  \$$  $$ \$$     \
    #     \$$       \$$       \$$     \$     \$$$$$$$   \$$$$   \$$$$$$$

    def _load_member_df(self) -> None:
        try:
            self._member_df = pd.read_csv(self._member_info)
        except FileNotFoundError:
            self._member_df = pd.DataFrame(
                columns=["first_name", "last_name", "id", "street", "city", "state", "zip"])

    def _save_member_df(self) -> None:
        self._member_df.sort_values(by=['last_name'], inplace=True)
        self._member_df.to_csv(self._member_info, index=False)

    def _load_provider_df(self) -> None:
        try:
            self._provider_df = pd.read_csv(self._provider_info)
        except FileNotFoundError:
            # create a new df
            self._provider_df = pd.DataFrame(
                columns=["first_name", "last_name", "id", "street", "city", "state", "zip"])

    def _save_provider_df(self) -> None:
        self._provider_df.sort_values(by=['last_name'], inplace=True)
        self._provider_df.to_csv(self._provider_info, index=False)

    def _save_all_services_df(self) -> None:
        self._all_services_df.to_csv(
            "summary_reports/all_services.csv", index=False)

    def _load_all_services_df(self) -> None:
        try:
            self._all_services_df = pd.read_csv(
                "summary_reports/all_services.csv")
        except FileNotFoundError:
            self._all_services_df = pd.DataFrame(columns=["current_date",
                                                          "current_time",
                                                          "date_of_service",
                                                          "provider_id",
                                                          "member_id",
                                                          "service_code",
                                                          "service_name",
                                                          "comments",
                                                          "fee"
                                                          ])

    def _load_service_df(self) -> None:
        try:
            self._service_directory_df = pd.read_csv(self._service_directory)
        except FileNotFoundError:
            self._service_directory_df = pd.DataFrame(
                columns=["service_code", "service_name", "fee"])

    def _save_service_df(self) -> None:
        self._service_directory_df.to_csv(self._service_directory, index=False)

    def _load_employee_df(self) -> None:
        try:
            self._employee_df = pd.read_csv(self._employee_directory)
        except FileNotFoundError:
            self._employee_df = pd.DataFrame(
                columns=["id", "first_name", "last_name", "is_manager"])

    def _get_provider_report_info(self, prov_id: int | str, start_date: str = None, end_date: str = None) -> pd.DataFrame | None:
        """
        Returns a dataframe containing the information needed to generate a provider report. Currently this defaults to
        the last 7 days, but can be changed by passing in start_date and end_date. This isn't currently supported by
        the system, but it would be easy to add for future use.

        :param prov_id: the provider id as a string or int
        :param start_date: start date as a string in the format mm-dd-yyyy
        :param end_date: end date as a string in the format mm-dd-yyyy
        :return: dataframe containing the information needed to generate a provider report or None if the provider is
        not found
        """
        if isinstance(prov_id, str):
            if len(prov_id) != 9:
                return None

            prov_id = int(prov_id)

        if self._all_services_df is None:
            self._load_all_services_df()

        if self._member_df is None:
            self._load_member_df()

        if self._all_services_df is None:
            self._load_all_services_df()

        if self._provider_df is None:
            self._load_provider_df()

        if start_date is None and end_date is None:
            start_date = pd.Timestamp.today() - pd.Timedelta(days=7)
            end_date = pd.Timestamp.today()

        if isinstance(start_date, str):
            start_date = datetime.datetime.strptime(start_date, "%m-%d-%Y")

        if isinstance(end_date, str):
            end_date = datetime.datetime.strptime(end_date, "%m-%d-%Y")

        if end_date - start_date < datetime.timedelta(days=0):
            return None

        left_df = self._all_services_df[self._all_services_df["provider_id"] == prov_id]
        left_df = left_df[["date_of_service", "current_date",
                           "current_time", "member_id", "service_code", "fee"]]

        right_df = self._member_df[["id", "first_name", "last_name"]]

        tmp_df = pd.merge(left_df, right_df,
                          left_on="member_id", right_on="id")

        tmp_df = tmp_df[(pd.to_datetime(tmp_df.date_of_service, format='%m-%d-%Y') >= start_date)
                        & (pd.to_datetime(tmp_df.date_of_service, format='%m-%d-%Y') <= end_date)]

        return tmp_df

    def _get_member_report_info(self, mem_id: int | str, start_date: str = None, end_date: str = None) -> pd.DataFrame | None:
        """
        Returns a dataframe containing the information needed to generate a member report. Currently this defaults to
        the last 7 days, but can be changed by passing in start_date and end_date. This isn't currently supported by
        the system, but it would be easy to add for future use.

        The logic behind this function is rather confusing as I had a rather hard time working with pandas' dates. I
        was forced to use some awkward syntax to get the dates to properly compare. I'm sure there is a better way to
        do this, but I couldn't figure it out.

        :param mem_id: the member id as a string or int
        :param start_date: start date as a string in the format mm-dd-yyyy
        :param end_date: end date as a string in the format mm-dd-yyyy
        :return: Returns a dataframe containing the information needed to generate a member report or None if the
        member is not found
        """
        if isinstance(mem_id, str):
            if len(mem_id) != 9:
                return None

            mem_id = int(mem_id)

        if self._all_services_df is None:
            self._load_all_services_df()

        if self._provider_df is None:
            self._load_provider_df()

        if start_date is None and end_date is None:
            start_date = pd.Timestamp.today() - pd.Timedelta(days=7)
            end_date = pd.Timestamp.today()

        if isinstance(start_date, str):
            start_date = datetime.datetime.strptime(start_date, "%m-%d-%Y")

        if isinstance(end_date, str):
            end_date = datetime.datetime.strptime(end_date, "%m-%d-%Y")

        if end_date - start_date < datetime.timedelta(days=0):
            return None

        left_df = self._all_services_df[self._all_services_df["member_id"] == mem_id]
        left_df = left_df[["date_of_service", "provider_id", "service_name"]]
        right_df = self._provider_df[["id", "first_name", "last_name"]]
        tmp_df = pd.merge(left_df, right_df,
                          left_on="provider_id", right_on="id")
        tmp_df.drop(columns=["provider_id"], inplace=True)
        tmp_df = tmp_df[(pd.to_datetime(tmp_df.date_of_service, format='%m-%d-%Y') >= start_date)
                        & (pd.to_datetime(tmp_df.date_of_service, format='%m-%d-%Y') <= end_date)]

        return tmp_df

    #     _______             __        __  __
    #    |       \           |  \      |  \|  \
    #    | $$$$$$$\ __    __ | $$____  | $$ \$$  _______
    #    | $$__/ $$|  \  |  \| $$    \ | $$|  \ /       \
    #    | $$    $$| $$  | $$| $$$$$$$\| $$| $$|  $$$$$$$
    #    | $$$$$$$ | $$  | $$| $$  | $$| $$| $$| $$
    #    | $$      | $$__/ $$| $$__/ $$| $$| $$| $$_____
    #    | $$       \$$    $$| $$    $$| $$| $$ \$$     \
    #     \$$        \$$$$$$  \$$$$$$$  \$$ \$$  \$$$$$$$

    def get_member_by_name(self, last_name: str) -> Member | None:
        """
        Returns a Member object if found, otherwise returns None

        If multiple members have the same last name, the first one found will be returned. So if you need to ensure
        that the correct member is returned, use get_member_by_id instead.
        :param last_name: the string used to search the dataframe
        :return: Member on success, None on failure
        """
        if self._member_df is None:
            self._load_member_df()

        member = self._member_df[self._member_df["last_name"] == last_name]

        if member.empty:
            return None

        return Member(**member.iloc[0].to_dict())

    def get_member_by_id(self, mem_id: int | str) -> Member | None:
        """
        Returns a Member object if found, otherwise returns None

        This method is preferred over get_member_by_name because it is guaranteed to return the correct member.
        :param mem_id: an integer or a string of length 9
        :return: Member on success, None on failure
        """
        if self._member_df is None:
            self._load_member_df()

        if isinstance(mem_id, str):
            if len(mem_id) != 9:
                return None

            mem_id = int(mem_id)

        member = self._member_df[self._member_df.id == mem_id]

        if member.empty:
            return None

        return Member(**member.iloc[0].to_dict())

    def add_member(self, member: Member) -> None:
        """
        Adds a member to the member dataframe. Will automatically assign an id if one is not provided.
        This does not check for duplicate members, so it is up to the user to ensure that the member is not already
        in the system otherwise the id will be incremented and the member will be added again.


        :param member: the member to add as a Member object
        :raises TypeError: if member is not of type Member
        :return: None on success
        """
        if self._member_df is None:
            self._load_member_df()

        if not isinstance(member, Member):
            raise TypeError("member must be of type Member")

        if member.id == 0:
            member.id = self.get_maximum_member_id() + 1

        self._member_df.loc[len(self._member_df.index)] = [n[1]
                                                           for n in member.__dict__.items() if n[0] != "name"]

    def update_member(self, member: Member) -> None:
        """
        If the user has a member object that they received from get_member_by_id or get_member_by_name, they can
        change the member object and then call this function to update the member in the dataframe.

        :param member: a member object that has been updated
        :raise TypeError: if member is not of type Member
        :raise ValueError: if the member is not found (should not call this function if the member is not found)
        :return: None on success
        """
        if not isinstance(member, Member):
            raise TypeError("member must be of type Member")

        if self._member_df is None:
            self._load_member_df()

        tmp = self._member_df[self._member_df["id"] == member.id]

        if tmp.empty:
            raise ValueError("Member not found")

        self._member_df.loc[tmp.index[0]] = [n[1]
                                             for n in member.__dict__.items() if n[0] != "name"]

    def remove_member(self, member: Member) -> None:
        """
        Removes a member from the member dataframe. It is up to the user to ensure that the member is in the system
        before calling this function.

        :param member: the member to remove as a Member object
        :raise TypeError: if member is not of type Member
        :return:
        """
        if self._member_df is None:
            self._load_member_df()

        tmp = self._member_df[self._member_df["id"] == member.id]

        if tmp.empty:
            raise ValueError("Member not found")

        self._member_df.drop(tmp.index, inplace=True)

    def get_provider_by_name(self, last_name: str) -> Provider | None:
        """
        Returns a Provider object if found, otherwise returns None. Does not check for duplicate providers, so it is
        up to the user to ensure that the provider they are getting is the correct one. So be sure to check whether

        the provider has a unique last name.
        :param last_name: the provider's last name
        :return: None on failure, Provider on success
        """
        if self._provider_df is None:
            self._load_provider_df()

        provider = self._provider_df[self._provider_df["last_name"] == last_name]

        if provider.empty:
            return None

        return Provider(**provider.iloc[0].to_dict())

    def update_provider(self, provider: Provider) -> None:
        """
        If the user has a provider object that they received from get_provider_by_id or get_provider_by_name, they can
        change the provider object and then call this function to update the provider in the dataframe.

        :param provider: a provider object that has been updated
        :raise TypeError: if provider is not of type Provider
        :raise ValueError: if the provider is not found (should not call this function if the provider is not found)
        :return: None on success
        """
        if not isinstance(provider, Provider):
            raise TypeError("provider must be of type Provider")

        if self._provider_df is None:
            self._load_provider_df()

        tmp = self._provider_df[self._provider_df["id"] == provider.id]

        if tmp.empty:
            raise ValueError("Provider not found")

        self._provider_df.loc[tmp.index[0]] = [n[1]
                                               for n in provider.__dict__.items() if n[0] != "name"]

    def get_provider_by_id(self, mem_id: int | str) -> Provider | None:
        """
        Returns a Provider object if found, otherwise returns None. This method is preferred over get_provider_by_name
        because it is guaranteed to return the correct provider.

        :param mem_id: the provider id as a string or int
        :return: None on failure, Provider on success
        """
        if isinstance(mem_id, str):
            if len(mem_id) != 9:
                return None

            mem_id = int(mem_id)

        if self._provider_df is None:
            self._load_provider_df()

        provider = self._provider_df[self._provider_df["id"] == mem_id]

        if provider.empty:
            return None

        return Provider(**provider.iloc[0].to_dict())

    def add_provider(self, provider: Provider) -> None:
        """
        Adds a provider to the provider dataframe. Will automatically assign an id if one is not provided.
        This does not check for duplicate providers, so it is up to the user to ensure that the provider is not already
        in the system otherwise the id will be incremented and the provider will be added again.

        :param provider: the provider to add as a Provider object
        :raise TypeError: if provider is not of type Provider
        :return: None on success
        """
        if self._provider_df is None:
            self._load_provider_df()

        if not isinstance(provider, Provider):
            raise TypeError("provider must be of type Provider")

        if provider.id == 0:
            provider.id = self.get_maximum_provider_id() + 1

        self._provider_df.loc[len(self._provider_df.index)] = [
            n[1] for n in provider.__dict__.items() if n[0] != "name"]

    def remove_provider(self, provider: Provider) -> None:
        """
        Removes a provider from the provider dataframe. It is up to the user to ensure that the provider is in the
        system before calling this function.

        :param provider: the provider to remove as a Provider object
        :raise TypeError: if provider is not of type Provider
        :raise ValueError: if the provider is not found (should not call this function if the provider is not found)
        :return: None on success
        """
        if self._provider_df is None:
            self._load_provider_df()

        if not isinstance(provider, Provider):
            raise TypeError("provider must be of type Provider")

        tmp = self._provider_df[self._provider_df["id"] == provider.id]

        if tmp.empty:
            raise ValueError("Provider not found")

        self._provider_df.drop(tmp.index, inplace=True)

    def is_valid_employee(self, emp_id: int | str) -> bool:
        """
        Checks if the employee is in the system. This is used to validate the employee id when logging in.

        :param emp_id: the employee id as a string or int
        :return: True if the employee is in the system, False otherwise
        """
        if self._employee_df is None:
            self._load_employee_df()

        if isinstance(emp_id, str):
            if len(emp_id) != 9:
                return False

            emp_id = int(emp_id)

        employee = self._employee_df[self._employee_df["id"] == emp_id]

        if employee.empty:
            return False

        return True

    def is_manager(self, emp_id: int | str) -> bool:
        """
        Checks if the employee is a manager. This is used to determine if the user has access to the manager menu.

        :param emp_id: the employee id as a string or int
        :return: True if the employee is a manager, False otherwise
        """
        if self._employee_df is None:
            self._load_employee_df()

        if isinstance(emp_id, str):
            if len(emp_id) != 9:
                return False

            emp_id = int(emp_id)

        employee = self._employee_df[self._employee_df["id"] == emp_id]

        if employee.empty:
            return False

        return employee.iloc[0]["is_manager"]

    def get_service_name_by_code(self, code: int | str) -> str | None:
        """
        Returns the service name associated with the service code. If the service code is not found, None is returned.

        :param code: the service code as a string or int
        :return: the service name as a string or None if the service code is not found
        """
        if self._service_directory_df is None:
            self._load_service_df()

        if isinstance(code, str):
            if len(code) != 6:
                return None

            code = int(code)

        service = self._service_directory_df[self._service_directory_df["service_code"] == code]

        if service.empty:
            return None

        return service.iloc[0]["service_name"]

    def get_fee_by_code(self, code: int | str) -> float | None:
        """
        Returns the fee associated with the service code. If the service code is not found, None is returned.

        :param code: the service code as a string or int
        :return: a float representing the fee or None if the service code is not found
        """
        if self._service_directory_df is None:
            self._load_service_df()

        if isinstance(code, str):
            if len(code) != 6:
                return None

            code = int(code)

        service = self._service_directory_df[self._service_directory_df["service_code"] == code]

        if service.empty:
            return None

        return service.iloc[0]["fee"]

    def document_service(self, service: Service, save_to_file: bool = True) -> None:
        """
        Adds a service to the all services dataframe. This is used to generate the various reports of the chocAn
        system. This does not check for duplicate services, so it is up to the user to ensure that the service is not
        already in the system otherwise the service will be added again. These services are not sorted, so the user
        should not rely on the order of the services in the dataframe.

        :param service: Service object to add
        :raise TypeError: if service is not of type Service
        :return: None on success
        """
        if not isinstance(service, Service):
            raise TypeError("service must be of type Service")

        if self._all_services_df is None:
            self._load_all_services_df()

        self._all_services_df.loc[len(
            self._all_services_df.index)] = list(service)

        if save_to_file:
            self._save_all_services_df()

    def get_member_report_as_string(self, mem_id: int | str, save_to_file: bool = True) -> str | None:
        """
        Returns a string containing an individual member's report formatted as required by the project description.
        It currently defaults to saving the report to a file, but this can be changed by passing in save_to_file=False.
        It also filters the report to only include the last 7 days, but this could be changed modifying the function
        in the future.


        :param mem_id: the member id as a string or int
        :param save_to_file: whether or not to save the report to a file
        :return: a string containing the member report or None if the member is not found
        """
        member = self.get_member_by_id(mem_id)
        if member is None:
            return None

        mem_str = f"{member}\n"

        df = self._get_member_report_info(mem_id)

        for row in df.iterrows():
            mem_str += f"\tDOS: {row[1]['date_of_service']}\n"
            mem_str += f"\tProvider Name: {row[1]['first_name']} {row[1]['last_name']}\n"
            mem_str += f"\tService: {row[1]['service_name']}\n\n"

        if save_to_file:
            with open(f"member_reports/{member.get_id()}_report.txt", "w") as file:
                print(f"{mem_str}", file=file)

        return mem_str

    def get_provider_report_as_string(self, prov_id: int | str, save_to_file: bool = True) -> str | None:
        """
        Returns a string containing an individual provider's report formatted as required by the project description.
        It currently defaults to saving the report to a file, but this can be changed by passing in save_to_file=False.
        It also filters the report to only include the last 7 days, but this could be changed modifying the function
        in the future.

        :param prov_id: the provider id as a string or int
        :param save_to_file: whether or not to save the report to a file
        :return: string containing the provider report or None if the provider is not found
        """
        provider = self.get_provider_by_id(prov_id)

        if provider is None:
            return None

        prov_str = f"{provider}\n"

        df = self._get_provider_report_info(prov_id)
        count = 0
        fee = 0
        for row in df.iterrows():
            count += 1
            fee += row[1]['fee']
            prov_str += f"\tDOS: {row[1]['date_of_service']}\n"
            prov_str += f"\tDate Processed: {row[1]['current_date']}\n"
            prov_str += f"\tTime Processed: {row[1]['current_time']}\n"
            prov_str += f"\tMember: {row[1]['first_name']} {row[1]['last_name']}\n"
            prov_str += f"\tMember ID: {row[1]['member_id']}\n"
            prov_str += f"\tService Code: {row[1]['service_code']}\n"
            prov_str += f"\tFee: {row[1]['fee']}\n\n"

        prov_str += f"Total Consultations: {count}\n"
        prov_str += f"Total Fees: {fee}\n"

        if save_to_file:
            with open(f"provider_reports/{provider.get_id()}_report.txt", "w") as file:
                print(f"{prov_str}", file=file)

        return prov_str

    def get_etf_report_as_string(self, prov_id: int | str, save_to_file: bool = True) -> str | None:
        """
        Returns a string containing an individual provider's etf statement formatted as required by the project
        description. It currently defaults to saving the report to a file, but this can be changed by passing in
        save_to_file=False. It also filters the report to only include the last 7 days, but this could be changed
        modifying the function in the future.

        :param prov_id: the provider id as a string or int
        :param save_to_file: Whether or not to save the report to a file
        :return: string containing the etf report or None if the provider is not found
        """
        provider = self.get_provider_by_id(prov_id)

        if provider is None:
            return None

        etf_str = f"Provider: {provider.first_name} {provider.last_name}\n"
        etf_str += f"Provider ID: {provider.id}\n"

        df = self._get_provider_report_info(prov_id)

        total_earned = df.fee.sum()

        etf_str += f"Total Earned: {total_earned}\n"

        if save_to_file:
            with open(f"provider_reports/{provider.get_id()}_etf_report.txt", "w") as file:
                print(f"{etf_str}", file=file)

        return etf_str

    def get_manager_report_as_string(self, save_to_file: bool = True) -> str | None:
        """
        Summarizes the weeks activity for all providers. It currently defaults to saving the report to a file, but
        this can be changed by passing in save_to_file=False. It also filters the report to only include the last 7
        days, but this could be changed modifying the function in the future.


        :param save_to_file: Whether or not to save the report to a file
        :return: string containing the manager report
        """
        if self._all_services_df is None:
            self._load_all_services_df()

        if self._provider_df is None:
            self._load_provider_df()

        df = self._all_services_df
        start_date = pd.Timestamp.today() - pd.Timedelta(days=7)
        end_date = pd.Timestamp.today()
        df = df[(pd.to_datetime(df.date_of_service, format='%m-%d-%Y') >= start_date)
                & (pd.to_datetime(df.date_of_service, format='%m-%d-%Y') <= end_date)]
        grouped_df = df.groupby(["provider_id"])

        man_str = "Weekly Summary Report\n\n"
        prov_count = 0
        fee_sum = 0

        for ids, prov_df in grouped_df:
            if len(prov_df.index) > 0:
                prov_count += 1
            tmp_df = self._provider_df[self._provider_df["id"] == ids]
            names = tmp_df.iloc[0][["first_name", "last_name"]].to_list()
            man_str += f"\tProvider: {names[0]} {names[1]}\n"
            man_str += f"\tTotal Consultations: {len(prov_df.index)}\n"
            man_str += f"\tTotal Fees: {prov_df.fee.sum()}\n\n"

        if prov_count == 0:
            fee_sum = 0
        else:
            fee_sum = df.fee.sum()
        man_str += f"Total Providers: {prov_count}\n"
        man_str += f"Total Consultations: {len(df)}\n"
        man_str += f"Total Fees: {fee_sum}\n"

        if save_to_file:
            with open(f"summary_reports/manager_summary_report.txt", "w") as file:
                print(f"{man_str}", file=file)

        return man_str

    def get_maximum_member_id(self) -> int:
        """
        Modeled after the idea of an auto incrementing primary key in a database. This is used to assign ids to members
        when they are added to the system.

        :return: the maximum member id in the member dataframe (so add 1 to this to get the next id)
        """
        if self._member_df is None:
            self._load_member_df()

        if self._member_df.empty:
            return 0

        return self._member_df["id"].max()

    def get_maximum_provider_id(self) -> int:
        """
        Modeled after the idea of an auto incrementing primary key in a database. This is used to assign ids to providers
        when they are added to the system.

        :return: the maximum provider id in the provider dataframe (so add 1 to this to get the next id)
        """
        if self._provider_df is None:
            self._load_provider_df()

        if self._provider_df.empty:
            return 0

        return self._provider_df["id"].max()

    def get_service_directory_as_string(self, save_to_file: bool = True) -> str | None:
        """
        Returns a string containing the service directory formatted as required by the project description.

        :return: string containing the service directory
        """
        if self._service_directory_df is None:
            self._load_service_df()

        service_str = "Service Directory\n\n"
        for index, row in self._service_directory_df.iterrows():
            service_str += f"Service Code: {row['service_code']}\n"
            service_str += f"Service Name: {row['service_name']}\n"
            service_str += f"Fee: {row['fee']}\n\n"

        if save_to_file:
            self._save_service_df()

        return service_str

    def save_dirs(self) -> None:
        """
        Very important to note that none of the dataframes are saved until this function is called. This is to ensure
        that frequent writes to the file system are not made. This function should be called before exiting the program.

        :return:  None
        """
        if self._member_df is not None:
            self._save_member_df()

        if self._provider_df is not None:
            self._save_provider_df()

        if self._service_directory_df is not None:
            self._save_service_df()

        if self._all_services_df is not None:
            self._save_all_services_df()


    def print_all_members(self) -> None:
        if self._member_df is None:
            self._load_member_df()
        print("\nAll members:\n")
        print(self._member_df.to_string() + '\n')

    def print_all_providers(self) -> None:
        if self._provider_df is None:
            self._load_provider_df()
        print("\nAll providers:\n")
        print(self._provider_df.to_string() + '\n')

    def print_all_employees(self) -> None:
        if self._employee_df is None:
            self._load_employee_df()
        print("\nAll employees:\n")
        print(self._employee_df.to_string() + '\n')

    def print_all_services(self) -> None:
        if self._all_services_df is None:
            self._load_all_services_df()
        print("\nAll services:\n")
        print(self._all_services_df.to_string() + '\n')

    def print_service_directory(self) -> None:
        if self._service_directory_df is None:
            self._load_service_df()
        print("\nService Directory:\n")
        print(self._service_directory_df.to_string() + '\n')
