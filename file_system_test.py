import pytest
import pandas as pd
import os
from file_system import FileSystem
import datetime
from member import Member
from provider import Provider
from service import Service



@pytest.fixture
def file_system():
    return FileSystem("member_data.csv", "provider_data.csv", "service_dir.csv", "employee_data.csv")


@pytest.fixture
def extra_member(file_system):
    return Member("Steve", "Patient2", 666666666, "1234 Test St", "Test City", "FA", 12345, False)

@pytest.fixture
def service_from_more_than_7_days_ago(file_system, extra_member, new_provider):
    return Service((datetime.date.today() - datetime.timedelta(days=8)).strftime("%m-%d-%Y"), new_provider, extra_member, 123456, "splinting", "I splinted his arm", 200.00)
@pytest.fixture
def empty_file_system():
    return FileSystem("empty_member_data.csv", "empty_provider_data.csv", "empty_service_dir.csv", "empty_employee_data.csv")


@pytest.fixture
def new_member():
    return Member("Steve", "Patient", 123456780, "1234 Test St", "Test City", "FA", 12345, False)


@pytest.fixture
def new_provider():
    return Provider("Steve", "Provider", 123456789, "1234 Test St", "Test City", "FA", 12345)


@pytest.fixture
def yesterday():
    return (datetime.date.today() - datetime.timedelta(days=1)).strftime("%m-%d-%Y")


@pytest.fixture
def new_service(new_provider, new_member, yesterday):
    return Service(yesterday, new_provider, new_member, 123456, "splinting", "I splinted his arm", 200.00)


def test_load_member_df(file_system):
    file_system._load_member_df()
    assert file_system._member_df is not None


def test_load_provider_df(file_system):
    file_system._load_provider_df()
    assert file_system._provider_df is not None


def test_load_service_df(file_system):
    file_system._load_service_df()
    assert file_system._service_directory_df is not None


# Geraldine,Simison,388789457,4528 Washington Junction,Olympia,WA,98516,false
def test_get_member_by_name(file_system):
    member = file_system.get_member_by_name("Simison")
    assert member.last_name == "Simison"
    assert member.first_name == "Geraldine"
    assert member.id == 388789457
    assert member.street == "4528 Washington Junction"
    assert member.city == "Olympia"
    assert member.state == "WA"
    assert member.zip == 98516
    assert member.is_suspended is False


def test_get_member_by_name_empty(empty_file_system):
    member = empty_file_system.get_member_by_name("Janning")
    assert member is None


def test_get_member_by_id(file_system):
    member = file_system.get_member_by_id(388789457)
    assert member.last_name == "Simison"
    assert member.first_name == "Geraldine"
    assert member.id == 388789457
    assert member.street == "4528 Washington Junction"
    assert member.city == "Olympia"
    assert member.state == "WA"
    assert member.zip == 98516
    assert member.is_suspended is False


def test_get_member_by_id_empty(empty_file_system):
    member = empty_file_system.get_member_by_id(22)
    assert member is None


def test_add_member(file_system, new_member):
    file_system.add_member(new_member)
    assert file_system.get_member_by_id(123456780) is not None


def test_add_member_fail(file_system):
    with pytest.raises(TypeError):
        file_system.add_member("Steve")


def test_remove_member(file_system, new_member):
    file_system.add_member(new_member)
    file_system.remove_member(new_member)
    assert file_system.get_member_by_id(123456780) is None


def test_remove_member_fail(file_system, new_member):
    with pytest.raises(ValueError):
        file_system.remove_member(new_member)


def test_add_provider(file_system, new_provider):
    file_system.add_provider(new_provider)
    assert file_system.get_provider_by_id(123456789) is not None


def test_remove_provider(file_system, new_provider):
    file_system.add_provider(new_provider)
    file_system.remove_provider(new_provider)
    assert file_system.get_provider_by_id(123456789) is None


