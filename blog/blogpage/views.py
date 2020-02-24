from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime


# Create your views here.
def get_month(num):
    if num == "1" or num == "01":
        return "Jan".upper()
    elif num == "2" or num == "02":
        return "Feb".upper()
    elif num == "3" or num == "03":
        return "Mar".upper()
    elif num == "4" or num == "04":
        return "Apr".upper()
    elif num == "5" or num == "05":
        return "May".upper()
    elif num == "6" or num == "06":
        return "Jun".upper()
    elif num == "7" or num == "07":
        return "Jul".upper()
    elif num == "8" or num == "08":
        return "Aug".upper()
    elif num == "9" or num == "09":
        return "Sep".upper()
    elif num == "10":
        return "Oct".upper()
    elif num == "11":
        return "Nov".upper()
    elif num == "12":
        return ("Dec").upper()
    else:
        raise ValueError

def home(request):
    data = fetchAPI()
    tempdata = data
    for i in tempdata:
        a = i['date'].split('-')
        b = a[2].split('T')
        #c = b[1].split(':')
        desc = i['content'][0:285] + "..."
        current_month = get_month(a[1])
        i.update({'month':current_month})
        i.update({'day': b[0]})
        i.update({'desc': desc})
    page = request.GET.get('page', 1)
    paginator = Paginator(tempdata, 2)
    try:
        blog = paginator.page(page)
    except PageNotAnInteger:
        blog = paginator.page(1)
    except EmptyPage:
        blog = paginator.page(paginator.num_pages)
    return render(request, 'blogpage/blog.html', {'blog': blog})

def fetchAPI():
    r = requests.get('http://saha2201.pythonanywhere.com/api/article/?format=json')
    r2 = r.json()
    return r2
    '''r3 = r2['product']
    r4 = r3[1]'''


def test(request):
    user_list = ['ABC', 'ABC', 'ABC', 'ABC', 'ABC', 'ABC', 'ABC', 'ABC','ABC', 'ABC', 'ABC', 'ABC']
    page = request.GET.get('page', 1)
    paginator = Paginator(user_list, 3)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'blogpage/user_list.html', {'users': users})