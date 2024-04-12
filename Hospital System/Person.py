class Person:
    """
        'Person' is a base class that represents a generic person with attributes like 'name', 'age', and 'gender'.
    """

    def __init__(self, name, age, gender, phone):
        self.name = name
        self.age = age
        self.gender = gender
        self.phone = phone

    def display_info(self):
        print(
            f"Name: {self.name}, Age: {self.age}, Gender: {self.gender},  Phone: {self.phone}")

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

    def get_gender(self):
        return self.gender

    def get_phone(self):
        return self.phone
