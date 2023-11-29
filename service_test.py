from service import Service
from member import Member
from provider import Provider

import pytest

@pytest.fixture
def new_service():
    new_provider = Provider('Bob', 'Smith', 1111711, '1234 Maple Lane', 'Alameda', 'CA', 77081)
    new_member = Member('John', 'Robert', 111111111, '1612 Grand St', 'Alameda', 'CA', 94501, False)
    
    return Service('12/12/12',new_provider,new_member,123456,'Accupuncture','holiday special',99.99)

def test_new_service(new_service):
    assert new_service.date_of_service == '12/12/12'
    assert new_service.provider_id == 1111711
    assert new_service.provider_first_name == 'Bob'
    assert new_service.provider_last_name == 'Smith'
    assert new_service.member_id == 111111111
    assert new_service.member_first_name == 'John'
    assert new_service.member_last_name == 'Robert'
    assert new_service.service_code == 123456
    assert new_service.service_name == 'Accupuncture'
    assert new_service.comments == 'holiday special'
    assert new_service.fee == 99.99

def test_get_member_report_info(new_service):
    assert new_service.get_member_report_info() == ['12/12/12','Bob','Smith','Accupuncture']
