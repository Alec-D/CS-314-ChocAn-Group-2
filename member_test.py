from member import Member
import pytest


@pytest.fixture
def new_member():
    return Member('Nathalie', 'Owen', 111111111, '1612 Grand St', 'Alameda', 'CA', 94501, False)


def test_edit_member_name(monkeypatch, capsys, new_member):
    inputs = iter(['First Name', 'Changed', 'y'])
    monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
    new_member.edit_member()
    captured = capsys.readouterr()

    assert new_member.first_name == 'Changed'

def test_edit_member_state(monkeypatch, capsys, new_member):
    inputs = iter(['State', 'TX', 'y'])
    monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
    new_member.edit_member()
    captured = capsys.readouterr()

    assert new_member.state == 'TX'

def test_edit_member_zip(monkeypatch, capsys, new_member):
    inputs = iter(['Zip', 77081, 'y'])
    monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
    new_member.edit_member()
    captured = capsys.readouterr()

    assert new_member.zip == 77081

def test_edit_member_status(monkeypatch, capsys, new_member):
    inputs = iter(['Status', 'y', 'y'])
    monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
    new_member.edit_member()
    captured = capsys.readouterr()

    assert new_member.is_suspended == True

def test_build_member(monkeypatch, capsys):
    inputs = iter(['Test', 'Test', '1234 Test St', 'Test City', 'CA', 12345, 1])
    monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
    new_member = Member.build_member()
    captured = capsys.readouterr()

    assert new_member.first_name == 'Test'
    assert new_member.last_name == 'Test'
    assert new_member.street == '1234 Test St'
    assert new_member.city == 'Test City'
    assert new_member.state == 'CA'
    assert new_member.zip == 12345

