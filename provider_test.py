#provider tests
from provider import Provider
import pytest

@pytest.fixture
def new_provider():
    return Provider('Nathalie', 'Owen', 111111111, '1234 Maple Lane', 'Alameda', 'CA', 77081)

def test_edit_provider_name(monkeypatch, capsys, new_provider):
    inputs = iter(['First Name', 'Richard', 'y', 'y'])
    monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
    new_provider.edit_provider()
    captured = capsys.readouterr()

    assert new_provider.first_name == 'Richard'

def test_edit_provider_state(monkeypatch, capsys, new_provider):
    inputs = iter(['State', 'TX', 'y', 'y'])
    monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
    new_provider.edit_provider()
    captured = capsys.readouterr()

    assert new_provider.state == 'TX'

def test_edit_provider_zip(monkeypatch, capsys, new_provider):
    inputs = iter(['Zip', 77081, 'y', 'y'])
    monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
    new_provider.edit_provider()
    captured = capsys.readouterr()

    assert new_provider.zip == 77081

def test_build_provider(monkeypatch, capsys):
    inputs = iter(['Test', 'Test','1234 Test St', 'Test City', 'CA', 12345, 1])
    monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
    new_provider = Provider.build_provider()
    captured = capsys.readouterr()

    assert new_provider.first_name == 'Test'
    assert new_provider.last_name == 'Test'
    assert new_provider.street == '1234 Test St'
    assert new_provider.city == 'Test City'
    assert new_provider.state == 'CA'
    assert new_provider.zip == 12345