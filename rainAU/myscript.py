from datetime import datetime
from rainAU.models import RainInAu
from django.core.cache import cache
from django.db.models  import Count

def cal_rain_poss():
    cache.delete('rain_poss_today')

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

    cache.set('rain_poss_today',score_rain_rank)