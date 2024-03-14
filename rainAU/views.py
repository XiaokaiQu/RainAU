from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.urls import reverse
from django.db.models  import Count
import csv, json
from datetime import datetime
from django.http import HttpResponse
from rainAU.models import RainInAu, LOCATION_CHOICES
from rainAU.data_process import dataClean, json_data
import logging
from django.core.cache import cache

logging = logging.getLogger(__name__)

#Ranking of Rain Probability Tomorrow
def rank_rain_poss(request):
    score_rain_rank = {}

    if cache.has_key('rain_poss_today'):
        score_rain_rank = cache.get('rain_poss_today')
    # If donot have value in cache, calculate
    else:
        today_date = datetime.now().strftime("-%m-%d")

        logging.info("Start calculate Rain Probability")

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
                score_rain[i['location']] = "{:.1f}%".format(score_rain.get(i['location'])/i['loca_num'] * 100)
            else:
                score_rain[i['location']] = '0.0%'

        logging.info("Finish calculate Rain Probability")

        #Sort by percentage
        score_rain_rank = dict(sorted(score_rain.items(),key = lambda x:x[1],reverse = True))
        cache.set('rain_poss_today',score_rain_rank,timeout=36000)

    return render(request, "map_forecast.html",{'score_rain_rank': score_rain_rank})
   
#Historical Temperature
#Historical Rainfall vs Evaporation
def history_charPage(request,loc,type):
    filter_type1 = ''
    filter_type2 = ''
    template_name = ''
    loc_list = []

    logging.info("Start get data for chart")

    if type=='1':
        filter_type1 = 'Rainfall'
        filter_type2 = 'Evaporation'
        template_name = 'historical_rainfall.html'
        for i in LOCATION_CHOICES[1:]:
            loc_list.append(i[1])
        loc_list.sort()
    else:
        filter_type1 = 'MinTemp'
        filter_type2 = 'MaxTemp'
        template_name = 'historical_temperature.html'

    temp_data = RainInAu.objects.filter(location=loc).values('record_date',filter_type1,filter_type2).order_by('record_date')
    
    if len(temp_data) == 0:
        raise Exception(1001,"No valid values found")
    
    #Get category/date
    date_list = []
    #Get Rainfall/MinTemp
    first_list = []
    #Get Evaporation/MaxTemp
    second_list = []
    for i in temp_data:
        date_list.append(i['record_date'])
        first_list.append(i[filter_type1])
        second_list.append(i[filter_type2])

    logging.info("Finish calculate Rain Probability")

    send_context = json.dumps({"date_list":date_list,"first_list":first_list,"second_list":second_list},cls=json_data.DecEncoder)

    return render(request, template_name, {"send_context":send_context,"loc":loc,"loc_list":loc_list})

class RainInAUListView(ListView):
    model = RainInAu
    template_name = "location_detail.html"
    paginate_by = 20 # 20 data per page
    
    def get_queryset(self):
        logging.info("Start query list by location")

        loc_val = self.kwargs.get('loc')
        # If the 'location' is defined, the result will be filtered
        if loc_val:
            return super().get_queryset().filter(location=loc_val).order_by('record_date')
        else:
            logging.info("Dont have location info, turn to query all data")

            return super().get_queryset().order_by('location','record_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loc_val = self.kwargs.get('loc')
        if loc_val:
            context['loc'] = self.kwargs.get('loc')
        return context

def download_csv(request):
    logging.info("Start download file")
    try:
        #File name
        file_name = 'RainInAu' + datetime.now().strftime('%Y%m%d%H%M%S%f') + '.csv'
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=' + file_name

        writer = csv.writer(response)
        
        # Title
        title_list = ['Location','RecordDate']
        for field in RainInAu._meta.get_fields()[3:]:
            title_list.append(field.name)
        writer.writerow(title_list)

        # Data
        rain_datas = RainInAu.objects.all().values_list().order_by('location','record_date')
        for rain_data in rain_datas:
            writer.writerow(rain_data[1:])
        #writer.writerows(list(rain_datas))
            
        logging.info("Finish download file")
        return response
    
    except Exception as ex:
        logging.error("Download file have error:"+ex)
        return HttpResponse("Fail")

def error_view(request):
    return render(request,'error.html')

def insert_data(request):
    logging.info("Start insert file")
    file_path = './weatherAUS.csv'

    current_date = datetime.now()
    print("Start insert data: " + current_date.strftime('%m-%d-%y, %H:%M:%S'))
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            rain_data_to_insert = list()

            for row in reader:
                rain_data_to_insert.append(RainInAu(
                    location=None if row['Location'] == 'NA' else row['Location'],
                    record_date=None if row['Date'] == 'NA' else row['Date'],
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

        return redirect(reverse("rainAU:rankRP"))
    except Exception as ex:
        logging.error("Upload file have error:"+ex)
        return render(request,'error.html')