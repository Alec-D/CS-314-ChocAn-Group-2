from member import Member
from service import Service
from provider import Provider
import pandas as pd
import os


class FileSystem:
    def __init__(self, member_file, provider_file, service_directory):
        self.member_info = member_file
        self.provider_info = provider_file
        self.service_directory = service_directory
        self.member_df = None
        self.provider_df = None
        self.service_directory_df = None
        self.all_services_df = None

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


    def load_member_df(self):
        try:
            self.member_df = pd.read_csv(self.member_info)
        except FileNotFoundError:
            self.member_df = pd.DataFrame(columns=["first_name", "last_name", "id", "street", "city", "state", "zip"])

    def save_member_df(self):
        self.member_df.sort_values(by=['last_name'], inplace=True)
        self.member_df.to_csv(self.member_info, index=False)

    def load_provider_df(self):
        try:
            self.provider_df = pd.read_csv(self.provider_info)
        except FileNotFoundError:
            self.provider_df = pd.DataFrame(columns=["first_name", "last_name", "id", "street", "city", "state", "zip"])

    def save_provider_df(self):
        self.provider_df.sort_values(by=['last_name'], inplace=True)
        self.provider_df.to_csv(self.provider_info, index=False)


    def save_all_services_df(self):
        self.all_services_df.to_csv("summary_reports/all_services.csv", index=False)

    def load_all_services_df(self):
        try:
            self.all_services_df = pd.read_csv("summary_reports/all_services.csv")
        except FileNotFoundError:
            self.all_services_df = pd.DataFrame(columns=["current_date",
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

    def load_service_df(self):
        try:
            self.service_directory_df = pd.read_csv(self.service_directory)
        except FileNotFoundError:
            self.service_directory_df = pd.DataFrame(columns=["date", "member_id", "provider_id", "service_code", "comments"])

    def save_service_df(self):
        self.service_directory_df.to_csv(self.service_directory, index=False)

    def get_provider_report_info(self, prov_id):
        try:
            tmp_df = pd.read_csv(f"provider_reports/{prov_id}.csv")
        except FileNotFoundError:
            return None

        return tmp_df

    def get_member_report_info(self, mem_id):
        try:
            tmp_df = pd.read_csv(f"member_reports/{mem_id}.csv")
        except FileNotFoundError:
            return None

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
    def get_member_by_name(self, last_name):
        if self.member_df is None:
            self.load_member_df()

        member = self.member_df[self.member_df["last_name"] == last_name]

        if member.empty:
            return None

        return Member(**member.iloc[0].to_dict())

    def get_member_by_id(self, mem_id):
        if self.member_df is None:
            self.load_member_df()

        member = self.member_df[self.member_df["id"] == mem_id]

        if member.empty:
            return None

        return Member(**member.iloc[0].to_dict())

    def add_member(self, member):
        if self.member_df is None:
            self.load_member_df()

        self.member_df.loc[len(self.member_df.index)] = list(member)

    def remove_member(self, member):
        if self.member_df is None:
            self.load_member_df()

        tmp = self.member_df[self.member_df["id"] == member.id]

        if tmp.empty:
            raise ValueError("Member not found")

        self.member_df.drop(tmp.index, inplace=True)

    def get_provider_by_name(self, last_name):
        if self.provider_df is None:
            self.load_provider_df()

        provider = self.provider_df[self.provider_df["last_name"] == last_name]

        if provider.empty:
            return None

        return Provider(**provider.iloc[0].to_dict())

    def get_provider_by_id(self, mem_id):
        if self.provider_df is None:
            self.load_provider_df()

        provider = self.provider_df[self.provider_df["id"] == mem_id]

        if provider.empty:
            return None

        return Provider(**provider.iloc[0].to_dict())

    def add_provider(self, provider):
        if self.provider_df is None:
            self.load_provider_df()

        self.provider_df.loc[len(self.provider_df.index)] = list(provider)

    def remove_provider(self, provider):
        if self.provider_df is None:
            self.load_provider_df()

        tmp = self.provider_df[self.provider_df["id"] == provider.id]

        if tmp.empty:
            raise ValueError("Provider not found")

        self.provider_df.drop(tmp.index, inplace=True)

    def get_service_name_by_code(self, code):
        if self.service_directory_df is None:
            self.load_service_df()

        service = self.service_directory_df[self.service_directory_df["service_code"] == code]

        if service.empty:
            return None

        return service.iloc[0]["service_name"]

    def get_fee_by_code(self, code):
        if self.service_directory_df is None:
            self.load_service_df()

        service = self.service_directory_df[self.service_directory_df["service_code"] == code]

        if service.empty:
            return None

        return service.iloc[0]["fee"]

    def document_service(self, service):
        if not isinstance(service, Service):
            raise TypeError("service must be of type Service")

        if not os.path.exists(f"member_reports/{service.member_id}.csv"):
            df = pd.DataFrame(columns=["date_of_service", "provider_first_name", "provider_last_name", "service_name"])
        else:
            df = pd.read_csv(f"member_reports/{service.member_id}.csv")
        
        df.loc[len(df.index)] = service.get_member_report_info()
        df.to_csv(f"member_reports/{service.member_id}.csv", index=False)

        if not os.path.exists(f"provider_reports/{service.provider_id}.csv"):
            df = pd.DataFrame(columns=["date_of_service",
                                       "current_date",
                                       "current_time",
                                       "member_first_name",
                                       "member_last_name",
                                       "member_id",
                                       "service_code",
                                       "fee"])
        else:
            df = pd.read_csv(f"provider_reports/{service.provider_id}.csv")

        df.loc[len(df.index)] = service.get_provider_report_info()
        df.to_csv(f"provider_reports/{service.provider_id}.csv", index=False)

        if self.all_services_df is None:
            self.load_all_services_df()

        self.all_services_df.loc[len(self.all_services_df.index)] = list(service)

    def get_member_report_as_string(self, mem_id):
        member = self.get_member_by_id(mem_id)
        if member is None:
            return None

        mem_str = f"{member}\n"

        df = self.get_member_report_info(mem_id)

        for row in df.iterrows():
            mem_str += f"\t{row[1]['date_of_service']}\n"
            mem_str += f"\t{row[1]['provider_first_name']} {row[1]['provider_last_name']}\n"
            mem_str += f"\t{row[1]['service_name']}\n\n"
        
        return mem_str


    def save_dirs(self):
        if self.member_df is not None:
            self.save_member_df()

        if self.provider_df is not None:
            self.save_provider_df()

        if self.service_directory_df is not None:
            self.save_service_df()

        if self.all_services_df is not None:
            self.save_all_services_df()
