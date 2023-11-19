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

    print("Member Report")
    print(file_system._get_member_report_info(tmp_mem.id))
    print(len(file_system._get_member_report_info(tmp_mem.id)))
    print("Provider Report")
    print(file_system._get_provider_report_info(tmp_prov.id))



if __name__ == "__main__":
    main()
