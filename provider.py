class Provider:
    def __init__(self, first_name, last_name, id, street, city, state, zip):
        self.first_name = first_name
        self.last_name = last_name
        self.id = id
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip

    def __str__(self):
        return f"Name: {self.first_name} {self.last_name}\nProvider ID: {self.id}\nStreet: {self.street}\nCity: {self.city}\nState: {self.state}\nZipcode: {self.zip}"

    def __iter__(self):
        yield self.first_name
        yield self.last_name
        yield self.id
        yield self.street
        yield self.city
        yield self.state
        yield self.zip