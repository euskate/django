from django.shortcuts import render
from django.http import HttpResponse

# insert1
from .models import Item

# select1
from .serializers import ItemSerializer
from rest_framework.renderers import JSONRenderer
import json


# Create your views here.

def select_test(request):
    # ?key=abc&num=10&search='가'
    # key와 num 물품 갯수, search 이름 들어간 것
    
    key = request.GET.get("key","")
    num = int(request.GET.get("num",1))
    search = request.GET.get("search","")
    # 원래는 key를 DB에서 확인
    
    data = json.dumps({"ret":'key error'})

    if key == 'abc':
        # obj = Item.objects.all()[:num]
        obj = Item.objects.filter(name__contains=search)[:num]
        # print(obj)W
        serializer = ItemSerializer(obj, many=True)
        data = JSONRenderer().render(serializer.data)
    
    return HttpResponse(data)


def select1(request):
    key = request.GET.get("key","")
    no = request.GET.get("no",1)
    # 원래는 key를 DB에서 확인

    data = json.dumps({"ret":'key error'})

    if key == 'abc':
        obj = Item.objects.get(no=no)
        serializer = ItemSerializer(obj)
        data = JSONRenderer().render(serializer.data)

    return HttpResponse(data)

def select2(request):
    obj = Item.objects.all()
    serializer = ItemSerializer(obj, many=True)
    data = JSONRenderer().render(serializer.data)
    return HttpResponse(data)


def insert1(request):
    objs = []
    for i in range(1, 11, 1):
        obj = Item()
        obj.name = '책'+str(i)
        obj.price = i*500+7000
        objs.append(obj)

        Item.objects.bulk_create(objs)

    return HttpResponse("insert1")

