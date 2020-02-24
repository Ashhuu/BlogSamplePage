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
    latest = tempdata[0]
    recentlist = [latest]
    searchlist = []
    categoryCount = countCategory(data)
    current_year, current_month1, current_date, current_hour, current_min, current_sec = splitdate(latest['date'])
    dmy = (current_year + "/" + current_month1 + "/" +
           current_date + " " + current_hour + ":" + current_min + ":" + current_sec)
    latestdmy = datetime.strptime(dmy, '%Y/%m/%d %H:%M:%S')
    for i in tempdata:
        current_year, current_month1, current_date, current_hour, current_min, current_sec = splitdate(i['date'])
        desc = i['content'][0:285] + "..."
        current_month = get_month(current_month1)
        i.update({'month': current_month})
        i.update({'monthN': current_month1})
        i.update({'day': current_date})
        i.update({'year': current_year})
        i.update({'desc': desc})
        dmy = (current_year + "/" + current_month1 + "/" +
               current_date + " " + current_hour + ":" + current_min + ":" + current_sec)
        dmy1 = datetime.strptime(dmy, '%Y/%m/%d %H:%M:%S')
        if dmy1 > latestdmy:
            latestdmy = dmy1
            latest = i
            recentlist.append(latest)
    recent = recentlist[:4]
    category = request.GET.get('category', 1)
    search = request.GET.get('search', 1)
    categoryList = []
    page = request.GET.get('page', 1)
    if category is not 1 and search is 1:
        for i in tempdata:
            if i['category'] == category:
                categoryList.append(i)
        paginator = Paginator(categoryList, 2)
    elif search is not 1:
        for i in tempdata:
            if search in i['title'] or search in i['desc']:
                searchlist.append(i)
                paginator = Paginator(searchlist, 2)
    else:
        paginator = Paginator(tempdata, 2)
    try:
        blog = paginator.page(page)
    except PageNotAnInteger:
        blog = paginator.page(1)
    except EmptyPage:
        blog = paginator.page(paginator.num_pages)
    return render(request, 'blogpage/blog.html', {'blog': blog, 'recent': recent[::-1], 'cData': categoryCount})


def splitdate(dt):
    a = dt.split('-')
    b = a[2].split('T')
    c = b[1].split(':')
    d = c[2].split('.')
    return a[0], a[1], b[0], c[0], c[1], d[0]


def fetchAPI():
    r = requests.get('http://saha2201.pythonanywhere.com/api/article/?format=json')
    r2 = r.json()
    return r2


def countCategory(data):
    addedCategory = []
    count = {}
    for i in data:
        if i['category'] in addedCategory:
            counter = count[i['category']]
            count.update({i['category']: counter+1})
        else:
            addedCategory.append(i['category'])
            count.update({i['category']: 1})
    return count


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