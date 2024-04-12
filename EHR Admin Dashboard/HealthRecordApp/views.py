from django.shortcuts import render
from .models import HealthRecord
# Create your views here.

def Table_view(request):
    Patient_Record = HealthRecord.objects.all()
    return render(request,'HealthRecordApp/Table.html',{
        'data':Patient_Record})

