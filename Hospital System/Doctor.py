from Person import *
import os
import pandas as pd


class Doctor(Person):
    """
        'Doctor' is a subclass of 'Person' and includes additional attributes like 'specialization' and a list of 'patients'.
    """
    __doctors_db = "doctors.csv"
    __nurses_db = "nurses.csv"
    __patients_db = "patients.csv"
    __doctor_nurse_db = "doctor_nurse.csv"
    __doctor_patient_db = "doctor_patient.csv"

    def __init__(self, name, age, gender, phone, specialization):
        super().__init__(name, age, gender, phone)
        self.specialization = specialization
        self.patients = []

    @classmethod
    def empty_Doctor_constructor(cls):
        cls.name = ""
        cls.age = ""
        cls.gender = ""
        cls.phone = ""
        cls.specialization = ""

        return cls(cls.name,
                   cls.age,
                   cls.gender,
                   cls.phone,
                   cls.specialization,
                   )

    def add_patient(self, patient):
        self.patients.append(patient)
        print(f"Patient {patient.name} added to {self.name}'s list.")

    # Adding Nurse To The Team
    def check_doctor_db(self, doctor_name, doctor_phone):
        """
            Return True If Doctor Already EXist, and False if Not
        """
        if os.path.isfile(Doctor.__doctors_db):
            df = pd.read_csv(Doctor.__doctors_db)

            doctor_phone = f"'{doctor_phone}'"  # Same Stored Format
            filt = (df["Name"] == doctor_name) & (
                df["Phone"] == doctor_phone)
            if sum(filt) == 1:
                return True
            else:
                return False
        else:
            return False

    def check_nurse_db(self, nurse_name, nurse_phone):
        """
            Return True If Nurse Already EXist, and False if Not
        """
        if os.path.isfile(Doctor.__nurses_db):
            df = pd.read_csv(Doctor.__nurses_db)

            nurse_phone = f"'{nurse_phone}'"  # Same Stored Format

            filt = (df["Name"] == nurse_name) & (
                df["Phone"] == nurse_phone)

            if sum(filt) == 1:
                return True
            else:
                return False
        else:
            return False

    def check_patient_db(self, patient_id, patient_name):
        """
            Return True If Patient Already EXist, and False if Not
        """
        if os.path.isfile(Doctor.__patients_db):
            df = pd.read_csv(Doctor.__patients_db)

            filt = (df["Name"] == patient_name) & (
                df["Patient_ID"] == patient_id)

            if sum(filt) == 1:
                return True
            else:
                return False
        else:
            return False

    def add_nurse_to_team(self, doctor_name, doctor_phone, nurse_name, nurse_phone):
        if self.check_doctor_db(doctor_name, doctor_phone) and self.check_nurse_db(nurse_name, nurse_phone):
            doctor_phone = f"'{doctor_phone}'"
            nurse_phone = f"'{nurse_phone}'"
            row_to_check = pd.Series({"Doctor": doctor_name,
                                      "Doctor_Phone": doctor_phone,
                                      "Nurse": nurse_name,
                                      "Nurse_Phone": nurse_phone})

            if os.path.isfile(Doctor.__doctor_nurse_db):

                # Read Doctors_Nurse DB
                df = pd.read_csv(Doctor.__doctor_nurse_db)

                # To Check if The Nurse Already In The Doctor's Team
                # => True if There is No Duplicates
                if df[df.eq(row_to_check).all(axis=1)].empty:
                    df_to_append = pd.DataFrame([row_to_check])
                    pd.concat([df, df_to_append]).drop_duplicates().to_csv(
                        Doctor.__doctor_nurse_db,  index=False)

                else:
                    return -1
            else:
                df = pd.DataFrame([row_to_check])
                df.to_csv(Doctor.__doctor_nurse_db, index=False)
        else:
            return False

    def add_patient_to_doctor(self, doctor_name, doctor_phone, patient_id, patient_name):
        if self.check_doctor_db(doctor_name, doctor_phone) and self.check_patient_db(patient_id, patient_name):
            doctor_phone = f"'{doctor_phone}'"
            row_to_check = pd.Series({"Doctor": doctor_name,
                                      "Doctor_Phone": doctor_phone,
                                      "Patient": patient_name,
                                      "Patient_ID": patient_id})

            if os.path.isfile(Doctor.__doctor_patient_db):

                # Read Doctors_Nurse DB
                df = pd.read_csv(Doctor.__doctor_patient_db)

                # To Check if The Nurse Already In The Doctor's Team
                # => True if There is No Duplicates
                if df[df.eq(row_to_check).all(axis=1)].empty:
                    df_to_append = pd.DataFrame([row_to_check])
                    pd.concat([df, df_to_append]).drop_duplicates().to_csv(
                        Doctor.__doctor_patient_db,  index=False)

                else:
                    return -1
            else:
                df = pd.DataFrame([row_to_check])
                df.to_csv(Doctor.__doctor_patient_db, index=False)
        else:
            return False

    # def add_nurse(self, nurse):
    #     print(f"Nurse {nurse.name} added to {self.name}'s team.")

    def display_info(self):
        super().display_info()
        print(f"Specialization: {self.specialization}")
        print("Patients:")
        for patient in self.patients:
            print(f"- {patient.name}")

    def get_specialization(self):
        return self.specialization
