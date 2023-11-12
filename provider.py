class Provider:
    def __init__(self,
                 first_name: str,
                 last_name: str,
                 id: str | int,
                 street: str,
                 city: str,
                 state: str,
                 zip: str | int):
        self.first_name = first_name
        self.last_name = last_name
        self.id = id
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip

    def __str__(self):
        return (f"Name: {self.first_name} {self.last_name}\n"
                f"Provider ID: {self.id}\n"
                f"Street: {self.street}\n"
                f"City: {self.city}\n"
                f"State: {self.state}\n"
                f"Zipcode: {self.zip}")

    def __iter__(self):
        yield self.first_name
        yield self.last_name
        yield self.id
        yield self.street
        yield self.city
        yield self.state
        yield self.zip