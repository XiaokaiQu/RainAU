from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import ListView
from django.urls import reverse
from django.db.models  import Count
import csv
from datetime import datetime
from django.http import HttpResponse
from rainAU.models import RainInAu
from rainAU.data_process import dataClean, json_data
import json

#Jump to Home Page
def main_map(request):
    return redirect(reverse("rainAU:rankRP"))

# def showEx(request):
#     example_rain_list = RainInAu.objects.order_by("-record_date")[:10]
#     context = {"example_rain_list": example_rain_list}
#     return render(request, "rainAU_main/showEx.html", context)

#Ranking of Rain Probability Tomorrow
def rank_rain_poss(request):

    today_date = datetime.now().strftime("-%m-%d")

    #Obtain the total number of certain location today 
    today_count = RainInAu.objects.filter(record_date__endswith=today_date).values('location').annotate(loca_num = Count('location'))
    #Obtain the times of rainy in certain location today
    today_rain_count = list(RainInAu.objects.filter(record_date__endswith=today_date,RainTomorrow=True).values('location').annotate(loca_rain_num = Count('location')))
    
    #store the probability of rain in certain location
    score_rain = {}

    for j in today_rain_count:
        score_rain[j['location']] = j['loca_rain_num']

    #Calculate percentage
    for i in list(today_count):
        if i['location'] in score_rain.keys():
            score_rain[i['location']] = str(round(score_rain.get(i['location'])/i['loca_num'],2) * 100) + '%'
        else:
            score_rain[i['location']] = '0.0%'

    #Sort by percentage
    score_rain_rank = dict(sorted(score_rain.items(),key = lambda x:x[1],reverse = True))

    return render(request, "map_forecast.html",{'score_rain_rank': score_rain_rank})


# class LocationDetailView(ListView):
#     model = RainInAu
#     template_name = 'historical_temperature.html'
#     context_object_name = 'RainInAu'

#     def get_queryset(self):
#         return RainInAu.objects.filter(location=self.request.location).order_by('-record_date')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['loc'] =  self.request.location
#         return context
    
#Historical Temperature
def hty_tmp_location(request, loc):
    print(loc)
    temp_data = RainInAu.objects.filter(location=loc).values('record_date','MinTemp','MaxTemp').order_by('record_date')

    #Get category/date
    date_list = []
    #Get MinTemp
    minTemp_list = []
    #Get MaxTemp
    maxTemp_list = []
    
    for i in temp_data:
        date_list.append(i['record_date'])
        minTemp_list.append(i['MinTemp'])
        maxTemp_list.append(i['MaxTemp'])

    send_context = json.dumps({"date_list":date_list,"minTemp_list":minTemp_list,"maxTemp_list":maxTemp_list},cls=json_data.DecEncoder)

    return render(request, "historical_temperature.html", {"send_context":send_context,"loc":loc})

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