import pandas as pd 
import os
from member import Member
from provider import Provider
from service import Service
from file_system import FileSystem



def main():
    file_system = FileSystem("member_data.csv", "provider_data.csv", "service_dir.csv")
    tmp_mem = file_system.get_member_by_name("Addekin")
    tmp_prov = file_system.get_provider_by_name("Zanini")
    tmp_serv = Service("12-31-1973", tmp_prov, tmp_mem, 123456, "splinting", "I splinted his arm", 200.00)
    file_system.document_service(tmp_serv)
    print(file_system.get_member_report_as_string(tmp_mem.id))

    os.remove("member_reports/399310330.csv")
    os.remove("provider_reports/263034389.csv")

if __name__ == "__main__":
    main()
