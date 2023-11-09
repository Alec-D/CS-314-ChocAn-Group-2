import pandas as pd 
import numpy as np
from member import Member
from provider import Provider
import os
from service import Service
from file_system import FileSystem



def main():
    file_system = FileSystem("member_data.csv", "provider_data.csv", "service_dir.csv", "employee_data.csv")
    tmp_mem = file_system.get_member_by_name("Addekin")
    tmp_prov = file_system.get_provider_by_name("Zanini")
    tmp_serv = Service("12-31-1973", tmp_prov, tmp_mem, 123456, "splinting", "I splinted his arm", 200.00)
    file_system.document_service(tmp_serv)
    print(file_system.get_member_report_as_string(tmp_mem.id))
    print(file_system.get_provider_report_as_string(tmp_prov.id))
    print(file_system.get_etf_report_as_string(tmp_prov.id))
    print(file_system.get_manager_report_as_string())

    os.remove("member_reports/399310330.csv")
    os.remove("provider_reports/263034389.csv")


if __name__ == "__main__":
    main()
