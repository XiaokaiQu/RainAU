from django.shortcuts import render
import csv
from rainAU.models import RainInAu
from datetime import datetime
from django.http import HttpResponse
from rainAU.data_process import dataClean
import uuid

def index(request):
    return HttpResponse("Hello, world. You're at the rainAU index.")

def showEx(request):
    example_rain_list = RainInAu.objects.order_by("-record_date")[:10]
    context = {"example_rain_list": example_rain_list}
    return render(request, "rainAU_main/showEx.html", context)

def error_view(request):
    return HttpResponse("Something is wrong")

def insert_data(request):
    file_path = './weatherAUS.csv'

    current_date = datetime.now()
    print("Start insert data: " + current_date.strftime('%m-%d-%y, %H:%M:%S'))
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            rain_data_to_insert = list()

            for row in reader:
                if dataClean.clean_NA(row['MinTemp']) and dataClean.clean_NA(row['MaxTemp']) and dataClean.clean_NA(row['Rainfall']) and dataClean.clean_NA(row['RainToday']) and dataClean.clean_NA(row['RainTomorrow']):
                    rain_data_to_insert.append(RainInAu(
                        location=row['Location'],
                        record_date=row['Date'],
                        #published_date=datetime.strptime(row['published_date'], '%Y-%m-%d').date(),
                        MinTemp=row['MinTemp'],
                        MaxTemp=row['MaxTemp'],
                        Rainfall=row['Rainfall'],
                        RainToday=dataClean.str2bool(row['RainToday']),
                        RainTomorrow=dataClean.str2bool(row['RainTomorrow']),
                        id=uuid.uuid4(),
                    ))

        RainInAu.objects.bulk_create(rain_data_to_insert)

        current_date = datetime.now()
        print("Finish insert data: " + current_date.strftime('%m-%d-%y, %H:%M:%S'))

        return HttpResponse("Success")
    except Exception as ex:
        print(ex)
        return HttpResponse("Fail")

