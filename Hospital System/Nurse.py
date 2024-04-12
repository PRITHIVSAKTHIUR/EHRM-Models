from Person import *


class Nurse(Person):
    """
        The 'Nurse' class inherits from the 'Person' class. This means that a 'Nurse' is a specialized type of 'Person' 
        and inherits the attributes and methods of the 'Person' class.
    """

    def __init__(self, name, age, gender, phone, shift):
        super().__init__(name, age, gender, phone)
        self.shift = shift

    def display_info(self):
        super().display_info()
        print(f"Shift: {self.shift}")

    def get_shift(self):
        return self.shift
