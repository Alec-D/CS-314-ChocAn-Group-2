from employee import Employee
from file_system import FileSystem
from service import Service
from member import Member
from provider import Provider

import os
import datetime

import pytest
import pandas as pd


@pytest.fixture
def file_system():
    return FileSystem("member_data.csv", "provider_data.csv", "service_dir.csv", "employee_data.csv")

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
def new_employee():
    return Employee(100)


# def test_things(file_system, empty_file_system, new_member, new_provider):
#     print("bla")

def test_new_employee(new_employee):
    assert new_employee.id == 100

def test_add_existing_member(new_employee, monkeypatch, capsys):
    inputs = iter(['Addekin'])
    monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
    new_employee.add_member()
    captured = capsys.readouterr()
    assert captured.out == "Member already exists\n"

def test_add_new_member(new_employee, monkeypatch):
    inputs = iter(['Test', 'Test', 'Test', '1234 Test St', 'Test City', 'CA', 12345, 1])
    monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
    new_employee.add_member()
    # print(new_employee.id)
    # print(new_employee.file_system)
    # print(file_system)
    assert new_employee.file_system.get_member_by_name('Test') is not None

def test_edit_member(new_employee, monkeypatch):
    inputs = iter(['Addekin', 'First Name', 'Changed', 'y'])
    monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
    new_employee.edit_member()
    assert new_employee.file_system.get_member_by_name('Addekin').first_name == 'Changed'

def test_delete_member(new_employee):
    new_employee.delete_member(399310330)
    assert new_employee.file_system.get_member_by_id(399310330) is None

def test_add_existing_provider(new_employee, monkeypatch, capsys):
    inputs = iter(['Aleixo'])
    monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
    new_employee.add_provider()
    captured = capsys.readouterr()
    assert captured.out == "Provider already exists\n"

def test_add_new_provider(new_employee, monkeypatch):
    inputs = iter(['Test', 'Test', 'Test', '1234 Test St', 'Test City', 'CA', 12345, 1])
    monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
    new_employee.add_provider()
    assert new_employee.file_system.get_provider_by_name('Test') is not None

def test_edit_provider(new_employee, monkeypatch):
    inputs = iter(['Aleixo', 'First Name', 'Changed', 'y', 'y'])
    monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
    new_employee.edit_provider()
    assert new_employee.file_system.get_provider_by_name('Aleixo').first_name == 'Changed'

def test_delete_provider(new_employee):
    new_employee.delete_provider(939285195)
    assert new_employee.file_system.get_provider_by_id(939285195) is None
