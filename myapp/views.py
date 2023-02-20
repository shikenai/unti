from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from myapp.management.commands import stocks, drawer, analizer
import mplfinance as mf
from myapp.models import Trades, Brand
from django_pandas.io import read_frame
import pandas as pd
import json


def test(request):
    analizer.test()
    return render(request, "test.html")


def get_trade_data(request):
    req = json.loads(request.body)
    plt = drawer.get_svg2http_response(int(req["days"]), req["brand_code"])
    return HttpResponse(plt)


def get_brand_list(request):
    _brand = Brand.objects.all()
    json_brand = list(_brand.values())
    return JsonResponse(json_brand, safe=False)


def home(request):
    return redirect("http://localhost:5173/")
