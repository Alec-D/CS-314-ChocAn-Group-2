from member import Member
from service import Service
from provider import Provider
import pandas as pd
import os


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
            self._member_df = pd.DataFrame(columns=["first_name", "last_name", "id", "street", "city", "state", "zip"])

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
        self._all_services_df.to_csv("summary_reports/all_services.csv", index=False)

    def _load_all_services_df(self) -> None:
        try:
            self._all_services_df = pd.read_csv("summary_reports/all_services.csv")
        except FileNotFoundError:
            self._all_services_df = pd.DataFrame(columns=["current_date",
                                                          "current_time",
                                                          "date_of_service",
                                                          "provider_id",
                                                          "provider_first_name",
                                                          "provider_last_name",
                                                          "member_id",
                                                          "member_first_name",
                                                          "member_last_name",
                                                          "service_code",
                                                          "service_name",
                                                          "comments",
                                                          "fee"
                                                          ])

    def _load_service_df(self) -> None:
        try:
            self._service_directory_df = pd.read_csv(self._service_directory)
        except FileNotFoundError:
            # create a new df
            self._service_directory_df = pd.DataFrame(
                columns=["date", "member_id", "provider_id", "service_code", "comments"])

    def _save_service_df(self) -> None:
        self._service_directory_df.to_csv(self._service_directory, index=False)

    def _load_employee_df(self) -> None:
        try:
            self._employee_df = pd.read_csv(self._employee_directory)
        except FileNotFoundError:
            self._employee_df = pd.DataFrame(columns=["id", "first_name", "last_name", "is_manager"])

    def _get_provider_report_info(self, prov_id: int | str) -> pd.DataFrame | None:
        if isinstance(prov_id, str):
            if len(prov_id) != 9:
                return None

            prov_id = int(prov_id)

        if self._all_services_df is None:
            self._load_all_services_df()

        if self._member_df is None:
            self._load_member_df()

        # build df from all services that contains dos, current date, current time, member fname, mem lname member id, service code, fee
        left_df = self._all_services_df[self._all_services_df["provider_id"] == prov_id]
        left_df = left_df[["date_of_service", "current_date", "current_time", "member_first_name", "member_last_name",
                         "member_id", "service_code", "fee"]]

        right_df = self._member_df[["id", "first_name", "last_name"]]

        tmp_df = pd.merge(left_df, right_df, left_on="member_id", right_on="id")

        return tmp_df

    def _get_member_report_info(self, mem_id: int | str) -> pd.DataFrame | None:
        if isinstance(mem_id, str):
            if len(mem_id) != 9:
                return None

            mem_id = int(mem_id)

        if self._all_services_df is None:
            self._load_all_services_df()

        if self._provider_df is None:
            self._load_provider_df()

        left_df = self._all_services_df[self._all_services_df["member_id"] == mem_id]
        left_df = left_df[["date_of_service","provider_id", "service_name"]]
        right_df = self._provider_df[["id", "first_name", "last_name"]]
        tmp_df = pd.merge(left_df, right_df, left_on="provider_id", right_on="id")
        tmp_df.drop(columns=["provider_id"], inplace=True)

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
        Adds a member to the member dataframe


        :param member:
        :return:
        """
        if self._member_df is None:
            self._load_member_df()

        if not isinstance(member, Member):
            raise TypeError("member must be of type Member")

        self._member_df.loc[len(self._member_df.index)] = [n[1] for n in member.__dict__.items() if n[0] != "name"]

    def update_member(self, member: Member) -> None:
        if not isinstance(member, Member):
            raise TypeError("member must be of type Member")

        if self._member_df is None:
            self._load_member_df()

        tmp = self._member_df[self._member_df["id"] == member.id]

        if tmp.empty:
            raise ValueError("Member not found")

        self._member_df.loc[tmp.index[0]] = [n[1] for n in member.__dict__.items() if n[0] != "name"]

    def remove_member(self, member: Member) -> None:
        if self._member_df is None:
            self._load_member_df()

        tmp = self._member_df[self._member_df["id"] == member.id]

        if tmp.empty:
            raise ValueError("Member not found")

        self._member_df.drop(tmp.index, inplace=True)

    def get_provider_by_name(self, last_name: str) -> Provider | None:
        if self._provider_df is None:
            self._load_provider_df()

        provider = self._provider_df[self._provider_df["last_name"] == last_name]

        if provider.empty:
            return None

        return Provider(**provider.iloc[0].to_dict())

    def update_provider(self, provider: Provider) -> None:
        if not isinstance(provider, Provider):
            raise TypeError("provider must be of type Provider")

        if self._provider_df is None:
            self._load_provider_df()

        tmp = self._provider_df[self._provider_df["id"] == provider.id]

        if tmp.empty:
            raise ValueError("Provider not found")

        self._provider_df.loc[tmp.index[0]] = [n[1] for n in provider.__dict__.items() if n[0] != "name"]

    def get_provider_by_id(self, mem_id: int | str) -> Provider | None:
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
        if self._provider_df is None:
            self._load_provider_df()

        if not isinstance(provider, Provider):
            raise TypeError("provider must be of type Provider")

        self._provider_df.loc[len(self._provider_df.index)] = [n[1] for n in provider.__dict__.items() if n[0] != "name"]

    def remove_provider(self, provider: Provider) -> None:
        if self._provider_df is None:
            self._load_provider_df()

        if not isinstance(provider, Provider):
            raise TypeError("provider must be of type Provider")

        tmp = self._provider_df[self._provider_df["id"] == provider.id]

        if tmp.empty:
            raise ValueError("Provider not found")

        self._provider_df.drop(tmp.index, inplace=True)

    def is_valid_employee(self, emp_id: int | str) -> bool:
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

    def document_service(self, service: Service) -> None:
        if not isinstance(service, Service):
            raise TypeError("service must be of type Service")

        if self._all_services_df is None:
            self._load_all_services_df()

        self._all_services_df.loc[len(self._all_services_df.index)] = [n for n in service.__dict__.values()]

    def get_member_report_as_string(self, mem_id: int | str) -> str | None:
        member = self.get_member_by_id(mem_id)
        if member is None:
            return None

        mem_str = f"{member}\n"

        df = self._get_member_report_info(mem_id)

        for row in df.iterrows():
            mem_str += f"\tDOS: {row[1]['date_of_service']}\n"
            mem_str += f"\tProvider Name: {row[1]['provider_first_name']} {row[1]['provider_last_name']}\n"
            mem_str += f"\tService: {row[1]['service_name']}\n\n"

        return mem_str

    def get_provider_report_as_string(self, prov_id: int | str) -> str | None:
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
            prov_str += f"\tMember: {row[1]['member_first_name']} {row[1]['member_last_name']}\n"
            prov_str += f"\tMember ID: {row[1]['member_id']}\n"
            prov_str += f"\tService Code: {row[1]['service_code']}\n"
            prov_str += f"\tFee: {row[1]['fee']}\n\n"

        prov_str += f"Total Consultations: {count}\n"
        prov_str += f"Total Fees: {fee}\n"

        return prov_str

    def get_etf_report_as_string(self, prov_id: int | str) -> str | None:
        provider = self.get_provider_by_id(prov_id)

        if provider is None:
            return None

        etf_str = f"Provider: {provider.first_name} {provider.last_name}\n"
        etf_str += f"Provider ID: {provider.id}\n"

        df = self._get_provider_report_info(prov_id)

        total_earned = df.fee.sum()

        etf_str += f"Total Earned: {total_earned}\n"

        return etf_str

    def get_manager_report_as_string(self) -> str | None:
        df = self._all_services_df
        df = df.groupby(["provider_first_name", "provider_last_name"])

        man_str = "Weekly Summary Report\n\n"

        for names, prov_df in df:
            man_str += f"Provider: {names[0]} {names[1]}\n"
            man_str += f"Total Consultations: {len(prov_df.index)}\n"
            man_str += f"Total Fees: {prov_df.fee.sum()}\n\n"

        return man_str

    def save_dirs(self) -> None:
        if self._member_df is not None:
            self._save_member_df()

        if self._provider_df is not None:
            self._save_provider_df()

        if self._service_directory_df is not None:
            self._save_service_df()

        if self._all_services_df is not None:
            self._save_all_services_df()
