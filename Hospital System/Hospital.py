from Doctor import *
from Nurse import *
from Patient import *
import os
import numpy as np
import pandas as pd


class Hospital:
    """
        In the 'Hospital' class, there are lists (self.doctors and self.nurses) that represent a composition 
        relationship with the 'Doctor' and 'Nurse' classes. The Hospital 'has' doctors and nurses as part of its composition. 
        The methods 'add_doctor' and 'add_nurse' are used to add instances of 'Doctor' and Nurse to the hospital.
    """
    # Doctors Data Structure
    __doctors_db = "doctors.csv"
    __doctors_list = []
    __doctors_dict = dict()

    # Nurse Data Structure
    __nurses_db = "nurses.csv"
    __nurses_list = []
    __nurses_dict = dict()

    # Patient Data Structure
    __patients_db = "patients.csv"
    __patients_list = []
    __patients_dict = dict()

    def __init__(self, name, location):
        self.name = name
        self.location = location

    # ============ Doctor ============

    def check_doctor_exist(self, doctor: Doctor):
        """
            Return True If User Exist Fasle If Not Return False
        """
        if doctor.get_phone() in [doc.get_phone() for doc in Hospital.__doctors_list]:
            return True

        else:
            if os.path.isfile(Hospital.__doctors_db):
                df = pd.read_csv(Hospital.__doctors_db)
                filt = (df["Phone"] == doctor.get_phone())
                if sum(filt) == 0:
                    return False
                else:
                    return True
            else:
                return False

    def add_doctor(self, doctor: Doctor):
        if self.check_doctor_exist(doctor):
            return False
        else:
            Hospital.__doctors_list.append(doctor)

    def save_doctor(self):
        if len(Hospital.__doctors_list) != 0:
            name, age, gender, phone, specializations = [], [], [], [], []
            for doctor in Hospital.__doctors_list:
                name.append(doctor.get_name())
                age.append(doctor.get_age())
                gender.append(doctor.get_gender())
                phone.append(doctor.get_phone())
                specializations.append(doctor.get_specialization())

            Hospital.__doctors_dict["Name"] = name
            Hospital.__doctors_dict["Age"] = age
            Hospital.__doctors_dict["Gender"] = gender
            Hospital.__doctors_dict["Phone"] = phone
            Hospital.__doctors_dict["Specialization"] = specializations

            df = pd.DataFrame(Hospital.__doctors_dict)
            if os.path.isfile(Hospital.__doctors_db):
                pd.concat([pd.read_csv(Hospital.__doctors_db), df]).drop_duplicates().to_csv(
                    Hospital.__doctors_db,  index=False)

                Hospital.__doctors_list = []
            else:
                df.to_csv(Hospital.__doctors_db, index=False)
                Hospital.__doctors_list = []
        else:
            return 0

    def get_all_doctors(self):
        if os.path.isfile(Hospital.__doctors_db):
            df = pd.read_csv(Hospital.__doctors_db)
            return df
        else:
            return pd.DataFrame()

    # ============ Nurse ============
    def check_nurse_exist(self, nurse: Nurse):
        """
            Return True If User Exist Fasle If Not Return False
        """
        if nurse.get_phone() in [nur.get_phone() for nur in Hospital.__nurses_list]:
            return True

        else:
            if os.path.isfile(Hospital.__nurses_db):
                df = pd.read_csv(Hospital.__nurses_db)
                filt = (df["Phone"] == nurse.get_phone())
                if sum(filt) == 0:
                    return False
                else:
                    return True
            else:
                return False

    def add_nurse(self, nurse: Nurse):
        if self.check_nurse_exist(nurse):
            return False
        else:
            Hospital.__nurses_list.append(nurse)

    def save_nurse(self):
        if len(Hospital.__nurses_list) != 0:
            name, age, gender, phone, shift = [], [], [], [], []
            for nurse in Hospital.__nurses_list:
                name.append(nurse.get_name())
                age.append(nurse.get_age())
                gender.append(nurse.get_gender())
                phone.append(nurse.get_phone())
                shift.append(nurse.get_shift())

            Hospital.__nurses_dict["Name"] = name
            Hospital.__nurses_dict["Age"] = age
            Hospital.__nurses_dict["Gender"] = gender
            Hospital.__nurses_dict["Phone"] = phone
            Hospital.__nurses_dict["Shift_Type"] = shift

            df = pd.DataFrame(Hospital.__nurses_dict)
            if os.path.isfile(Hospital.__nurses_db):
                pd.concat([pd.read_csv(Hospital.__nurses_db), df]).drop_duplicates().to_csv(
                    Hospital.__nurses_db,  index=False)

                Hospital.__nurses_list = []
            else:
                df.to_csv(Hospital.__nurses_db, index=False)
                Hospital.__nurses_list = []
        else:
            return 0

    def get_all_nurses(self):
        if os.path.isfile(Hospital.__nurses_db):
            df = pd.read_csv(Hospital.__nurses_db)
            return df
        else:
            return pd.DataFrame()

    # ============ Patient ===========
    def check_patient_exist(self, patient: Patient):
        """
            Return True If User Exist Fasle If Not Return False
        """
        if patient.get_phone() in [p.get_phone() for p in Hospital.__patients_list]:
            return True

        else:
            if os.path.isfile(Hospital.__patients_db):
                df = pd.read_csv(Hospital.__patients_db)
                filt = (df["Phone"] == patient.get_phone())
                if sum(filt) == 0:
                    return False
                else:
                    return True
            else:
                return False

    def add_patient(self, patient: Patient):
        if self.check_patient_exist(patient):

            return False
        else:
            Hospital.__patients_list.append(patient)

    def save_patient(self):
        if len(Hospital.__patients_list) != 0:
            patient_id, name, age, gender, phone = [], [], [], [], []
            for patient in Hospital.__patients_list:
                patient_id.append(patient.get_patient_id())
                name.append(patient.get_name())
                age.append(patient.get_age())
                gender.append(patient.get_gender())
                phone.append(patient.get_phone())

            Hospital.__patients_dict["Patient_ID"] = patient_id
            Hospital.__patients_dict["Name"] = name
            Hospital.__patients_dict["Age"] = age
            Hospital.__patients_dict["Gender"] = gender
            Hospital.__patients_dict["Phone"] = phone

            df = pd.DataFrame(Hospital.__patients_dict)
            if os.path.isfile(Hospital.__patients_db):
                pd.concat([pd.read_csv(Hospital.__patients_db), df]).drop_duplicates().to_csv(
                    Hospital.__patients_db,  index=False)

                Hospital.__patients_list = []
            else:
                df.to_csv(Hospital.__patients_db, index=False)
                Hospital.__patients_list = []
        else:
            return 0

    def get_all_patients(self):
        if os.path.isfile(Hospital.__patients_db):
            df = pd.read_csv(Hospital.__patients_db)
            return df
        else:
            return pd.DataFrame()

    def display_info(self):
        print(f"Hospital: {self.name}")
        print(f"Location: {self.location}")
        print("Doctors:")
        for doctor in Hospital.__doctors_list:
            print(f"- {doctor.name}")
        print("Nurses:")
        for nurse in self.nurses:
            print(f"- {nurse.name}")
