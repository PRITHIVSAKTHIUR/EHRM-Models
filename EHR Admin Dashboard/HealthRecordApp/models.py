from django.db import models

# Create your models here.

class HealthRecord(models.Model):

    Gender_Choice =[
        ('Male','MALE'),('Female','FEMALE')
    ]
    Blood_Choice=[
        ('O-','O-ve'),('O+','O+ve'),('B-','B-ve'),('B+','B+ve'),('AB+','AB+ve'),('AB-','AB-ve'),('A+','A+ve'),('A-','A-ve') 
    ]
    Admission_Choice=[
        ('Elective','Elective'),('Emergency','Emergency'),('Urgent','Urgent')
    ]
    Result_Choice=[
        ('Abnormal','Abnormal'),('Inconclusive','Inconclusive'),('Normal','Normal')
    ]
    Name = models.CharField(max_length=20)
    Age = models.IntegerField()
    Gender = models.CharField(max_length=20,choices=Gender_Choice)
    Blood_Type =models.CharField(max_length=20,choices=Blood_Choice)
    Medical_Condition= models.CharField(max_length=20)
    Date_of_Admission = models.DateField()
    Doctor = models.CharField(max_length=20)
    Hospital = models.CharField(max_length=20,default='hospital A')
    Insurance_Provider= models.CharField(max_length=20)
    Billing_Amount=models.FloatField()
    Room_Number=models.IntegerField()
    Admission_Type =models.CharField(max_length=20,choices=Admission_Choice)
    Discharge_Date=models.DateField()
    Medication=models.CharField(max_length=20)
    Test_Result=models.CharField(max_length=20,choices=Result_Choice)
    