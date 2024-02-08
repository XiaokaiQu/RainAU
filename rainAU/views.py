from django.shortcuts import render
import csv
from rainAU.models import RainInAu
from datetime import datetime
from django.http import HttpResponse
from rainAU.data_process import dataClean


def main_map(request):
    return render(request, "map_forecast.html")

# def showEx(request):
#     example_rain_list = RainInAu.objects.order_by("-record_date")[:10]
#     context = {"example_rain_list": example_rain_list}
#     return render(request, "rainAU_main/showEx.html", context)

def rank_rain_poss(request):
    a = datetime.today()
    print(a)
    #ROUND(COUNT(CASE WHEN result='A' THEN result END)/COUNT(*),2) AS rate1
    #RainInAu.objects.values('location','')
    return HttpResponse("Success")


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
            num = 0
            for row in reader:
                rain_data_to_insert.append(RainInAu(
                    location=None if row['Location'] == 'NA' else row['Location'],
                    record_date=None if row['Date'] == 'NA' else row['Date'],
                    #published_date=datetime.strptime(row['published_date'], '%Y-%m-%d').date(),
                    MinTemp=None if row['MinTemp'] == 'NA' else row['MinTemp'],
                    MaxTemp=None if row['MaxTemp'] == 'NA' else row['MaxTemp'],
                    Rainfall=None if row['Rainfall'] == 'NA' else row['Rainfall'],
                    Evaporation=None if row['Evaporation'] == 'NA' else row['Evaporation'],
                    Sunshine=None if row['Sunshine'] == 'NA' else row['Sunshine'],
                    WindGustDir=None if row['WindGustDir'] == 'NA' else row['WindGustDir'],
                    WindGustSpeed=None if row['WindGustSpeed'] == 'NA' else row['WindGustSpeed'],
                    WindDir9am=None if row['WindDir9am'] == 'NA' else row['WindDir9am'],
                    WindDir3pm=None if row['WindDir3pm'] == 'NA' else row['WindDir3pm'],
                    WindSpeed9am=None if row['WindSpeed9am'] == 'NA' else row['WindSpeed9am'],
                    WindSpeed3pm=None if row['WindSpeed3pm'] == 'NA' else row['WindSpeed3pm'],
                    Humidity9am=None if row['Humidity9am'] == 'NA' else row['Humidity9am'],
                    Humidity3pm=None if row['Humidity3pm'] == 'NA' else row['Humidity3pm'],
                    Pressure9am=None if row['Pressure9am'] == 'NA' else row['Pressure9am'],
                    Pressure3pm=None if row['Pressure3pm'] == 'NA' else row['Pressure3pm'],
                    Cloud9am=None if row['Cloud9am'] == 'NA' else row['Cloud9am'],
                    Cloud3pm=None if row['Cloud3pm'] == 'NA' else row['Cloud3pm'],
                    Temp9am=None if row['Temp9am'] == 'NA' else row['Temp9am'],
                    Temp3pm=None if row['Temp3pm'] == 'NA' else row['Temp3pm'],
                    RainToday=dataClean.str2bool(row['RainToday']),
                    RainTomorrow=dataClean.str2bool(row['RainTomorrow']),
                ))

        RainInAu.objects.bulk_create(rain_data_to_insert)

        current_date = datetime.now()
        print("Finish insert data: " + current_date.strftime('%m-%d-%y, %H:%M:%S'))

        return HttpResponse("Success")
    except Exception as ex:
        print(ex)
        return HttpResponse("Fail")

