from django.shortcuts import render
from django.http import HttpResponse
import codecs
import csv

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def uploadFile():
    dic = {}
    num = 1
    with codecs.open('../weatherAUS.csv', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f,skipinitialspace=True):
            if row['Location'] not in list(dic.values()):
                dic[str(num)] = row['Location']
                num+=1
    f.close()
    print(dic.items())
