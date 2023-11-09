class Member:
    def __init__(self, first_name, last_name, id, street, city, state, zip, is_suspended):
        self.first_name = first_name
        self.last_name = last_name
        self.id = id
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.is_suspended = is_suspended

    def __iter__(self):
        yield self.first_name
        yield self.last_name
        yield self.id
        yield self.street
        yield self.city
        yield self.state
        yield self.zip
        yield self.is_suspended

    def __str__(self):
        return f"Name: {self.first_name} {self.last_name}\nMember ID: {self.id}\nStreet: {self.street}\nCity: {self.city}\nState: {self.state}\nZipcode: {self.zip}"