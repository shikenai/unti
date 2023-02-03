from django.shortcuts import render, redirect
from django.http import JsonResponse
from myapp.management.commands import stocks


def index(request):
    # stocks.reg_brands_from_csv()　実施済み
    # stocks.reg_trades_from_csv() 実施済み 20分くらいかかったので、改善希望
    return JsonResponse({"user": [
        {"id": 1, "name": "taro"},
        {"id": 2, "name": "jiro"},
    ]})


def home(request):
    return redirect("http://localhost:5173/")
