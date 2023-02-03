from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from myapp.management.commands import stocks, drawer
import mplfinance as mf
from myapp.models import Trades
from django_pandas.io import read_frame
import pandas as pd


def index(request):
    if True:
        _trades = Trades.objects.filter(brand_code="1301.jp").order_by("trade_date")
        for t in _trades.all()[0:15]:
            print(t.values())
        df = read_frame(_trades.all()[0:15])
        df["trade_date"] = pd.to_datetime(df["trade_date"])
        df = df.set_index("trade_date")
        df = df.reindex(columns=['open_value', 'high_value', 'low_value', 'close_value', 'volume'])
        df = df.rename(columns={'open_value': "Open", 'high_value': "High", 'low_value': "Low", 'close_value': "Close",
                                'volume': "Volume"})
        mf.plot(df, type="line")

    print(type(df))

    # stocks.reg_brands_from_csv()　実施済み
    # stocks.reg_trades_from_csv() 実施済み 20分くらいかかったので、改善希望
    # return JsonResponse({"user": [
    #     {"id": 1, "name": "taro"},
    #     {"id": 2, "name": "jiro"},
    # ]})

    plt = drawer.get_svg()
    print(type(plt))
    print(plt)
    return HttpResponse(plt)
    # return HttpResponse("hello")


def home(request):
    return redirect("http://localhost:5173/")