def test_document_service(file_system, new_service, new_member, new_provider, yesterday):
    file_system.add_member(new_member)
    file_system.add_provider(new_provider)
    file_system.document_service(new_service, save_to_file=False)

    df = file_system._all_services_df
    assert len(df.index) > 0
    assert df[df["member_id"] == 123456780].iloc[0]["date_of_service"] == yesterday
    assert df[df["member_id"] == 123456780].iloc[0]["current_time"] != "00:00:00"
    assert df[df["member_id"] == 123456780].iloc[0]["date_of_service"] == yesterday
    assert df[df["member_id"] == 123456780].iloc[0]["provider_id"] == 123456789
    assert df[df["member_id"] == 123456780].iloc[0]["member_id"] == 123456780
    assert df[df["member_id"] == 123456780].iloc[0]["service_code"] == 123456
    assert df[df["member_id"] == 123456780].iloc[0]["service_name"] == "splinting"
    assert df[df["member_id"] == 123456780].iloc[0]["comments"] == "I splinted his arm"
    assert df[df["member_id"] == 123456780].iloc[0]["fee"] == 200.00

    df = file_system._get_member_report_info(new_service.member_id)
    assert len(df.index) == 1
    assert df[df["last_name"] == "Provider"].iloc[0]["date_of_service"] == yesterday
    assert df[df["last_name"] == "Provider"].iloc[0]["first_name"] == "Steve"
    assert df[df["last_name"] == "Provider"].iloc[0]["last_name"] == "Provider"
    assert df[df["last_name"] == "Provider"].iloc[0]["service_name"] == "splinting"

    df = file_system._get_provider_report_info(new_service.provider_id)
    assert len(df.index) == 1
    assert df[df["member_id"] == 123456780].iloc[0]["date_of_service"] == yesterday
    assert df[df["member_id"] == 123456780].iloc[0]["current_date"] != yesterday
    assert df[df["member_id"] == 123456780].iloc[0]["current_time"] != "00:00:00"
    assert df[df["member_id"] == 123456780].iloc[0]["first_name"] == "Steve"
    assert df[df["member_id"] == 123456780].iloc[0]["last_name"] == "Patient"
    assert df[df["member_id"] == 123456780].iloc[0]["member_id"] == 123456780
    assert df[df["member_id"] == 123456780].iloc[0]["service_code"] == 123456
    assert df[df["member_id"] == 123456780].iloc[0]["fee"] == 200.00


def test_get_member_report_as_string(file_system, new_member, new_provider, new_service, yesterday):
    file_system.add_member(new_member)
    file_system.add_provider(new_provider)
    file_system.document_service(new_service, save_to_file=False)
    report = file_system.get_member_report_as_string(new_service.member_id, save_to_file=False)
    assert report == f"Name: Steve Patient\nMember ID: 123456780\nStreet: 1234 Test St\nCity: Test City\nState: FA\nZipcode: 12345\n\tDOS: {yesterday}\n\tProvider Name: Steve Provider\n\tService: splinting\n\n"


def test_get_provider_report_as_string(file_system, new_member, new_provider, new_service, yesterday):
    file_system.add_member(new_member)
    file_system.add_provider(new_provider)
    file_system.document_service(new_service, save_to_file=False)
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    current_date = datetime.date.today().strftime("%m-%d-%Y")
    report = file_system.get_provider_report_as_string(new_service.provider_id, save_to_file=False)
    assert report == (f'Name: Steve Provider\n'
                      f'Provider ID: 123456789\n'
                      f'Street: 1234 Test St\n'
                      f'City: Test City\n'
                      f'State: FA\n'
                      f'Zipcode: 12345\n'
                             f'\tDOS: {yesterday}\n'
                             f'\tDate Processed: {current_date}\n'
                             f'\tTime Processed: {current_time}\n'
                             f'\tMember: Steve Patient\n'
                             f'\tMember ID: 123456780\n'
                             f'\tService Code: 123456\n'
                             f'\tFee: 200.0\n'
                             f'\n'
                      f'Total Consultations: 1\n'
                      f'Total Fees: 200.0\n')


def test_update_member(file_system, new_member):
    file_system.add_member(new_member)
    new_member.first_name = "Bob"
    file_system.update_member(new_member)
    assert file_system.get_member_by_id(123456780).first_name == "Bob"


def test_update_provider(file_system, new_provider):
    file_system.add_provider(new_provider)
    new_provider.first_name = "Bob"
    file_system.update_provider(new_provider)
    assert file_system.get_provider_by_id(123456789).first_name == "Bob"


def test_is_valid_employee(file_system):
    assert file_system.is_valid_employee(831130215) == True
    assert file_system.is_valid_employee(831130216) == False


def test_is_manager(file_system):
    assert file_system.is_manager(831130215) == True
    assert file_system.is_manager(831130216) == False


def test_get_maximum_member_id(file_system):
    assert file_system.get_maximum_member_id() == 971447942


def test_document_service_from_more_than_7_days_ago(file_system, service_from_more_than_7_days_ago, new_member, new_provider, save_to_file=False):
    file_system.add_member(new_member)
    file_system.add_provider(new_provider)
    file_system.document_service(service_from_more_than_7_days_ago, save_to_file=False)
    df = file_system._all_services_df
    assert len(df.index) != 0
    member_df = file_system._get_member_report_info(service_from_more_than_7_days_ago.member_id)
    provider_df = file_system._get_provider_report_info(service_from_more_than_7_days_ago.provider_id)

    assert len(member_df.index) == 0
    assert len(provider_df.index) == 0

