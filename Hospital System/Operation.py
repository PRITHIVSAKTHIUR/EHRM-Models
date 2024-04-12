import os
import pandas as pd


class Operation:
    """
        In the 'Operation' class, the attribute 'self.surgeon' represents a composition relationship with the 'Doctor' class. 
        Additionally, the list 'self.nurses' represents a composition relationship with the 'Nurse' class. 
        The method 'add_nurse' is used to add instances of 'Nurse' to the operation.
    """

    __operation_db = "operations.csv"
    __nurses_list = []
    __operation_count = 1

    def count_rows_csv(file_path):
        try:
            with open(file_path, 'rb') as file:
                line_count = sum(1 for line in file)
            return line_count

        except Exception as e:
            return 1

    if __operation_count == 1 and os.path.isfile("operations.csv"):
        __operation_count = count_rows_csv("patients.csv")

    def __init__(self, name, date, time, surgeon, nurses=[]):
        self.__name = name
        self.__date = date
        self.__time = time
        self.__surgeon = surgeon
        self.__nurses = nurses
        self.__operation_id = f"{name}_{surgeon}_{Operation.__operation_count}"

    @classmethod
    def empty_operation_constructor(cls):
        cls.name = ""
        cls.date = ""
        cls.time = ""
        cls.surgeon = ""
        cls.nurses = []

        return cls(cls.name,
                   cls.date,
                   cls.time,
                   cls.surgeon,
                   cls.nurses
                   )

    # ===== Getter Methods =====

    def get_operation_name(self):
        return self.__name

    def get_operation_date(self):
        return self.__date

    def get_operation_time(self):
        return self.__time

    def get_operation_surgeon(self):
        return self.__surgeon

    def get_operation_id(self):
        return self.__operation_id

    def get_nurses(self):
        return "/".join(Operation.__nurses_list)

    # ======= Setter Methods =======

    def set_operation_name(self, operation_name):
        self.__name = operation_name

    def set_operation_date(self, operation_date):
        self.__date = operation_date

    def set_operation_time(self, operation_time):
        self.__time = operation_time

    def set_operation_surgeon(self, operation_surgeon):
        self.__surgeon = operation_surgeon

    def set_operation_id(self, operation_name, surgeon_name):
        self.__operation_id = f"{operation_name[0:4]}_{surgeon_name}_{Operation.__operation_count}"

    def add_nurse(self, nurse_name):
        if nurse_name not in Operation.__nurses_list:
            Operation.__nurses_list.append(nurse_name)
        else:
            return 0

    def create_operation(self):
        row_to_check = pd.Series({"Operation_ID": self.get_operation_id(),
                                  "Date": self.get_operation_date(),
                                  "Time": self.get_operation_time(),
                                  "Surgeon": self.get_operation_surgeon(),
                                  "Nurses": self.get_nurses()})

        if os.path.isfile(Operation.__operation_db):
            # Read Doctors_Nurse DB
            df = pd.read_csv(Operation.__operation_db)

            # To Check if The Nurse Already In The Doctor's Team
            # => True if There is No Duplicates
            if df[df.eq(row_to_check).all(axis=1)].empty:
                df_to_append = pd.DataFrame([row_to_check])
                print(df_to_append)
                pd.concat([df, df_to_append]).drop_duplicates().to_csv(
                    Operation.__operation_db,  index=False)
                Operation.__nurses_list = []
            else:
                return -1
        else:
            df = pd.DataFrame([row_to_check])
            df.to_csv(Operation.__operation_db, index=False)
            Operation.__nurses_list = []

    def get_all_operation(self):
        if os.path.isfile(Operation.__operation_db):
            df = pd.read_csv(Operation.__operation_db)
            return df
        else:
            return pd.DataFrame()

    def display_info(self):
        print(f"Operation: {self.name}")
        print(f"Date: {self.date}, Time: {self.time}")
        print(f"Surgeon: {self.surgeon.name}")
        print("Nurses:")
        for nurse in self.nurses:
            print(f"- {nurse.name}")
