from Person import *
import os
import pandas as pd


class Patient(Person):
    """
        'Patient' is another subclass of 'Person' and includes attributes like 'patient_id' and a reference to the assigned 'doctor'.
    """
    __patient_counter = 1
    __doctor_patient_db = "doctor_patient.csv"
    __doctors_db = "doctors.csv"
    __patients_db = "patients.csv"

    def count_rows_csv(file_path):
        try:
            with open(file_path, 'rb') as file:
                line_count = sum(1 for line in file)
            return line_count

        except Exception as e:
            return 1

    if __patient_counter == 1 and os.path.isfile("patients.csv"):
        __patient_counter = count_rows_csv("patients.csv")

    def __init__(self, name, age, gender, phone):
        super().__init__(name, age, gender, phone)
        self.patient_id = f"PID_{Patient.__patient_counter:03d}"
        Patient.__patient_counter += 1
        self.doctor = None

    @classmethod
    def empty_patient_constructor(cls):
        cls.name = ""
        cls.age = ""
        cls.gender = ""
        cls.phone = ""

        return cls(cls.name,
                   cls.age,
                   cls.gender,
                   cls.phone,
                   )

    def check_doctor_db(self, doctor_name, doctor_phone):
        """
            Return True If Doctor Already EXist, and False if Not
        """
        if os.path.isfile(Patient.__doctors_db):
            df = pd.read_csv(Patient.__doctors_db)

            doctor_phone = f"'{doctor_phone}'"  # Same Stored Format
            filt = (df["Name"] == doctor_name) & (
                df["Phone"] == doctor_phone)
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
        if os.path.isfile(Patient.__patients_db):
            df = pd.read_csv(Patient.__patients_db)

            filt = (df["Name"] == patient_name) & (
                df["Patient_ID"] == patient_id)

            if sum(filt) == 1:
                return True
            else:
                return False
        else:
            return False

    def assign_doctor_to_pateint(slef, doctor_name, doctor_phone, patient_id, patient_name):
        if slef.check_doctor_db(doctor_name, doctor_phone) and slef.check_patient_db(patient_id, patient_name):
            doctor_phone = f"'{doctor_phone}'"
            row_to_check = pd.Series({"Doctor": doctor_name,
                                      "Doctor_Phone": doctor_phone,
                                      "Patient": patient_name,
                                      "Patient_ID": patient_id})

            if os.path.isfile(Patient.__doctor_patient_db):

                # Read Doctors_Nurse DB
                df = pd.read_csv(Patient.__doctor_patient_db)

                # To Check if The Nurse Already In The Doctor's Team
                # => True if There is No Duplicates
                if df[df.eq(row_to_check).all(axis=1)].empty:
                    df_to_append = pd.DataFrame([row_to_check])
                    pd.concat([df, df_to_append]).drop_duplicates().to_csv(
                        Patient.__doctor_patient_db,  index=False)

                else:
                    return -1
            else:
                df = pd.DataFrame([row_to_check])
                df.to_csv(Patient.__doctor_patient_db, index=False)
        else:
            return False

    def assign_doctor(self, doctor):
        self.doctor = doctor
        print(f"{self.name} assigned to Dr. {doctor.name}")

    def display_info(self):
        super().display_info()
        print(f"Patient ID: {self.patient_id}")
        if self.doctor:
            print(f"Assigned Doctor: {self.doctor.name}")
        else:
            print("No assigned doctor.")

    def get_patient_id(self):
        return self.patient_id
