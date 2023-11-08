import datetime
from member import Member
from provider import Provider


class Service:
    def __init__(self,
                 date_of_service,
                 provider,
                 member,
                 service_code,
                 service_name,
                 comments,
                 fee):

        if not isinstance(provider, Provider):
            raise TypeError("provider must be of type Provider")

        if not isinstance(member, Member):
            raise TypeError("member must be of type Member")

        self.current_date = datetime.date.today().strftime("%m-%d-%Y")
        self.current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.date_of_service = date_of_service
        self.provider_id = provider.id
        self.provider_first_name = provider.first_name
        self.provider_last_name = provider.last_name
        self.member_id = member.id
        self.member_first_name = member.first_name
        self.member_last_name = member.last_name
        self.service_code = service_code
        self.service_name = service_name
        self.comments = comments
        self.fee = fee

    def get_member_report_info(self):
        return [self.date_of_service,
                self.provider_first_name, 
                self.provider_last_name, 
                self.service_name]

    def get_provider_report_info(self):
        return [self.date_of_service,
                self.current_date,
                self.current_time,
                self.member_first_name,
                self.member_last_name,
                self.member_id,
                self.service_code,
                self.fee]

    def __iter__(self):
        yield self.current_date
        yield self.current_time
        yield self.date_of_service
        yield self.provider_id
        yield self.provider_first_name
        yield self.provider_last_name
        yield self.member_id
        yield self.member_first_name
        yield self.member_last_name
        yield self.service_code
        yield self.service_name
        yield self.comments
        yield self.fee